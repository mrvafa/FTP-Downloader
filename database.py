"""
This file is responsible for creating, inserting, and editing from the database.
This database has two tables.
    1. URL (id INTEGER PRIMARY KEY,
           URL text not null unique,
           date DateTime DEFAULT CURRENT_TIMESTAMP)
    2. counter (id INTEGER)

The URLs has unique id and DateTime. DateTime is the time that a URL will add to the database.
The counter is the index that will get the URL from the database and extract links from that site.
"""
import sqlite3


# Create database and table for saving url
def create_table():
    con = sqlite3.connect('urls.db')
    cur = con.cursor()

    cur.execute('''CREATE TABLE if not exists  urls
                   (id INTEGER PRIMARY KEY,
                   url text not null unique,
                    date datetime DEFAULT CURRENT_TIMESTAMP)''')

    cur.execute('''CREATE TABLE if not exists  counter (id INTEGER) ''')

    con.commit()

    con.close()


# Insert url to database
def insert_url(url):
    con = sqlite3.connect('urls.db')
    cur = con.cursor()

    cur.execute("insert into urls (url) values (?)", (url,))

    con.commit()

    con.close()


# Returns True if url exist in database, else False.
def url_exists(url):
    con = sqlite3.connect('urls.db')
    cur = con.cursor()

    cur.execute("select url from urls where url = ?", (url,))

    res = cur.fetchone()

    con.close()

    return res is not None


# Get url by id from database
def get_url_by_id(_id):
    con = sqlite3.connect('urls.db')
    cur = con.cursor()

    cur.execute("select url from urls where id = ?", (_id,))

    res = cur.fetchone()

    con.close()

    return res[0].strip()


# Get urls length. (last id number for url)
def get_urls_length():
    con = sqlite3.connect('urls.db')
    cur = con.cursor()

    cur.execute("select count(url) from urls", )

    res = cur.fetchone()

    con.close()

    return res[0]


# Set counter to zero and store to database
def set_counter():
    con = sqlite3.connect('urls.db')
    cur = con.cursor()

    cur.execute("select id from counter")

    _id = cur.fetchone()
    if _id:
        cur.execute("delete from counter where id = ?", (_id,))
    cur.execute("insert into counter (id) values (?)", (1,))
    con.commit()

    con.close()


# Increment counter (counter += 1) and store to database
def increment_counter():
    con = sqlite3.connect('urls.db')
    cur = con.cursor()
    _id = get_counter()
    cur.execute("update counter set id = ? where id = ?", (_id + 1, _id))
    con.commit()

    con.close()


# Get number of counter
def get_counter():
    con = sqlite3.connect('urls.db')
    cur = con.cursor()
    cur.execute("select id from counter")
    _id = cur.fetchone()
    if not _id:
        set_counter()
        cur.execute("select id from counter")
        _id = cur.fetchone()
    return _id[0]
