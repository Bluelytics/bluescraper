import psycopg2, os

def getConnection():
    return psycopg2.connect(user = os.environ['PG_USER'],
                                  password = os.environ['PG_PASSWORD'],
                                  host = os.environ['PG_HOSTNAME'],
                                  port = "5432",
                                  database = os.environ['PG_DB'])

def insertBlue(source, value_buy, value_sell):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute("insert into dolar_values (scraped_at, source, value_buy, value_sell) values(current_timestamp, %s, %s, %s)",
    (source, value_buy, value_sell))
    connection.commit()
    cursor.close()
    connection.close()


def insertNewCurrency(code, name):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute("select count(*) from  currency_map where code = %s", (code,))
    res = cursor.fetchone()
    if res[0] == 0:
        print('New currency detected!: %s' % code)
        cursor.execute("select max(ID) from currency_map")
        res = cursor.fetchone()
        last_id = res[0]

        cursor.execute("insert into currency_map (id, code, name) values(%s, %s, %s)",
        (last_id+1, code, name))
        connection.commit()
    cursor.close()
    connection.close()


def insertCurrencyValue(code, value):
    connection = getConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("select id from currency_map where code = %s", (code,))
        res = cursor.fetchone()
        curr_id = res[0]
        
        cursor.execute("delete from currency_values where scraped_dt = current_date and currency_id = %s", (curr_id,))
        cursor.execute("insert into currency_values (scraped_dt, currency_id, value) values(current_date, %s, %s)",
        (curr_id, value))
        connection.commit()
    except Exception as error:
        print ("Oops! An exception has occured:", error)
    cursor.close()
    connection.close()

def refreshView(view_name):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY %s" % view_name)
    connection.commit()
    cursor.close()
    connection.close()