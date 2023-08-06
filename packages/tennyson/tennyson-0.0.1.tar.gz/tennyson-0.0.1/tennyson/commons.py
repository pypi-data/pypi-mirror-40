import os, errno, subprocess, json, socket

# TODO remove config
from   tennyson.config  import get_config

# from   secrets import AWS_KEY_ID, AWS_SECRET_KEY

hostname = socket.gethostname()

def mkdir_p(path: str) -> None:
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def j_load(path):
    with open(path) as fp:
        return json.load(fp)

def j_dump(obj, path):
    with open(path, 'w') as fp:
        return json.dump(obj, fp)

def encrypt_pipe(file_obj, pipe):
    recipients = [a for recipient in get_config()['GPG_KEY_UIDS']
                  for a in ['-r', recipient]]
    encrypt    = subprocess.Popen(['gpg', '--encrypt'] + recipients,
                    stdin=pipe, stdout=file_obj)
    encrypt.wait()

