# README_internals.md

## Async Pitfalls in Frappe Client Scripts

### Making a frappe.call inside the validate client event (before_save handler)
This does not work reliably because the `validate` event is synchronous, while `frappe.call` is asynchronous. The validation process may complete before the API call returns, leading to race conditions where the validation logic depends on the call's result. For example, if you try to validate a field based on an API response, the validation might pass or fail unpredictably.

**Bad Example (Do Not Use):**
```javascript
frappe.ui.form.on('Job Card', {
    validate: function(frm) {
        frappe.call({
            method: 'some.api.check_something',
            args: { value: frm.doc.some_field },
            callback: function(r) {
                if (!r.message.valid) {
                    frappe.validated = false; // Too late, validation already passed
                }
            }
        });
    }
});
```

### Using onload or refresh for async data fetches
This is the correct approach. Perform async operations like API calls in `onload` (for initial setup) or `refresh` (for dynamic updates), ensuring the UI is ready and the operations complete properly.

**Good Example:**
```javascript
frappe.ui.form.on('Job Card', {
    onload: function(frm) {
        frappe.call({
            method: 'some.api.fetch_data',
            callback: function(r) {
                // Update form based on response
            }
        });
    }
});
```

## Tree DocType Explanation
A Tree DocType represents hierarchical data structures, such as organizational charts or nested categories. Examples include the "Account" DocType (for chart of accounts) or "Employee" (for reporting hierarchies). It allows records to have parent-child relationships, displayed in a tree view.

- **doctype_tree_js**: This file customizes the tree view behavior, similar to `doctype_list_js` for list views. It handles actions like adding/editing nodes, drag-and-drop, and custom indicators.
- **Required Fields**: A Tree DocType needs `parent_field` (links to the parent record) and `is_group` (boolean to indicate if it's a group/branch node).

## Client Script DocType vs Shipped JS Tradeoffs

### When to Use Client Script DocType
- **Pros**: Stored in the database, no deployment needed. Ideal for consultants making quick customizations without code changes.
- **Cons**: Not version-controlled, harder to track changes, and can cause production instability if misused (e.g., conflicting scripts).

### When to Use Shipped JS
- **Pros**: Version-controlled in the app codebase, easier to maintain, test, and deploy. Preferred for developers building robust features.
- **Cons**: Requires app updates and redeployment for changes.

Consultants often use Client Script DocType for client-specific tweaks, while app developers use shipped JS for core functionality.

## Field Hiding vs Permission Security Pitfall
Hiding fields in JS (e.g., `frm.set_df_property("customer_phone", "hidden", 1);`) only affects the UI—it does not enforce security. An API call can still retrieve the field value, as permissions are checked at the server level, not the client.

**Demo**: In `job_card.js`, we hide `customer_phone` for non-managers:
```javascript
if (!frappe.user.has_role("Manager")) {
    frm.set_df_property("customer_phone", "hidden", 1);
}
```
Despite hiding, `frappe.call({ method: "frappe.client.get_value", args: { doctype: "Job Card", name: frm.doc.name, fieldname: "customer_phone" } })` will return the value if the user has read permissions. Always use DocType permissions for true security, not JS hiding.