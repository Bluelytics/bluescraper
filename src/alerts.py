import datetime
from database import getConnection
import firebase_admin
from firebase_admin import messaging, credentials

def evaluate_alerts():
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute("""
    with values_blue as (
        select
        date_trunc('minute', scraped_at), avg(value_sell) as value
        from dolar_values
        where scraped_at > (now() - interval '2 hours')
        and scraped_at < (now() - interval '15 minutes')
        and source <> 'oficial'
        group by 1
        ),
        historical_value as (
            select 
            max(value) as value_max,
            min(value) as value_min
            from values_blue
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
    
    if diff_alerta.seconds > 10*60: # At least 10 minutes since last alert
        if value_current_sell > value_max or value_current_sell < value_min:
            change_perc = abs((float(value_current_sell / value_last_alert) - 1.0)*100) # Percentage change since last alert
            if change_perc > 0.5:
                
                send_alerta_mobile(value_current_sell, value_last_alert)

                cursor.execute("insert into alertas_dolar values(DEFAULT, CURRENT_TIMESTAMP, %s, %s)",
                (value_current_buy, value_current_sell))
                connection.commit()


    cursor.close()
    connection.close()

def send_alerta_mobile(value_current, value_prev):
    change_val = value_current - value_prev
    change_perc = (float(value_current / value_prev) - 1.0)*100
    if value_current > value_prev:
        title = 'Subió el Dólar Blue'
    else:
        title = 'Bajó el Dólar Blue'
    body = 'Venta: {:.2f} ({}{:.2f} / {}{:.2f}%)'.format(
        value_current,
        '+' if value_current > value_prev else '',
        change_val,
        '+' if value_current > value_prev else '',
        change_perc
    )

    cred = credentials.Certificate("/bluelytics-mobile-firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)
    
    msg = messaging.Message(
        notification = messaging.Notification(
            title = title,
            body = body
        ),
        android = messaging.AndroidConfig(
            collapse_key='dolar-blue',
            priority='high',
            ttl=1200,
            notification=messaging.AndroidNotification(
                title = title,
                body = body,
                color='#221199',
                channel_id='Dolar Blue'
            )
        ),
        topic = 'alertas-blue'
    )
    
    res = messaging.send(msg)
    return res

evaluate_alerts()
