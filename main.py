import psycopg2


COLORS = (
   'black',
   'white',
   'black & white',
   'red',
   'red & white',
   'red & black & white',
)

db_connection = None
cur = None


def count(color):
    cur.execute('SELECT COUNT (name) ' +
                'FROM cats ' +
                'WHERE cats.color=\'' + color + '\'')

    amount = cur.fetchone()

    return amount


def write_color_info(color, amount):
    print(f'{color} - {amount}')

    try:
        cur.execute('INSERT INTO cat_colors_info (color, count) ' +
                    'VALUES (%s, %s)', (color, amount))

        return
    except psycopg2.IntegrityError:
        cur.execute("ROLLBACK")

    try:
        cur.execute('UPDATE cat_colors_info ' +
                    'SET count = %s ' +
                    'WHERE color = %s', (amount, color))
    except psycopg2.IntegrityError as exc:
        print(exc)
        cur.execute("ROLLBACK")


def main():
    for cat_color in COLORS:
        amount = count(cat_color)
        write_color_info(cat_color, amount[0])

if __name__ == "__main__":
    db_connection = psycopg2.connect(host="postgreDB",
                                     database="wg_forge_db",
                                     user="wg_forge",
                                     password="42a")

    cur = db_connection.cursor()

    main()

    db_connection.commit()

    cur.close()
    db_connection.close()
