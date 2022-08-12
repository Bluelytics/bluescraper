import datetime, shutil, tempfile, locale, subprocess, os, uuid, boto3
from pytz import timezone
from database import getConnection
from decimal import Decimal
from buffer import send_post

buenos_aires = timezone("America/Buenos_Aires")

def social_network_update(social_network, min_alert_minutes):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute("""
        with historical_value as (
        select
            min(value_sell) value_min,
            max(value_sell) value_max
        from dolar_evolution
        where dttm > current_date - 2
        and dttm < current_date
        and tipo = 'Blue'
        ),
        current_value as (
        select
            value_buy as  value_current_buy,
            value_sell as value_current_sell
        from dolar_latest
        where tipo = 'blue'
        ),
        current_oficial as (
        select
            value_buy as  oficial_current_buy,
            value_sell as oficial_current_sell
        from dolar_latest
        where tipo = 'oficial'
        ),
        ranked_updates as (
        select
        *, row_number() over(order by update_at desc) as rnk
        from actualizaciones_sociales
        where social_network = %s
        ),
        last_update as (
        select
        value_sell as value_last_update, update_at as update_at_last
        from ranked_updates
        where rnk = 1
        )
        select value_current_buy, value_current_sell, oficial_current_buy, oficial_current_sell, value_min, value_max, value_last_update, update_at_last
        from current_value
        full join current_oficial on 1=1
        full join historical_value on 1=1
        full join last_update on 1=1
        """, (social_network,))
    res = cursor.fetchone()
    cursor.close()
    connection.close()

    value_current_buy = res[0]
    value_current_sell = res[1]
    oficial_current_buy = res[2]
    oficial_current_sell = res[3]
    value_min = res[4]
    value_max = res[5]
    value_last_update = res[6]
    update_at_last = res[7]
    now = datetime.datetime.now()


    if value_min is None:
        value_min = 0.0
    if value_max is None:
        value_max = 9999999999999999.0

    if update_at_last is None:
        update_at_last = datetime.datetime(2020, 5, 17)
    diff_update = now - update_at_last
    
    if diff_update.seconds > min_alert_minutes*60: # At least <alert> minutes since last update

        if float(value_current_sell) > value_max or float(value_current_sell) < value_min: # Alert
            change_perc = abs((float(value_current_sell / value_last_update) - 1.0)*100) # Percentage change since last alert
            
            if change_perc >= 0.75:
                send_update(social_network, value_current_buy, value_current_sell, oficial_current_buy, oficial_current_sell, value_last_update)
                
    

def send_update(social_network, value_current_buy, value_current_sell, oficial_current_buy, oficial_current_sell, value_last_update):
    try:
        locale.setlocale(locale.LC_TIME, "es_AR.UTF-8")
        
        shutil.copytree('alerts', '/tmp/%s' % social_network)
        tmpFilename = '/tmp/%s/out.html' % social_network
        with open(tmpFilename, 'wt') as o:
            with open('alerts/update_template.html') as f:
                template = f.read()

                template = template.replace('%Blue_Compra%', '{:.2f}'.format(value_current_buy))
                template = template.replace('%Blue_Venta%', '{:.2f}'.format(value_current_sell))
                template = template.replace('%Oficial_Compra%', '{:.2f}'.format(oficial_current_buy))
                template = template.replace('%Oficial_Venta%', '{:.2f}'.format(oficial_current_sell*Decimal(1.75)))

                template = template.replace('%FECHA%', datetime.datetime.now(tz=buenos_aires).strftime('%c'))
                o.write(template)
                o.flush()

        outName = '/tmp/%s.jpg' % social_network
        widths = {'facebook': '960', 'instagram': '960', 'twitter': '1350', 'linkedin': '1200'}
        heights = {'facebook': '720', 'instagram': '720', 'twitter': '706', 'linkedin': '628'}
        subprocess.run(['wkhtmltoimage', '--width', widths[social_network], '--height', heights[social_network], tmpFilename, outName])
        subprocess.run(['jpegoptim', outName])
        
        s3_name = '{}/{}-{}.jpg'.format(social_network, datetime.datetime.today().strftime('%Y-%m-%d'), uuid.uuid4())
        print('Uploading {}'.format(s3_name))

        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(outName, os.environ['S3_BUCKET'], s3_name)
        except ClientError as e:
            logging.error(e)
            return False
                
        if value_current_sell > value_last_update:
            action = "subio"
        else:
            action = "bajo"

        messages = {
            'instagram': 'El Dolar Libre/Blue {} a {:.2f} \n\n\n #dolar #dolarblue #argentina #economia',
            'facebook': 'El Dolar Libre/Blue {} a {:.2f} - Visita https://bluelytics.com.ar para mantenerte al día!',
            'twitter': 'El Dolar Libre/Blue {} a {:.2f} - Visita https://bluelytics.com.ar para mantenerte al día!'
        }

        status = send_post(social_network, messages[social_network].format(action, value_current_sell), s3_name)
        print('Status: {}'.format(status))
        
        if status != 200:
            print("Error sending update!")

        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute("insert into actualizaciones_sociales values(DEFAULT, %s, CURRENT_TIMESTAMP, %s, %s)",
            (social_network, value_current_buy, value_current_sell))
        connection.commit()
        cursor.close()
        connection.close()

    finally:
        locale.setlocale(locale.LC_TIME, "C")


now = datetime.datetime.today()

if now.weekday() < 5 and now.hour >= 13 and now.hour < 22:
    social_network_update('twitter', 15) # 15 minutes
    social_network_update('instagram', 60) # 1 hour
    social_network_update('facebook', 60) # 1 hour
