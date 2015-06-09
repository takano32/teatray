from . import *
import os, os.path
import ConfigParser
import sys

config = ConfigParser.ConfigParser()
config.read([os.path.expanduser('~/.hypchat'), '/etc/hypchat'])
if config.has_section('HipChat'):
    AUTH_TOKEN = config.get('HipChat', 'token')

elif 'HIPCHAT_TOKEN' in os.environ:
    AUTH_TOKEN = os.environ['HIPCHAT_TOKEN']

else:
    print('Authorization token not detected! The token is pulled from '\
          '~/.hypchat, /etc/hypchat, or the environment variable HIPCHAT_TOKEN.')
    sys.exit(1)

ENDPOINT = None
if config.has_section('HipChat'):
    ENDPOINT = config.get('HipChat', 'endpoint')

elif 'HIPCHAT_ENDPOINT' in os.environ:
    ENDPOINT = os.environ['HIPCHAT_ENDPOINT']

if ENDPOINT:
    hipchat = HypChat(AUTH_TOKEN, ENDPOINT)
else:
    hipchat = HypChat(AUTH_TOKEN)

capabilities = hipchat.capabilities
emoticons = hipchat.emoticons
rooms = hipchat.rooms
users = hipchat.users
endpoint = hipchat.endpoint

try:
    import IPython
    IPython.embed()
except ImportError:
    import code
    code.interact(local=locals())
