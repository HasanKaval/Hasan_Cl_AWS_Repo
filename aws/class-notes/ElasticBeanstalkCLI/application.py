import flask
import pymysql
from flask import g, render_template, flash, session, request, abort, redirect
from flask import url_for
from beaker.middleware import SessionMiddleware
from flask.sessions import SessionInterface
import os

# Send our logging statements to a custom log file that beanstalk
# will let us snapshot.
#
# Note: the log file must exist and we writable by this application (user: wsgi)
import logging
logging.basicConfig(filename='/opt/python/log/application.log', level=logging.DEBUG)

# Beaker sesion options: store sessions in files in the ./cache directory
# session_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
session_opts = {
    'session.type': 'file',
    'session.data_dir': "./cache",
    'session.cookie_key': 'beaker',
    'session.cookie_expires': True,
    'session.timeout': 60
}

# Adapt beaker interface to Flask sessions
class BeakerSessionInterface(SessionInterface):
    def open_session(self, app, request):
        session = request.environ['beaker.session']
        return session

    def save_session(self, app, session, response):
        session.save()

application = flask.Flask(__name__)
application.config.from_object("settings")
# wrap Flask WSGI application in Beaker session WSGI middleware
application.wsgi_app = SessionMiddleware(application.wsgi_app, session_opts)
application.session_interface = BeakerSessionInterface()

@application.route('/')
def show_entries():
    cursor = g.db.cursor()
    cursor.execute("SELECT title, body, posted_at, posted_by, @@session.time_zone as timezone FROM entries ORDER BY id DESC")
    entries = [dict(title=row[0], text=row[1], posted_at=row[2], posted_by=row[3], timezone=row[4]) for row in cursor.fetchall()]
    return render_template('show_entries.html', entries=entries)

@application.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    cursor = g.db.cursor()
    cursor.execute("INSERT INTO entries (title, body, posted_at, posted_by) VALUES (%s, %s, NOW(), %s)",
        [request.form['title'], request.form['text'],
         session['user']])
    g.db.commit()
    flash("The new entry was successfully posted")
    return redirect(url_for('show_entries'))

@application.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        cursor = g.db.cursor()
        cursor.execute("SELECT id FROM users WHERE name=%s AND password=%s",
            [username, password])
        rs = cursor.fetchall()
        if len(rs) != 1:
            error = "Invalid username or password."
        else:
            session['logged_in'] = True
            session['user'] = username
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@application.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

#
# Create and return a new MySQL connection
#
def connect_db():
    return pymysql.connect(host=application.config['DB_HOST'],
        port=application.config['DB_PORT'],
        user=application.config['DB_USER'],
        passwd=application.config['DB_PASSWD'],
        db=application.config['DB_NAME'])

#
# Automagically create a new DB connection before every request
# and make it available as the per-request 'g.db' object
#
@application.before_request
def before_request():
    g.db = connect_db()

#
# Automagically close the per-request DB connection object, if it exists
#
@application.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# This is useful for testing outside Elastic Beanstalk. The code below is NOT
# executed in a Elastic Beanstalk environment, so don't put anything there
# that is material to the applications functionality.
#
# Note: Elastic Beanstalk looks for an 'application'
# object in 'application.py' and automatically runs it in a WSGI container.
if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
