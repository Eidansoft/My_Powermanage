from flask import Flask, Response

app = Flask(__name__)

@app.route("/scripts/update.php")
def keep_alive():
    return Response("status=0&ka_time=50&allow=0", mimetype='text/plain')


@app.route("/")
def test():
    return "hola mundo"
