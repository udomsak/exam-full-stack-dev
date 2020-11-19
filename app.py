from flask import Flask, request
from flask_rq2 import RQ
import rq_dashboard

'''
For production work should filter or implement access control to end-points 
'''
app = Flask(__name__)

app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/monitor-queues")


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    RQ(app)
    # app.run()
