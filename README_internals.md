# README_internals.md

# B2 - ORM Internals & Query Builder
   ### Part A - Table naming (bench console)
            In [1]: frappe.db.sql("SHOW TABLES LIKE '%Job%'")
            Out[1]: (('tabJob Card',), ('tabScheduled Job Log',), ('tabScheduled Job Type',))

               In [2]: frappe.db.sql("DESCRIBE `tabJob Card`", as_dict=True)
                    Out[2]:
                [{'Field': 'name',
                'Type': 'varchar(140)',
                'Null': 'NO',
                'Key': 'PRI',
                'Default': None,
                'Extra': ''},
                {'Field': 'creation',
                'Type': 'datetime(6)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'modified',
                'Type': 'datetime(6)',
                'Null': 'YES',
                'Key': 'MUL',
                'Default': None,
                'Extra': ''},
                {'Field': 'modified_by',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'owner',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'docstatus',
                'Type': 'int(1)',
                'Null': 'NO',
                'Key': '',
                'Default': '0',
                'Extra': ''},
                {'Field': 'idx',
                'Type': 'int(8)',
                'Null': 'NO',
                'Key': '',
                'Default': '0',
                'Extra': ''},
                {'Field': 'customer_name',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'customer_phone',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'customer_email',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'device_type',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'device_brand',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'device_model',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'imei_or_serial',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'problem_description',
                'Type': 'longtext',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'assigned_technician',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'diagnosis_notes',
                'Type': 'longtext',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'estimated_cost',
                'Type': 'decimal(21,9)',
                'Null': 'NO',
                'Key': '',
                'Default': '0.000000000',
                'Extra': ''},
                {'Field': 'diagnosis_date',
                'Type': 'date',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'priority',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': 'Normal',
                'Extra': ''},
                {'Field': 'parts_total',
                'Type': 'decimal(21,9)',
                'Null': 'NO',
                'Key': '',
                'Default': '0.000000000',
                'Extra': ''},
                {'Field': 'labour_charge',
                'Type': 'decimal(21,9)',
                'Null': 'NO',
                'Key': '',
                'Default': '0.000000000',
                'Extra': ''},
                {'Field': 'final_amount',
                'Type': 'decimal(21,9)',
                'Null': 'NO',
                'Key': '',
                'Default': '0.000000000',
                'Extra': ''},
                {'Field': 'payment_status',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': 'Unpaid',
                'Extra': ''},
                {'Field': 'delivery_date',
                'Type': 'date',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'remarks',
                'Type': 'text',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'status',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'anonyomous',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'amended_from',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': 'MUL',
                'Default': None,
                'Extra': ''},
                {'Field': '_user_tags',
                'Type': 'text',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': '_comments',
                'Type': 'text',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': '_assign',
                'Type': 'text',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': '_liked_by',
                'Type': 'text',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''}]
    
### Part D - DocStatus transitions
In Frappe, docstatus has three  values: 0 means Draft, 1 means Submitted, and 2 means Cancelled.

UpdateAfterSubmitError:  Not allowed to change Customer Name after submission from sfgtr to Test---this is shwon when i try to save on the submited document
ValidationError: Cannot edit cancelled document--this is shown when an cancel document is tried to submit this is because that the document is already cancelled we need to amend it to make it submittable

when i try to save the document but others already saved that but the older version is showing that 

### Part E - Dangerous patterns
self.save() inside the validate() method is wrong because validate() is already triggered during the save process, so calling save() again will cause recursion

updating the stock quantity is done only in the on submit but here it is inside the validate but more than that validates just saves it so this action should only oerformed in the on submit
def validate(self):
    self.total = sum(r.amount for r in self.items)
def on_submit(self):
    other = frappe.get_doc("Spare Part", self.part)
    other.stock_qty -= self.qty
    other.save()

# C1
### Child Table Internals
        parent (the name of the main document), parenttype (the parent DocType), parentfield (the field name linking the child table), and idx (the row order).
        The database table name for the Part Usage Entry DocType will be tabPart Usage Entry 

        If a row (for example, at idx = 2) is deleted and the document is saved again, Frappe automatically reorders the remaining rows and updates their idx values sequentially  to maintain proper ordering.

### C3 - Part Usage Entry & Service Invoice
### Renaming task
when a Technician record is renamed , the assigned_technician field in linked Job Cards automatically updates because Frappe maintains links using  and internally updates all Doc name . 
  “track changes” means Frappe keeps a history of modifications (like renaming or field updates) so we can see what was changed and when it changed. 
  For unique constraints, setting a field as “unique” in database level which ensures that therer is no duplicate values
   using frappe.db.exists() in validate() is a manual check done in code, which can be bypassed in some cases and is less reliable compared to the built-in unique constraint.

### D1 -
If a user who is not a QF Manager calls this method, Frappe will raise a PermissionError and block the request before executing any further code. 

### D2
Using frappe.get_all in a method that anyone can call is not safe because it can return all data without checking who the user is. This means even a guest or low-level user might see important or private information. Normally, Frappe uses permission_query_conditions to show only the data a user is allowed to see, but get_all ignores this. So it can break security. To avoid this, we should use frappe.get_list, which automatically follows permission rules.

### E1 -Call self.save() inside on_update and see to the issues of it and explain them in the same readme_internals.
This usually occurs when i try to do it
RecursionError: maximum recursion depth exceeded while calling a Python object
instead of that we could use the db_set

### F3-Asset, Jinja & Website Hooks
app_include_js is used to load JavaScript files in the Frappe Desk (backend UI), which is what logged-in users like admins, managers,technicians

web_include_js is used to load JavaScript only on the website or portal pages (frontend), like a customer site

 doctype_js and doctype_list_js are used to add custom JavaScript behavior the document. doctype_js runs on the form view, which means it works when a document is opened, and it is used to give the some client script works . 
  doctype_list_js runs on the list view which shows allavailable  records  and it is used to add custom functionalities in the list page by adding buttons, showing messages. 

  usually the doctype_tree_js is not applicable here because the we ddoes not have a tree architecture or hierarchy which means the doctype which we have created does not have any tree doctype .A tree doctype have an hierarchy but the normal doctype doesnot have these kind of hierarchy

  when we run bench build the js,css file were loaded to the browser and then the Cache-busting is important because  store old js files in cache, so without rebuilding, updated code may not reflect. by rebuilding, Frappe forces the browser to load the latest version of the files that were the changes were made