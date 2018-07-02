# LA ANALYSIS PROJECT

This project was set up using PostgreSQL database for a news website.
Python script uses the psycopg2 library to query the database. 

## Getting Started

Make sure you have Python 2.7 and PostgreSQL installed onto your machine.

### Prerequisites

Install pycodestyle to test code style

```
pip install pycodestyle
```

Threre are three tables in the news database: articles, authors, and log
Articles contain columns author, title, slug, lead, body, time, id
Authors contain columns name, bio, id
Logs contain path, ip, method, status, time, id

Views are incorporated into code, no need to manually paste them into psql.
However, views are formed shown below:

```
CREATE OR REPLACE VIEW all_count AS
SELECT date(TIME) AS DAY,
       count(*) AS all_method 
FROM log 
GROUP BY DAY;
```

```
CREATE OR REPLACE VIEW error_count AS 
SELECT date(TIME) AS DAY, 
       count(*) AS error_method 
FROM log 
WHERE status = '404 NOT FOUND' 
GROUP BY day;
```

```
CREATE OR REPLACE VIEW error_percent AS 
SELECT error_count.day, 
       error_count.error_method * 100/ all_count.all_method::decimal AS error_rate 
FROM error_count, all_count 
WHERE error_count.day = all_count.day;
```

### How to run

Run the following command onto terminal:

```
python la_analysis.py
```

Once, ran it will query the database and return answers for the three questions

### And coding style tests

To check Python style: 

```
pycodestyle la_analysis.py
```

## Data Output

What are the most popular three articles of all time?

  "Candidate is jerk, alleges rival"  -  338647  views
  "Bears love berries, alleges bear"  -  253801  views
  "Bad things gone, say good people"  -  170098  views

Who are the most popular article authors of all time?

  Ursula La Multa  -  507594  views
  Rudolf von Treppenwitz  -  423457  views
  Anonymous Contributor  -  170098  views
  Markoff Chaney  -  84557  views

On which days did more than 1% of requests lead to errors?

  July 17, 2016  -  2.26 % errors

## Built With

* Python 2.7.12
* PostgreSQL

## Authors

John C