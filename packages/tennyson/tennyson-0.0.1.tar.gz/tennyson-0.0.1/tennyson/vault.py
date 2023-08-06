#!/usr/bin/env python3
import hvac, os, json
from pathlib import Path

_secrets = None

def get_secrets(path='scripts', mount_point='secret', token=None):
    global _secrets
    if _secrets:
        return _secrets


    if token is None:
        token = os.environ.get('TENNYSON_VAULT_TOKEN', None)

    if token:
        client = hvac.Client(url='https://vault.tennysontbardwell.com:8200',
                             token=token)
        client.renew_token()
    else:
        with open(os.path.join(str(Path.home()), '.config',
                'tennyson', 'scripts-vault-login')) as fp:
            vault = json.load(fp)
        client = hvac.Client(url=vault['url'])
        client.auth_approle(vault['role_id'], vault['secret_id'])

    res = client.secrets.kv.v2.read_secret_version(
        path=path, mount_point=mount_point)
    _secrets = res['data']['data']
    return _secrets

