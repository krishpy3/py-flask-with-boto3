import sqlite3

conn = sqlite3.connect('test.sqlite3')

cur = conn.cursor()

# cur.execute('''CREATE TABLE movies (
#     year INT NOT NULL,
#     title VARCHAR NOT NULL,
#     release_date VARCHAR,
#     running_time_secs INT
# )''')


# mov_list = [(2009, "I Love You Phillip Morris", "2009-01-18T00:00:00Z", 5880),
#             (2013, "Rush", "2013-09-02T00:00:00Z",  7380),
#             (2013, "Prisoners", "2013-08-30T00:00:00Z", 9180),
#             (2014, "X-Men: Days of Future Past", "2014-05-21T00:00:00Z", 'null')]

# for mov in mov_list:
#     # print(mov)
#     cur.execute("""INSERT INTO movies
#     (year, title, release_date, running_time_secs) VALUES {}""". format(mov))

# conn.commit()


# cur.execute('SELECT * FROM movies')
# hello = cur.fetchmany(2)
# print(hello)
# cur.close()
# conn.close()


cur.execute('''CREATE TABLE user (
    username TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT,
    password TEXT
)''')
