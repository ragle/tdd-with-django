from os import path
import subprocess
from os import environ
THIS_FOLDER = path.dirname(path.abspath(__file__))

def create_session_on_server(host, email):
    user = environ['LIVESERVERUSER']
    return subprocess.check_output(
            [
                'fab',
                'create_session_on_server:email={}'.format(email),
                '--host={}@{}'.format(user,host),
                '--hide=everything,status',
            ],
            cwd=THIS_FOLDER
    ).decode().strip()

def reset_database(host):
    if "www" in host:
        raise RuntimeError("FTs SHOULD NOT BE RUN AGAINST THE PRODUCTION SERVER")
        return
    user = environ['LIVESERVERUSER']
    subprocess.check_call(
            ['fab', 'reset_database', '--host={}@{}'.format(user,host)],
            cwd=THIS_FOLDER
    )

