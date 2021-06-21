import datetime, shutil, tempfile, locale, subprocess, os, uuid, boto3, json
from database import getConnection
from decimal import Decimal
from buffer import send_post

def social_network_weekly_update(social_network):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute("""
        select extract(days from current_timestamp-coalesce(max(sent_at), '2020-05-01')) days_last_update from actualizaciones_sociales_weekly
        where social_network = %s
    """, (social_network,))
    res = cursor.fetchone()

    if res[0] < 5:
        print('Already sent')
        return

    cursor.execute("""
         select
            dttm,
            extract(dow from dttm) day_of_week,
            value_sell
        from dolar_evolution
        where
            date_trunc('week', dttm) = date_trunc('week', current_date)
            and extract(dow from dttm) between 1 and 5
            and tipo = 'Blue'
           order by dttm
    """)
    res = cursor.fetchall()
    cursor.close()
    connection.close()

    try:
        locale.setlocale(locale.LC_TIME, "es_AR.UTF-8")

        mapDays = {1: "Lunes", 2: "Martes", 3: "Miércoles", 4:"Jueves",5:"Viernes"}

        arrayData = [{"x": mapDays[r[1]], "y": '{:.2f}'.format(r[2])} for r in res]
        print(json.dumps(arrayData))
        firstRes = res[0]
        lastRes = res[4]
        firstValue = firstRes[2]
        lastValue = lastRes[2]
        changeAbs = lastValue-firstValue
        plusChange = ''
        if lastValue > firstValue:
            plusChange = '+'
        changePerc = round((changeAbs / firstValue) * 100, 2)
        firstDate = firstRes[0].strftime('%d %b %Y')
        lastDate = lastRes[0].strftime('%d %b %Y')
        
        shutil.copytree('weekly_chart', '/tmp/%s' % social_network)
        tmpFilename = '/tmp/%s/out.html' % social_network
        with open(tmpFilename, 'wt', encoding='utf-8') as o:
            with open('weekly_chart/weekly.html', 'rt', encoding='utf-8') as f:
                template = f.read()

                template = template.replace('%Value_Inicio%', '{:.2f}'.format(firstValue))
                template = template.replace('%Value_Fin%', '{:.2f}'.format(lastValue))
                template = template.replace('%Delta_Value%', '{}{:.2f}'.format(plusChange, changeAbs))
                template = template.replace('%Delta_Percent%', '{}{:.2f}'.format(plusChange, changePerc))
                template = template.replace('%Array_Data%', json.dumps(arrayData))
                template = template.replace('%Fecha_Inicio%', firstDate)
                template = template.replace('%Fecha_Fin%', lastDate)
                o.write(template)
                o.flush()
        locale.setlocale(locale.LC_TIME, "C")

        outName = '/tmp/%s.jpg' % social_network
        widths = {'facebook': '960', 'instagram': '960', 'twitter': '1350'}
        heights = {'facebook': '720', 'instagram': '720', 'twitter': '706'}
        subprocess.run(['wkhtmltoimage', '--debug-javascript', '--javascript-delay', '2000', '--width', widths[social_network], '--height', heights[social_network], tmpFilename, outName])
        subprocess.run(['jpegoptim', outName])
        
        s3_name = '{}/{}-{}.png'.format(social_network, datetime.datetime.today().strftime('%Y-%m-%d'), uuid.uuid4())
        print('Uploading {}'.format(s3_name))

        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(outName, os.environ['S3_BUCKET'], s3_name)
        except ClientError as e:
            logging.error(e)
            return False
        
        messages = {
            'instagram': 'Evolucion Dolar Blue de esta semana! \n\n\n #dolar #dolarblue #argentina #economia',
            'facebook': 'Evolucion Dolar Blue de esta semana! - Visita https://bluelytics.com.ar para mantenerte actualizado/a!',
            'twitter': 'Evolucion Dolar Blue de esta semana! - Visita https://bluelytics.com.ar para mantenerte actualizado/a!\n #dolar #dolarblue #argentina #economia'
        }

        status = send_post(social_network, messages[social_network], s3_name)

        if status != 200:
            print("Error!")
        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute("insert into actualizaciones_sociales_weekly values(DEFAULT, %s, CURRENT_TIMESTAMP)",
            (social_network,))
        connection.commit()
        cursor.close()
        connection.close()

    finally:
        locale.setlocale(locale.LC_TIME, "C")

    


now = datetime.datetime.today()

if now.weekday() == 4 and now.hour >= 21:
    social_network_weekly_update('twitter')
    social_network_weekly_update('instagram')
    social_network_weekly_update('facebook')
