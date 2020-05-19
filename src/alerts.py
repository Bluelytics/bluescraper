import datetime
from database import getConnection

def evaluate_alerts():
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute("""
            with historical_value as (
        select
            max(value_sell) value_max,
            min(value_sell) value_min
        from dolar_evolution
        where dttm > current_date - 1
        and tipo = 'Blue'
        ),
        current_value as (
        select
            value_buy as  value_current_buy,
            value_sell as value_current_sell
        from dolar_latest
        where tipo = 'blue'
        ),
        ranked_alertas as (
        select
        *, row_number() over(order by alert_at desc) as rnk
        from alertas_dolar
        ),
        last_alerta as (
        select
        value_sell as value_last_alert, alert_at as alerta_at_last
        from ranked_alertas
        where rnk = 1
        )
        select
            value_current_buy, value_current_sell, value_min, value_max, value_last_alert, alerta_at_last
        from current_value
        full join historical_value on 1=1
        full join last_alerta on 1=1
        ;""")
    res = cursor.fetchone()

    value_current_buy = res[0]
    value_current_sell = res[1]
    value_min = res[2]
    value_max = res[3]
    value_last_alert = res[4]
    alerta_at_last = res[5]
    now = datetime.datetime.now()

    diff_alerta = now - alerta_at_last
    
    if diff_alerta.seconds > 30*60: # At least 30 minutes since last alert
        if value_current_sell > value_max or value_current_sell < value_min:
            change_perc = abs((float(value_current_sell / value_last_alert) - 1.0)*100) # Percentage change since last alert

            if change_perc > 0.5:
                change = round(value_current_sell - value_last_alert, 2)
                
                cursor.execute("insert into alertas_dolar values(DEFAULT, CURRENT_TIMESTAMP, %s, %s)",
                (value_current_buy, value_current_sell))
                connection.commit()
    cursor.close()
    connection.close()


evaluate_alerts()
