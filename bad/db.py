
import sqlite3
from passlib.hash import pbkdf2_sha256

def db_init():

    users = [
        ('admin', pbkdf2_sha256.encrypt('adminPass')),
        ('john', pbkdf2_sha256.encrypt('PasswordQwerty')),
        ('tim', pbkdf2_sha256.encrypt('Vaider2Dart'))
    ]

    conn = sqlite3.connect('users.sqlite')
    c = conn.cursor()
    c.execute("DROP TABLE users")
    c.execute("CREATE TABLE users (user text, password text, failures int)")

    for u,p in users:
        c.execute("INSERT INTO users (user, password, failures) VALUES ('%s', '%s', '%d')" %(u, p, 0))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    db_init()

