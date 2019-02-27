from bottle import route, run, response, request
import xmltodict

@route("/scripts/update.php")
def keep_alive():
    response.content_type = 'text/plain; charset=utf-8'
    return "status=0&ka_time=50&allow=0"


@route("/scripts/notify.php", method='POST')
def event_notified():
    raw_body = request.body.read()
    index_value_sent = xmltodict.parse(raw_body)['notify']['index']
    return "hola mundo"

@route('/hello')
def hello():
    return "Hello World!"

run(host='0.0.0.0', port=8080, debug=True)
