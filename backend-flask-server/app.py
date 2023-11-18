import time
from flask import Flask, send_file, request

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, Flask!'


# It is good practice to have the API routes namespaced, so that they do not get mixed
# with any possible routes used by the React side. E.g. "/api/time" instead of "/time".
@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/generate', methods=['POST'])
def get_mp4():
    data = request.json
    selected_option = data['option']

    # TODO: Generate and expose mp4, temporary test mp4 for now
    path_to_mp4 = f'./test.mp4'

    try:
        return send_file(path_to_mp4, mimetype='video/mp4')
    except FileNotFoundError:
        return "File not found.", 404

if __name__ == '__main__':
    app.run(debug=True)



# if __name__ == '__main__':
#     app.run(debug=True)