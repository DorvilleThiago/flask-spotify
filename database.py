import psycopg2

host = 'tyke.db.elephantsql.com'
database = 'tctcetpl'
user = 'tctcetpl'
password = '2g0fBGouNALROhPmbbbyF4r1EruJgiIc'

def create_connection():
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    return {
        "cursor": cursor,
        "conn": conn
    }