#!/usr/bin/python
import psycopg2

DBNAME = "news"


def first_question_answer():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        "SELECT articles.title, count(*) "
        "FROM articles JOIN log ON log.path = '/article/' || articles.slug "
        "GROUP BY articles.title "
        "ORDER BY count DESC LIMIT 3;")
    answer_one = c.fetchall()

    q_one = "What are the most popular three articles of all time?"
    print('\n' + q_one + '\n')
    for row in answer_one:
        print " ", '"%s"' % row[0], " - ", str(row[1]), " views"

    db.close()


def second_question_answer():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        "SELECT authors.name, count(*) "
        "FROM authors JOIN articles "
        "ON authors.id = articles.author "
        "JOIN log ON log.path = '/article/' || articles.slug "
        "GROUP BY authors.name "
        "ORDER BY count DESC;")
    answer_two = c.fetchall()

    q_two = "Who are the most popular article authors of all time?"
    print('\n' + q_two + '\n')
    for row in answer_two:
        print " ", row[0], " - ", str(row[1]), " views"

    db.close()


def third_question_answer():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        "CREATE OR REPLACE VIEW all_count AS SELECT date(time) AS day, "
        "count(*) AS all_method FROM log GROUP BY day;")
    c.execute(
        "CREATE OR REPLACE VIEW error_count AS SELECT date(time) AS day, "
        "count(*) AS error_method FROM log "
        "where status  = '404 NOT FOUND' GROUP BY day;")
    c.execute(
        "CREATE OR REPLACE VIEW error_percent AS SELECT error_count.day, "
        "error_count.error_method * 100/ all_count.all_method::decimal "
        "AS error_rate "
        "FROM error_count, all_count WHERE error_count.day = all_count.day;")
    c.execute(
        "SELECT day, error_rate "
        "FROM error_percent "
        "where error_rate >= 1 "
        "ORDER BY error_rate DESC;")
    answer_three = c.fetchall()

    q_three = "On which days did more than 1% of requests lead to errors?"
    print('\n' + q_three + '\n')
    for row in answer_three:
        print " ", str(row[0].strftime('%B %d, %Y')
                       ), " - ", str(round(row[1], 2)), "% errors"
    print('\n')

    db.close()


def main():
    first_question_answer()
    second_question_answer()
    third_question_answer()


if __name__ == '__main__':
    main()
