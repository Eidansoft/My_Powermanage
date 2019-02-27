from flask import Flask, Response
import xmltodict

app = Flask(__name__)

@app.route("/scripts/update.php", methods=['GET'])
def keep_alive():
    return Response("status=0&ka_time=50&allow=0", mimetype='text/plain')


@app.route("/scripts/notify.php", methods=['POST'])
def event_notified():
    xmltodict.parse(request.data)['xml']['From']
    return "hola mundo"
