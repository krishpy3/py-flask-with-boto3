# CREATE TABLE

`CREATE TABLE <table-name> ( col1 coltype, col2 coltype );`

`CREATE TABLE movies (
    year INT NOT NULL,
    title VARCHAR NOT NULL,
    release_date VARCHAR,
    running_time_secs INT
)`


# INSERT DATA

`INSERT INTO <table-name> (column_list) VALUES (data)`

`INSERT INTO movies (year, title, release_date, running_time_secs) VALUE (2009, "I Love You Phillip Morris", "2009-01-18T00:00:00Z", 5880);`

`INSERT INTO movies (year, title) VALUE (2006, "Big Momma's House 2",);`


# SELECT
`SELECT (cl, c2, c3) FROM Table-name`

`SELECT (year, title) FROM movies`


# UPDATE
`UPDATE table-name SET c1=NewValue, c2=NewValue WHERE `
`UPDATE movies SET running_time_secs=9000 where year=2013;`


# DELETE
`DELETE FROM movies where year=2013;`
