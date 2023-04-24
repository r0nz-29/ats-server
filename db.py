import psycopg2

conn = psycopg2.connect(
    "postgres://szkeqarh:lsI99T4FCsUdOlkOyzimbaYI0_oC9fIZ@lallah.db.elephantsql.com/szkeqarh")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
# cur.execute('DROP TABLE IF EXISTS keywords;')
cur.execute('CREATE TABLE history (id serial PRIMARY KEY,'
            'name text NOT NULL,'
            'score text NOT NULL,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);'
            )

# Insert data into the table

cur.execute('INSERT INTO history (name, score)'
            'VALUES (%s, %s)',
            ('Raunit',
             '98%')
            )

cur.execute('INSERT INTO history (name, score)'
            'VALUES (%s, %s)',
            ('Shrivastava',
             '99.9%')
            )


conn.commit()

cur.close()
conn.close()
