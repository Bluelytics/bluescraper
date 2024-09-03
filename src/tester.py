import psycopg2, os

def getConnection():
    return psycopg2.connect(user = os.environ['PG_USER'],
                                  password = os.environ['PG_PASSWORD'],
                                  host = os.environ['PG_HOSTNAME'],
                                  port = "5432",
                                  database = os.environ['PG_DB'])

def insertBlue(source, value_buy, value_sell):
    print(f"Insert for {source}: {value_buy} - {value_sell}")

