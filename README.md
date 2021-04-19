# Django Singhealth Project


## Group Members:

Chang Min xuan -> Minxuan77

Ang Sok Teng Cassie -> Kahssie

Pan Feng -> Adler-p

Peh Jing Xiang -> pjx98



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

## More details can be found in our final report
