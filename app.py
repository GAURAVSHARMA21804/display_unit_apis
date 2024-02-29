from flask import Flask,request, abort
from flask_cors import CORS
# from flask_ngrok2 import run_with_ngrok
from model.user_model import user_model
from flask import jsonify
from flask_socketio import SocketIO, emit
# from flask_ngrok2 import run_with_ngrok
from apscheduler.schedulers.background import BackgroundScheduler
from controllers.connection_verifier import ConnectionVerifier
from model.demo_display_model import demo_display_unit_model
import signal, sys
# app = Flask(__name__)

verifier = None

def create_app():
    app = Flask(__name__)
    
    from controllers.demo_display_controller import register_controllers
    register_controllers(app)
    
    return app

# from controllers import demo_display_controller

app = create_app()

CORS(app, origins=["*"], supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')
scheduler = BackgroundScheduler()

# run_with_ngrok(app)
obj1=user_model()


demo_display_unit_model_obj = demo_display_unit_model()
con2 = demo_display_unit_model_obj.get_con2()
# @app.before_first_request
def start_verifier():
    global verifier
    verifier = ConnectionVerifier(con2)
    verifier.start()

# @app.route('/stop_verifier')
# def stop_verifier():
#     global verifier
#     verifier.stopped = True
#     return 'Stopped the verifier'

# @app.teardown_appcontext
# def teardown_app_context(exception):
#     print("####### Close the flask app #######")
#     global verifier
#     if verifier:
#         verifier.stopped = True

def signal_handler(sig, frame):
    # global app_running
    # app_running = False
    global verifier
    if verifier:
        verifier.stopped = True
    print('Flask app stopped manually')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)




@app.route("/")
def welcome():
    con2.close()
    return "avfcHedsalkllo"

@app.route("/home")
def home():
    return "myhokjme"
# WebSocket event handler
latest_result = {"data": None}

@app.route("/work/operator", methods=["POST"])
def update_operator_data():
    try:
        response = obj1.getworkforoperator_model()
        result = response.json
        latest_result["data"] = result
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        print(f"Error in update_operator_data: {e}")
        return jsonify({'status': 'error', 'message': 'Internal Server Error'})

# WebSocket event handler
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Background task for periodic updates
def scheduled_task():
    print("Entering scheduled_task")
    try:
        result = latest_result.get("data")
        print("latest_result:", result)
        if result is not None:
            print("Emitting message to clients")
            socketio.emit('update_work_for_operator', {'data': result})
    except Exception as e:
        print(f"Error in scheduled_task: {e}")



# Start the background task when the server starts
scheduler.add_job(scheduled_task, 'interval', seconds=5)
scheduler.start()

if __name__ == '__main__':
    start_verifier()
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False)
    # app.run(host='0.0.0.0', port=5000)
