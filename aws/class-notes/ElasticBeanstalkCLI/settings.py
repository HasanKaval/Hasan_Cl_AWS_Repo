import os

# Database connection settings.
#
# We assume that the MySQL engine is being used.
#
# We read the connection settins from environment variables RDS_*.
# Elastic Beanstalk will populate these automatically if you are using
# Beanstalk to create the RDS DB.  If you are creating a DB manually, then
# you need to populate these environment variables yourself.
#
if 'RDS_HOSTNAME' in os.environ:
    DB_HOST = os.environ['RDS_HOSTNAME']
    DB_PORT = int(os.environ['RDS_PORT'])
    DB_USER = os.environ['RDS_USERNAME']
    DB_PASSWD = os.environ['RDS_PASSWORD']
    DB_NAME   = os.environ['RDS_DB_NAME']

# Enable debug only if the FLASK_DEBUG environment variable is set
FLASK_DEBUG = 'false' if os.environ.get('FLASK_DEBUG') is None else os.environ.get('FLASK_DEBUG')

# A unguessable secret key to secure session cookies
SECRET_KEY = "a6f63329aac901501fab1936e1b172e9"
