# from app import get_app_instance
# from user_model.user_model import user_model
from model.demo_display_model import demo_display_unit_model
from flask import Flask,request, Blueprint
# obj1=user_model()
obj2=demo_display_unit_model()

# get_app = get_app_instance()


get_app = Blueprint('demo_display_controller', __name__)


def register_controllers(app):
    app.register_blueprint(get_app)




@get_app.route("/user/checkapi/version_two")
def operator_check_controller_version_two():
    return obj2.operator_check_model()
            
##OPERATOR LOGIN
@get_app.route("/user/login/versiontwo", methods=["POST"])
def operator_login_controller_version_two():
    return obj2.operator_login_model(request.form)
            
##ADMIN LOGIN
@get_app.route("/user/loginadmin/version_two", methods=["POST"])
def operator_loginadmin_controller_version_two():
    return obj2.operator_loginadmin_model(request.form)
            
##GETTASK
@get_app.route("/task/gettask/version_two", methods=["POST"])
def operator_gettask_controller_version_two():
    return obj2.operator_gettask_model(request.form)

##GETFLOOR
@get_app.route("/floor/getfloor/version_two", methods=["POST"])
def floor_controller_version_two():
    return obj2.floor_model(request.form)


##GETSTATIONS
@get_app.route("/stations/getstations/version_two", methods=["POST"])
def station_controller_version_two():
    return obj2.station_model(request.form)


##ADDLINE
@get_app.route("/line/addline/version_two", methods=["POST"])
def add_line_controller_version_two():
    return obj2.add_line_model(request.form)

##GETFLOORPARTS
@get_app.route("/floor/parts/version_two", methods=["POST"])
def get_floor_parts_controller_version_two():
    return obj2.get_floor_parts_model(request.form)

##GETCHECKSHEET
@get_app.route("/checksheet/version_two", methods=["POST"])
def get_checksheet_controller_version_two():
    return obj2.get_checksheet_model()

##GETINSTRUCTIONIMAGE
@get_app.route("/instructionimage/version_two", methods=["POST"])
def get_instructionimage_controller_version_two():
    return obj2.get_instructionimage_model(request.form)

##ADDCHECKSHEETDATA
@get_app.route("/checksheet/add/version_two", methods=["POST"])
def add_checksheetdata_controller_version_two():
    return obj2.add_checksheetdata_model(request.form)

##GETPROCESSDATA
@get_app.route("/process/get/version_two", methods=["POST"])
def get_oneprocess_controller_version_two():
    return obj2.get_oneprocess_model(request.form)

##SAVEWORK
@get_app.route("/work/save/version_two", methods=["POST"])
def savework_controller_version_two_two():
    return obj2.savework_model(request.form)

##REASON
@get_app.route("/reason", methods=["POST"])
def reason_controller_version_two():
    return obj2.reason_model(request.form)


##SAVEWORK
@get_app.route("/work/get/version_two", methods=["POST"])
def getwork_controller_version_two():
    return obj2.getwork_model(request.form)


##SAVEWORK
# @app.route("/work/getoperator", methods=["POST"])
# def getworkforoperator_controller():
#     return obj.getworkforoperator_model(request.form)



##ADDSTATION
@get_app.route("/station/add/version_two", methods=["POST"])
def add_station_controller_version_two():
    return obj2.add_station_model(request.json)

@get_app.route("/task_assigned_version_three/version_two",methods=["POST"])
def task_assigned_version_three_controller():
    return obj2.task_assigned_version_three_model(request.json)

@get_app.route("/get/assigned_parts_all/version_two",methods=["POST"])
def get_assigned_parts_all_controller():
    return obj2.get_assigned_parts_all_model()

@get_app.route("/get_taskassigned_all/version_two",methods=["POST"])
def get_taskassigned_all_controller():
    return obj2.get_taskassigned_all_model()


@get_app.route("/stationadd/version_two",methods=["POST"])
def Station_controller_version_two():
    return obj2.Station_model(request.json)

@get_app.route("/getprocess/version_two",methods=["POST"])
def process_controller_version_two():
    return obj2.get_process(request.form)

@get_app.route("/getlogin_process/version_two",methods=["POST"])
def login_process_controller_version_two():
    return obj2.get_process_and_login_data(request.form)

@get_app.route("/task_assigned/version_two",methods=["POST"])
def task_assigned_controller_version_two():
    return obj2.task_assigned_model(request.json)

# @app.route("/get/task_assigned",methods=["POST"])
# def get_task_assigend_model():
#     return obj2.get_task_assigend_model()

