#
# Initialize DB schema and fill in database entries.
#
# Should be executed one time for a particular RDS DB.
#
# This file is not part of the application. It is intended to be
# run standalone once per deployment.
#
# If running from the command line, during testing, run it as:
#
# $ RDS_HOSTNAME=... RDS_PORT=... RDS_USER=... RDS_PASSWORD=... RDS_DB_NAME=... python -c "import initdb; initdb.init_db()"
#
import settings
import pymysql
import os

def connect_db():
    conn = pymysql.connect(
        host = settings.DB_HOST,
        port = settings.DB_PORT,
        user = settings.DB_USER,
        passwd = settings.DB_PASSWD,
        db = settings.DB_NAME
        )
    return conn
#
# For first time initialization: create DB schema if it does
# not exist.
#
def init_db():
    print("Initializing DB")
    print("RDS_HOSTNAME is " + os.environ['RDS_HOSTNAME'])
    from contextlib import closing
    with closing(connect_db()) as conn:
        cursor = conn.cursor()
        if not table_exists(cursor, 'users'):
            create_schema(cursor)
        else:
            print("Not creating schema.")
        conn.commit()

def table_exists(cursor, tablename):
    print("Checking if table " + tablename + " exists...")
    cursor.execute("SHOW TABLES LIKE '%s'" % tablename)
    rs = cursor.fetchall()
    if len(rs) == 1 and rs[0][0] == 'users':
        print("Table " + tablename + " already exists.")
        return True
    else:
        print("Table " + tablename + " does not exist.")
        return False

def create_schema(cursor):
    print("Creating schema")
    cursor.execute("""
        CREATE TABLE users (
            id SERIAL NOT NULL AUTO_INCREMENT PRIMARY KEY
            , name CHAR(255) NOT NULL UNIQUE KEY
            , password CHAR(255) NOT NULL)
            engine=InnoDB
        """)
    cursor.execute("""
        INSERT INTO users (name, password) VALUES
        ('anne', 'secret123'),
        ('joe', 'secret123')
        """)
    cursor.execute("""
        CREATE TABLE entries (
            id SERIAL NOT NULL AUTO_INCREMENT PRIMARY KEY
            , title VARCHAR(255) NOT NULL
            , body TEXT NOT NULL
            , posted_at TIMESTAMP NOT NULL
            , posted_by CHAR(255) NOT NULL) engine = InnoDB
        """)
    cursor.execute("""
        INSERT INTO entries (title, body, posted_at, posted_by) VALUES
        ('My first entry', 'I used Elastic Beanstalk, and it was good.', NOW(), 'anne'),
        ('My second entry', 'I used Elastic Beanstalk, and it was good.', NOW(), 'joe')
        """)
