import requests, os, boto3

def send_post(social_network, msg, img):

    payload = {
        'access_token': os.environ['BUFFER_API_KEY'],
        'text': msg,
        'profile_ids[]': os.environ['SN_PROFILE_{}'.format(social_network.upper())],
        'shorten': 'false',
        'top': 'true',
        'now': 'true',
        'media[photo]': 'https://{}.s3-us-west-2.amazonaws.com/{}'.format(os.environ['S3_BUCKET'], img),
        'media[thumbnail]': 'https://{}.s3-us-west-2.amazonaws.com/{}'.format(os.environ['S3_BUCKET'], img)
    }
    r = requests.post("https://api.bufferapp.com/1/updates/create.json", data=payload)

    if r.status_code != 200:
        print(r.text)

    sns = boto3.client("sns")
    sns.publish(TopicArn='arn:aws:sns:us-west-2:151654911502:mailPablo', 
            Message="{}\n\nhttps://{}.s3-us-west-2.amazonaws.com/{}".format(msg, os.environ['S3_BUCKET'], img), 
            Subject="New update available for {}".format(social_network))

    return r.status_code