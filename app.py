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

class FindBandCValue(Resource):
    def find_bc(self, A=21, result=-21):
        """
        Simple calculation finding / magic number.
        If A = 21, A + B = 23, A + C = -21 - Please create a new function for finding B and C value.

        In case you want to find ALL possible value use range combine with Set() and iterate to finding number.
        If you want to use Lexical parser may be use PLY (Python Lex-Yacc).

        :param A: Is fix value (a detail above) default is 21
        :param result: Is fix value (a detail above) default is -21
        :return:
        """
        # check negative number
        if result < 0:
            C = -(A + abs(-result))
            find_bc_response = {
                "A": A,
                "B": C,
                "result": result,
                "text": "If A = {}, A + {} = -21".format(A, C)
            }
            return C
        if result > 0:
            B = result - A
            find_bc_response = {
                "A": A,
                "B": B,
                "result": result,
                "text": "If A = {}, A + {} = 23".format(A, B)
            }
            return B
        return None

    def get(self):
        """
        Simple calculation finding / magic number.
        If A = 21, A + B = 23, A + C = -21 - Please create a new function for finding B and C value.

        :return: Jsonify
        """
        message = "A = 21, A + {} = 23, A + {} = -21 ".format(self.find_bc(21, 23), self.find_bc(21, -21))
        return jsonify(
            {'A': 21,
             'B': self.find_bc(21, 23),
             'C': self.find_bc(21, -21),
             'result': message })

class FindXYZ(Resource):
    def get(self):
        """
         X, Y, 5, 9, 15, 23, Z - Please create a new function for finding X, Y, Z value.
         https://github.com/udomsak/exam-full-stack-dev
        :return:
        """
        X = 'X'
        Y = 'Y'
        Z = 'Z'

        response = self.idx_poisiton_find(X=X, Y=Y, Z=Z)
        return jsonify(response)

    def idx_poisiton_find(self, X,Y,Z):
        """
        Finding element index in List()
        :param X: x element want to find.
        :param Y: y element want to find.
        :param Z: z element want to find.
        :return: jsonify object with result descripe:
        [{"element_represent":"X","index_postion":0},{"element_represent":"Y","index_postion":1},
        {"element_represent":"Z","index_postion":6}]
        """
        slot_value = [X, Y, 5, 9, 15, 23, Z]
        enum_member = [filter for filter in enumerate(slot_value)
                       if 'X' in filter or 'Y' in filter or 'Z' in filter]
        temp_store = []
        for idx, elem in enum_member:
            _temp = {
                "index_postion": idx,
                "element_represent": elem
            }
            temp_store.append(_temp)
        response = temp_store
        return response
    def post(self):
        pass

# if X is None and Y is None and Z is None:
#     message = "Need X, Y, Z parameter found x={},y={},z={}".format(X, Y, Z)
#     return jsonify(message)

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

# API caching will implement in reverse-proxy instead.
api.add_resource(MinMapDistance, '/map-direction')
api.add_resource(FindBandCValue, '/find-bc')
api.add_resource(FindXYZ, '/find-xyz')

if __name__ == '__main__':
    # For scalability use model task-queue for task execution.
    RQ(app)
    # app.run()
