from flask import Flask, request
from models import User, File, Owner, Base, Session
from sqlalchemy import DateTime
import datetime, json

app = Flask(__name__)


@app.route("/search/<query>")
def search(query):
    session = Session()
    files = session.query(Owner, User, File).filter(Owner.owner == User.id).filter(Owner.fileid == File.id)
    files = files.filter(File.filename.like('%' + query + '%'))
    files = files.filter(User.lastping > datetime.datetime.now() - datetime.timedelta(seconds=30))
    values = []
    for (owner, user, f) in files.all():
        values.append({"path":owner.dirpath, "userip":user.lastip, "port":user.lastport, "hash":f.md5, "filename":f.filename, "size":f.filesize})
    return json.dumps(values)


@app.route("/signin", methods = ["POST"])
def signin():
    if 'username' not in request.form or 'secret' not in request.form or 'openport' not in request.form:
        return "\"POST request must contain 'openport', 'username' and 'secret' fields\""
    session = Session()
    username = request.form['username']
    secret = request.form['secret']
    openport = int(request.form['openport'])
    users = session.query(User).filter(User.id == username).all()
    if (len(users) == 0):
        now = datetime.datetime.now()
        user = User(id=username, secret = secret, lastping = now, lastip=request.remote_addr, lastport = openport)
        session.add(user)
        session.commit()
        session.close()
        return json.dumps("True")
    else:
        if users[0].secret == secret:
            users[0].lastip = request.remote_addr
            users[0].lastport = openport
            users[0].lastping = datetime.datetime.now()
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
    if 'username' not in request.form or 'filename' not in request.form or 'hash' not in request.form or 'size' not in request.form:
        return "\"POST request must contain 'username', 'filename', 'size', and 'hash'.\""
    session = Session()
    username = request.form['username']
    filename = request.form['filename']
    md5 = request.form['hash']
    size = request.form['size']
    files = session.query(File).filter(File.filename == filename).filter(File.md5 == md5)
    files = files.all()
    if len(files) == 0:
        f = File(filename= filename, md5 = md5, filesize = size)
        session.add(f)
        session.commit()
    else:
        f = files[0]
    fileid = f.id
    if 'path' in request.form:
        loc = request.form['path']
    else:
        loc = filename

    print username, filename, md5, loc
    if not session.query(Owner).filter(Owner.owner == username).filter(Owner.dirpath == loc).filter(Owner.fileid == fileid).all():
        session.add(Owner(owner = username, dirpath = loc, fileid = fileid))
    session.commit()
    session.close()
    return json.dumps(True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
