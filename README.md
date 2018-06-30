# LA ANALYSIS PROJECT

Analyzes data from PostgreSQL and displays results.

## Getting Started

Make sure you have Python 2.7 and PostgreSQL installed onto your machine.

### Prerequisites

Install pycodestyle to test code style

```
pip install pycodestyle
```

Views are incorporated into code, no need to manually paste them into psql.
However, views are formed shown below:

```
create view all_count as select date(time) as day, count(*) as all_method 
from log group by day;
```

```
create view error_count as select date(time) as day, count(*) as error_method 
from log 
where status like '%404%' group by day;
```

```
create view error_percent as select error_count.day, error_count.error_method * 100/ all_count.all_method::decimal as error_rate 
from error_count, all_count 
where error_count.day = all_count.day;
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

  "Candidate is jerk, alleges rival"  -  342102  views
  "Bears love berries, alleges bear"  -  256365  views
  "Bad things gone, say good people"  -  171762  views

Who are the most popular article authors of all time?

  Ursula La Multa  -  512805  views
  Rudolf von Treppenwitz  -  427781  views
  Anonymous Contributor  -  171762  views
  Markoff Chaney  -  85387  views

On which days did more than 1% of requests lead to errors?

  July 17, 2016  -  2.26 % errors

## Built With

* Python 2.7.12
* PostgreSQL

## Authors

John C