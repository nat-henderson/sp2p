from flask import Flask, request
from models import User, File, Owner, Base, Session
from sqlalchemy import join
import datetime, json

app = Flask(__name__)


@app.route("/search/<query>")
def search(query):
    session = Session()
    files = session.query(File).filter(File.filename.like('%' + query + '%'))
    searchresults = []
    for f in files.distinct().all():
        owners = session.query(Owner).filter(Owner.fileid == f.id)
        for o in owners.distinct().all():
            usable = session.query(User).filter(User.id == o.owner).filter(
                    User.lastping + datetime.timedelta(seconds=30) >= datetime.datetime.now())
            for u in usable.distinct().all():
                searchresults.append({'user' : u.id, 'ip' : u.lastip, 'port' : u.lastport,
                    'filename' : f.filename, 'hash' : f.md5, 'path' : o.dirpath})
    return json.dumps(searchresults)


@app.route("/signin", methods = ["POST"])
def signin():
    if 'username' not in request.form or 'secret' not in request.form or 'openport' not in request.form:
        return "\"POST request must contain 'openport', 'username' and 'secret' fields\""
    session = Session()
    username = request.form['username']
    secret = request.form['secret']
    openport = int(request.form['openport'])
    users = session.query(User).filter(User.id == username).all()
    print users
    if (len(users) == 0):
        print request.remote_addr
        now = datetime.datetime.now()
        user = User(id=username, secret = secret, lastping = now, lastip=request.remote_addr, lastport = openport)
        print user
        session.add(user)
        session.commit()
        session.close()
        return json.dumps("True")
    else:
        if users[0].secret == secret:
            users[0].lastip = request.remote_addr
            users[0].lastport = openport
            session.add(users[0])
            for ownership in session.query(Owner).filter(Owner.owner == username).all():
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
    files = session.query(File).filter(File.filename == filename, File.md5 == md5)
    files = files.all()
    if len(files) == 0:
        f = File(filename= filename, md5 = md5)
        session.add(f)
        session.commit()
    else:
        f = files[0]
    fileid = f.id
    if 'path' in request.form:
        loc = request.form['path']
    else:
        loc = filename
    if not session.query(Owner).filter(Owner.owner == username, Owner.dirpath == loc, Owner.fileid == fileid).all():
        session.add(Owner(owner = username, dirpath = loc, fileid = fileid))
    session.commit()
    session.close()
    return json.dumps(True)

if __name__ == "__main__":
    app.run(debug=True)
