import sqlite3


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


def increment_counter():
    con = sqlite3.connect('urls.db')
    cur = con.cursor()
    _id = get_counter()
    cur.execute("update counter set id = ? where id = ?", (_id + 1, _id))
    con.commit()

    con.close()


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


def insert_url(url):
    con = sqlite3.connect('urls.db')
    cur = con.cursor()

    cur.execute("insert into urls (url) values (?)", (url,))

    con.commit()

    con.close()


def url_exists(url):
    con = sqlite3.connect('urls.db')
    cur = con.cursor()

    cur.execute("select url from urls where url = ?", (url,))

    res = cur.fetchone()

    con.close()

    return res is not None


def get_url_by_id(_id):
    con = sqlite3.connect('urls.db')
    cur = con.cursor()

    cur.execute("select url from urls where id = ?", (_id,))

    res = cur.fetchone()

    con.close()

    return res[0].strip()


def get_urls_length():
    con = sqlite3.connect('urls.db')
    cur = con.cursor()

    cur.execute("select count(url) from urls", )

    res = cur.fetchone()

    con.close()

    return res[0]