@get_app.route("/get/assigend_parts/version_two",methods=["POST"])
def get_assigned_parts_controller_version_two():
    return obj2.get_asssigned_parts_model()

@get_app.route("/get/task_assigned/version_two",methods=["POST"])
def get_task_assigend_model_version_two():
    return obj2.get_task_assigend_model(request.form)

@get_app.route("/update/assigned_parts_stations/version_two",methods=["POST"])
def update_assigned_parts_controller_version_two():
    return obj2.update_assigned_parts_model(request.form)

@get_app.route("/get/task/version_two",methods=["POST"])
def get_task_controller_version_two():
    return obj2.get_task_model()

@get_app.route("/task_assigned_version_two/version_two",methods=["POST"])
def task_assigned_version_two_controller_version_two():
    return obj2.task_assigned_version_two_model(request.json)

@get_app.route("/work/save_version_two/version_two", methods=["POST"])
def savework_controller_version_two_three():
    return obj2.savework_model_version_two(request.form)

@get_app.route('/get_max_station/version_two',methods=['POST'])
def get_max_station_controller_version_two():
    return obj2.get_max_station_model(request.form)



# demo project apis
# no. of lines and per line stations and part_names and part_id for each line api
@get_app.route("/get/line_no_station_no_assigned_parts",methods=["POST"])
def get_line_no_station_no_assigned_parts_controller():
    return obj2.get_line_no_station_no_assigned_parts_model()

#shift timing inserting data
@get_app.route("/add/shift_timings",methods=["POST"])
def add_shift_timings_controller():
    return obj2.add_shift_timings_model(request.json)

#shift timing get data
@get_app.route("/get_shift_timings",methods=["POST"])
def get_shift_timings_controller():
    return obj2.get_shift_timings_model()

@get_app.route("/get/operator/task",methods=["POST"])
def get_operator_task_controller():
    return obj2.get_operator_task_model(request.form)

# task_approved 
@get_app.route("/task/approved",methods=["POST"])
def task_approved_controller():
    return obj2.task_approved_model(request.form)

# get work data from staion_id and date month
@get_app.route("/get/work_f1/version_two", methods=["POST"])
def get_work_f1_controller_version_two():
    return obj2.get_work_f1_model(request.form)
 
@get_app.route("/get_work_f1_date_month/version_two",methods=["POST"])
def get_work_f1_date_month_controller_version_two():
    return obj2.get_work_f1_date_month_model(request.form)

# get stationdata by floor_id
@get_app.route("/get/stations_data/by_floor_id/version_two",methods=["POST"])
def get_stations_data_by_floor_id_version_two():
    return obj2.get_stations_data_by_floor_id_version_two_model(request.form)

# get process data by date month
@get_app.route("/get/process_data/month/date/version__two",methods=["POST"])
def get_process_data_month_date_version_two_controller():
    return obj2.get_process_data_month_date_version_two_model(request.form)

#get checksheetdate by date month
@get_app.route("/get/checksheet_data/month/date/version_two",methods=["POST"])
def get_checksheet_data_month_date_version_two_controller():
    return obj2.get_checksheet_data_month_date_version_two_model(request.form)


# work save new api
@get_app.route("/save/work/update/pass/fail/counter_task_assigned/save/process_data",methods=["POST"])
def save_work_updation_counter_save_process_data_controller():
    return obj2.save_work_updation_counter_save_process_data_model(request.form)

#api for fetch tasl_assigned accordingt to task_id
@get_app.route("/get/task_for_app/version_two",methods=["POST"])
def get_task_for_app_version_two_controller():
    return obj2.get_task_for_app_version_two_model(request.form)

# api for fetch process_data reading
@get_app.route("/get/process_data_readings_timestamps/version_two",methods=["POST"])
def get_processs_data_readings_timestamps_controller():
    return obj2.get_process_data_readings_timestamp_model(request.form)

#work_f1 data and process_data according to date month 
@get_app.route("/get/work_data/process_data/version_two",methods=["POST"])
def get_work_data_process_data_version_two_controller():
    return obj2.get_work_data_process_data_version_two_model(request.form)

@get_app.route("/save/readings/version_two",methods=["POST"])
def save_readings_version_two_controller():
    return obj2.save_readings_version_two_model(request.form)

#fetch readings
@get_app.route("/get/readings_data/version_two",methods=["POST"])
def get_readings_data_version_two_controller():
    return obj2.get_readings_data_version_two_model(request.form)

@get_app.route("/get/readings_by_date_month/version_two",methods=["POST"])
def get_readings_by_date_month_version_two_controller():
    return obj2.get_readings_by_date_month_version_model(request.form)
