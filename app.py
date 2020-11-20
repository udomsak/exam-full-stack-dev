from flask import Flask, request, jsonify
from flask_rq2 import RQ
from flask_cors import CORS
import rq_dashboard
import sys, json
import googlemaps
from pony.flask import Pony
from pony.orm import Database, PrimaryKey, Required
from flask_restful import Resource, Api

DEBUG = True

db = Database()


# this class name not valid for PEP-8 specify
class DOSCG(db.Entity):
    """
    Just sample use concept of ORM by requirement.
    {
        "mode" : Str() Direction routing mode,
        "distance": Str() Store distance text,
        "metrix_value": Int() use to identify cost route,
        "short_path_selected": use to tell client this should to be main route or not.
    }
    """
    _table_ = "map_routing_metrix"
    id = PrimaryKey(int, auto=True)
    mode = Required(str)
    distance = Required(str)
    short_path_selected = Required(int)


'''
For production work should filter or implement access control to end-points 
'''
app = Flask(__name__)
app.config.from_object('config')

# Monitoring config rq-dashboard. use to monitoring task.
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/monitor-queues")

redis_connection_string = app.config['RQ_REDIS_URL']
google_api_key = app.config['GOOGLE_PROJECT_CREDENTIAL_KEY']

if google_api_key is None or google_api_key == "":
    print("Google API key not found in variable please set "
          "GOOGLE_PROJECT_CREDENTIAL_KEY in config.py or OS variable")
    sys.exit(128)

# Init Google-map client.
gmap_client_connect = googlemaps.Client(google_api_key)

# Possible all route options.
possible_route_type = ["driving", "walking", "transit", "bicycling"]

# TODO: This should use placeid instead of use name. ( recommend from Google API doc. )
drive_mode = lambda x: gmap_client_connect. \
    distance_matrix('SCG+สำนักงานใหญ่+บางซื่อ', 'Central+World+(Flagship+store)', mode=x)

# Init flask-restful
api = Api(app)


class MinMapDistance(Resource):
    """"
    Handling RESTFUL for Google-map Distance metrix.
    """
    # lambda filter only need attribute ( distance ).
    distance_matrix = lambda x: x['rows'][0]['elements'][0]['distance']

    def get(self):
        """
        Handling GET Request. payload
        :return json
        """
        distance_matrix = lambda x: x['rows'][0]['elements'][0]['distance']
        payload_possible_route = [(index, drive_mode(index)) for index in possible_route_type]
        distance_metrixs = [(key, distance_matrix(value)) for key, value in
                            json.loads(json.dumps(payload_possible_route)) if
                            value['rows'][0]['elements'][0]['status'] != "ZERO_RESULTS"]
        response = self.restruct_payload(distance_metrixs)
        return response

    def restruct_payload(self, payload):
        """
        Restruct payload for client easy to mapping to Vuetable-2.
        :param payload: List() of distance metrixs
        :return:  List() with dict() contain each of route-weight and mark with MIN() distance.
        """
        minimum_distance = min(payload, key=lambda obj: obj[1]['value'])[0]
        restruct_dict = []
        for item in payload:
            use_direction = "Y" if item[0] == minimum_distance else "N"
            _temp = {
                "mode": item[0],
                "distance": item[1]['text'],
                "metrix_value": item[1]['value'],
                "short_path_selected": use_direction
            }
            restruct_dict.append(_temp)
        return restruct_dict


# eanble CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def hello_world():
    return 'Hello World!'


# Simple REST End-point use to check healthy.
# TODO: Implement with monitoring and PWA for offline browsing.
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong')


def _enum_xyz(slot):
    for element in slot:
        yield element


@app.route('/find-xyz', methods=['POST'])
def find_xyz():
    """
    Use to find element in request
    :return:
    """
    X = request.form['X']
    Y = request.form['Y']
    Z = request.form['Z']
    if X is None and Y is None and Z is None:
        message = "Need X, Y, Z parameter found x={},y={},z={}".format(X, Y, Z)
        app.logger(message)
        return jsonify(message)
    slot_value = [X, Y, 5, 9, 15, 23, Z]
    enum_member = enumerate(_enum_xyz(slot_value))
    temp_store = []
    for idx, elem in enum_member:
        print(idx, elem)
        _temp = {
            "index_postion": idx,
            "element_represent": elem
        }
        temp_store.append(_temp)
    app.logger(temp_store)
    jsonify(json.dumps(temp_store))


# API caching will implement in reverse-proxy instead.
api.add_resource(MinMapDistance, '/map-direction')

if __name__ == '__main__':
    # For scalability use model task-queue for task execution.
    RQ(app)
    # app.run()
