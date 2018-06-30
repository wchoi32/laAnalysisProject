#!/usr/bin/python2.7
import psycopg2

DBNAME = "news"


def first_question_answer():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        "select articles.title, count(*) "
        "from articles join log on log.path "
        "like '%' || articles.slug || '%' "
        "group by articles.title "
        "order by count desc limit 3;")
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
        "select authors.name, count(*) "
        "from authors join articles "
        "on authors.id = articles.author "
        "join log on log.path "
        "like '%' || articles.slug || '%' "
        "group by authors.name "
        "order by count desc;")
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
        "create view all_count as select date(time) as day, "
        "count(*) as all_method from log group by day;")
    c.execute(
        "create view error_count as select date(time) as day, "
        "count(*) as error_method from log "
        "where status like '%404%' group by day;")
    c.execute(
        "create view error_percent as select error_count.day, "
        "error_count.error_method * 100/ all_count.all_method::decimal "
        "as error_rate "
        "from error_count, all_count where error_count.day = all_count.day;")
    c.execute(
        "select day, error_rate "
        "from error_percent "
        "where error_rate >= 1 "
        "order by error_rate desc;")
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
