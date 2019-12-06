# Expense-Tracker

Expense Tracker is an application which lets the user log in and track their expenses. The app displays the expenses in a list and on a chart.
The app uses Django_chartit to display charts.

Django version: 2.2.7
Python version: 3.6.8


### Installing and Prerequisites

To run the app locally:

1. Create virtualenv and run it:

```
virtualenv venv

source venv/bin/activate
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Migrate:

```
python manage.py migrate
```

4. Create a superuser:

```
python manage.py createsuperuser
```

5. Finally run the server:

```
python manage.py runserver
```

### Usage

Before setting ap an account as a user, you have to add currencies as an admin. 
You can do it by going to admin panel, then EXPENSE > Currencys > ADD CURRENCY


