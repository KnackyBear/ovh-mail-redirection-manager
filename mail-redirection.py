from configparser import Error
import json
import ovh
import sys
from getopt import GetoptError, gnu_getopt
from decouple import config
from ovh.exceptions import ResourceConflictError


###############################################################################
# Variables
###############################################################################

# Your domain
domain = config("DOMAIN")

# Authorized arguments
AUTHORIZED_ARGS = ["list", "add", "remove"]

# Instanciate an OVH Client.
# You can generate new credentials with full access to your account on
# the token creation page
client = ovh.Client(
    # Endpoint of API OVH Europe (List of available endpoints)
    endpoint=config("OVH_END_POINT"),
    # Application Key
    application_key=config("OVH_APPLICATION_KEY"),
    # Application Secret
    application_secret=config("OVH_APPLICATION_SECRET"),
    # Consumer Key
    consumer_key=config("OVH_CONSUMER_KEY"),
)

###############################################################################
# Functions
###############################################################################


def syntax():
    print(
        "Syntax : %s list|add|remove [--from <mail>] [--to <mail>]" % sys.argv[0])
    sys.exit


def list_redirections(mail_from='', mail_to=''):
    # Get all IDs
    ids = client.get('/email/domain/%s/redirection' % domain, _from=mail_from, to=mail_to)
    for id in ids:
        # Get details for each Id.
        redirection = client.get(_target='/email/domain/%s/redirection/%s' % (domain, id))
        print("%-50s %s" % (redirection['from'], redirection['to']))
    return

def add_redirection(mail_from='', mail_to=''):
    try:
        redirection = client.post(_target='/email/domain/%s/redirection' % domain, _from=mail_from, to=mail_to, localCopy=False)
        print(json.dumps(redirection, indent=4))
    except ResourceConflictError as err:
        print(err)
    return

def remove_redirection(mail_from=''):
    ids = client.get('/email/domain/%s/redirection' % domain, _from=mail_from)
    for id in ids:
        redirection = client.delete(_target='/email/domain/%s/redirection/%s' % (domain, id))
        print(json.dumps(redirection, indent=4))
    return


###############################################################################
# Main
###############################################################################


# Options and arguments manage
try:
    options, args = gnu_getopt(sys.argv[1:], '', ['from=', 'to='])
    opt_from, opt_to = '', ''
    for k, v in options:
        if k == '--from':
            opt_from = v
        elif k == '--to':
            opt_to = v

    # only one argument
    if len(args) > 1 or len([_ for arg in args if arg not in AUTHORIZED_ARGS]) > 0:
        syntax()

    if len(args) > 0:
        if args[0] == AUTHORIZED_ARGS[0]:
            list_redirections(opt_from, opt_to)
        elif args[0] == AUTHORIZED_ARGS[1]:
            add_redirection(opt_from, opt_to)
        elif args[0] == AUTHORIZED_ARGS[2]:
            remove_redirection(opt_from)
except GetoptError as err:
    print(err)
    syntax()