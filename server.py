import simplejson
import urllib
import datetime
import calendar
import time
import flask

app = flask.Flask(__name__, static_url_path='')

API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"

@app.route("/", methods=['GET'])
def index():
    return flask.redirect('/index.html')

@app.route("/api/", methods=['GET'])
def api():
    f = urllib.urlopen("http://realtime.mbta.com/developer/api/v2/predictionsbystop?api_key=%s&stop=68&format=json" % API_KEY)
    data = simplejson.loads(f.read())
    f.close()

    json = simplejson.dumps([int(t['pre_away']) for t in data['mode'][0]['route'][0]['direction'][0]['trip']])
    return flask.Response(json, mimetype='application/json')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
