### quickfix

Quickfix app

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app quickfix
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/quickfix
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### A2 Multisite and Congiguration
 
 ### 1.)config files
          There are two types of the config files usually found in frappe .When we create a new site in frappe ,it automatically creates a new site configuration file- ""site_config.json"" there it contains db_passwords,db_name,db_host values and if developer mode enabled then developer_mode:1.   
          
          Another configuration file is the -""common_site_configuration.json"" which includes the user details,port numbers
          and other  configurations which are applicable to all the sites available at the bench

### 2. ) Four processess

         when we start the bench there are four major processess occurs that is responsible for the smooth running of the bench and ensures the proper working of the system
         1.)WEB-it is kind of a dynamic process which handles the HTTP requests when ever the user triggers a request,it logs what are the requests send by the user and while starting the bench for example, 
         ![alt text](image-2.png)
         2.)REDIS-usually redis is used in frappe for two functionalities that is,*CACHE,*QUEUE
         ->redis caching is the process in which the frequently accessed data are stored in a temporary memory to ensure the faster  accessing of the data.It is mainly used  to cutdown of direct database access frequently .In simpler words redis cache is used to store the data which are frequently used 