# Django Singhealth Project


## Group Members:

Chang Min xuan -> Minxuan77

Ang Sok Teng Cassie -> Kahssie

Pan Feng -> Adler-p

Peh Jing Xiang -> pjx98

## Features:

 * Add new tenant/delete existing tenant
 * Fill in and submit checklist
 * Upload photos (e.g. non-compliance)
 * Automatically compute checklist score
 * Export/send checklist to email address
 * Select timeframe to rectify non-compliance (i.e. immediate, <3 days, <1 week) Tenant may request for 
 extension with reasons.
 * Dashboard to show tenants’ rectification progress
 * Security feature to securely transmit and store data
 * Retail tenant to write notes/upload photos to close 
findings
 * Prompt retail tenant on outstanding non-compliance
 * Dynamic checklist function.





## Getting Started
```
git clone https://github.com/minxuan77/TecWatch.git
```

## To run our application: 

Navigate to TecWatch-master directory

After creating virtual environment and activating it, run:
```
pip install -r requirements.txt
```
## Setting up database

Run these commands:
```
python manage.py makemigrations
python manage.py migrate
```
## To run web application:

Run the following command:
```
python manage.py runserver
```
Open another terminal and run:
```
python manage.py process_tasks 
```



## Running Tests

Navigate to singhealth/tests folder where our tests are located.

The command to run the specific tests are commented above the test functions.

For example, if you want to run Selenium test_user_full_cycle() tests, navigate to singhealth/tests/test_selenium.py, find the commented command line above the test and run.

Example is show below:
```
python manage.py test singhealth.tests.test_selenium.seleniumTest.test_user_full_cycle
```

More details can be found in our final report: [C4G6_Final_Report.pdf](https://github.com/pjx98/TecWatch/blob/master/C4G6_Final_Report.pdf)



