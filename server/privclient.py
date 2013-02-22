from flask import Flask, request
from models.py import User, File, Owner, Base, Session
import datetime

app = Flask(__name__)

@app.route("/search/<query>")
def search(query):
    session = Session()
    files = (session.query(File).filter(File.filename.like('%' + query + '%')).join(Owner).join(User)
            .filter(User.lastping + datetime.timedelta(seconds=30) < datetime.now())
            .add_column(User.lastip).add_column(User.lastport).add_column(Owner.dirpath))
    return json.dumps(files.all())


@app.route("/signin", methods = ["POST"])
def signin():
    if 'username' not in request.form or 'secret' not in request.form or 'openport' not in request.form:
        return "\"POST request must contain 'openport', 'username' and 'secret' fields\""
    session = Session()
    users = session.query(User).filter(User.id == request.form['username']).all()
    if (len(users) == 0):
        session.add(User(id=request.form['username'], secret = request.form['secret'], lastping = datetime.now(),
            lastip=request.remote_addr, lastport = request.form['openport']))
        session.commit()
        session.close()
        return json.dumps(True)
    else:
        if users[0].secret == request.form['secret']:
            users[0].lastip = request.remote_addr
            users[0].lastip = request.form['openport']
            session.add(users[0])
            for ownership in session.query(Owner).filter(Owner.owner = request.form['username']).all():
                session.delete(ownership)
            session.commit()
            session.close()
            return json.dumps(True)
        else:
            return json.dumps(False)

@app.route("/register", methods = ["POST"])
def register():
    if 'username' not in request.form or 'filename' not in request.form or 'hash' not in request.form:
        return "\"POST request must contain 'username', 'filename', and 'hash'.\""
    session = Session()
    username = request.form['username']
    filename = request.form['filename']
    md5 = request.form['hash']
    files = session.query(File).filter(File.filename = filename, File.md5 = md5)
    files = files.all()
    if len(files) == 0:
        session.add(File(filename= filename, md5 = md5))
        session.commit()

    if 'path' in request.form:
        loc = request.form['path']
    else:
        loc = filename
    session.add(Owner(owner = username, dirpath = loc, filename = filename))
    session.commit()
    session.close()
    return json.dumps(True)
