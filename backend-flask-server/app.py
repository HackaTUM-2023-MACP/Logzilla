import time
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, Flask!'


# It is good practice to have the API routes namespaced, so that they do not get mixed
# with any possible routes used by the React side. E.g. "/api/time" instead of "/time".
@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}


# if __name__ == '__main__':
#     app.run(debug=True)