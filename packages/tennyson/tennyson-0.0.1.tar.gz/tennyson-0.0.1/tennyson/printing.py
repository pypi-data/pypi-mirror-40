import logging, inspect, traceback, json, sys, time, datetime, socket, \
    psutil, os
import boto3, botocore
from   typing import List
from   tennyson.vault import get_secrets


def mklog(name: str=None):
    if not name:
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        name = module.__file__

    LOG = logging.getLogger(name)
    LOG.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    LOG.addHandler(ch)
    return LOG

def date_stamp():
    return datetime.datetime.today().strftime('%Y-%m-%d')

def datetime_stamp():
    return datetime.datetime.today().strftime('%Y-%m-%d_%H%M%S')

def datetime_zone_stamp() -> str:
    offset = '{}{:0>2}{:0>2}'\
        .format('-'
            if time.altzone > 0
            else '+', abs(time.altzone) // 3600, abs(time.altzone // 60) % 60)
    return datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + offset

def send_email_exn(recipients: List[str], subject: str, text: str) -> None:
    sender     = 'bot@tennysontbardwell.com'
    aws_region = 'us-east-1'
    secrets    = get_secrets()

    client = boto3.client('ses',
                          region_name=aws_region,
                          aws_access_key_id=secrets['AWS_KEY_ID'],
                          aws_secret_access_key=secrets['AWS_SECRET_KEY'])
    response = client.send_email(
        Destination={
            'ToAddresses': recipients,
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': text,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=sender
    )

def alert_exn(message: str, subject=None) -> None:
    hostname = socket.gethostname()
    pid      = os.getpid()
    if not subject:
        subject = "Alert from process {} on {}".format(pid, hostname)
    cml      = psutil.Process(pid).cmdline()
    cwd      = os.getcwd()
    header   = json.dumps({'hostname': hostname, 'pid': pid, 'cml': cml,
                           'cwd': cwd}, indent=4)
    content  = header + '\n\n' + message
    send_email_exn(['tennysontaylorbardwell@gmail.com'], subject, content)

def error_email_exn(exception):
    tb = traceback.format_exc()
    alert_exn(tb)
