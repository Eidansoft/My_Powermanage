from bottle import route, run, response, request
import xmltodict

@route("/scripts/update.php")
def keep_alive():
    response.content_type = 'text/plain; charset=utf-8'
    log(request)
    return "status=0&ka_time=50&allow=0"


@route("/scripts/notify.php", method='POST')
def event_notified():
    raw_body = request.body.read().decode('utf-8')
    index_value_sent = xmltodict.parse(raw_body)['notify']['index']
    response.content_type = 'text/xml;charset=utf-8'
    log(request)
    return "<?xml version '1.0'?> <index>{}</index>".format(index_value_sent)


# @route('/hello')
@route("/<url:re:.+>")
def hello(url):
    print("CAPTURADA GENERICA A: {}".format(url))
    log(request)
    return "Hello World!"


def log(request):
    result = {
        'method': request.method,
        'headers': dict(request.headers),
        'body': request.body.read().decode('utf-8'),
        'files': [
            {'key': key, 'name': request.files[key].raw_filename}
            for key in request.files
        ]
    }
    print('#################################')
    print(result)
    print('#################################')

run(host='0.0.0.0', port=8080, debug=True)
