import psycopg2

con = psycopg2.connect(
          database = "calhounio_demo",
          user = "postgres",
          password = "qwerty")

cur = con.cursor()

a = cur.execute("select id from users")

print(a)

con.close
'''
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  age INT,
  first_name TEXT,
  last_name TEXT,
  email TEXT UNIQUE NOT NULL
);
'''
