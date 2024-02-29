import base64
import json
from app import app
from model.user_model import user_model
from flask import request
obj = user_model()


@app.route("/user/checkapi")
def operator_check_controller():
    return obj.operator_check_model()
            
##OPERATOR LOGIN
@app.route("/user/login", methods=["POST"])
def operator_login_controller():
    return obj.operator_login_model(request.form)
            
##ADMIN LOGIN
@app.route("/user/loginadmin", methods=["POST"])
def operator_loginadmin_controller():
    print("Function Execiting Succefully...")
    return obj.operator_loginadmin_model(request.form)
            
##GETTASK
@app.route("/task/gettask", methods=["POST"])
def operator_gettask_controller():
    return obj.operator_gettask_model(request.form)

##GETFLOOR
@app.route("/floor/getfloor", methods=["POST"])
def floor_controller():
    return obj.floor_model(request.form)


##GETSTATIONS
@app.route("/stations/getstations", methods=["POST"])
def station_controller():
    return obj.station_model(request.form)


##ADDLINE
@app.route("/line/addline", methods=["POST"])
def add_line_controller():
    return obj.add_line_model(request.form)

##GETFLOORPARTS
@app.route("/floor/parts", methods=["POST"])
def get_floor_parts_controller():
    return obj.get_floor_parts_model(request.form)

##GETCHECKSHEET
@app.route("/checksheet", methods=["POST"])
def get_checksheet_controller():
    return obj.get_checksheet_model()

##GETINSTRUCTIONIMAGE
@app.route("/instructionimage", methods=["POST"])
def get_instructionimage_controller():
    return obj.get_instructionimage_model(request.form)

##ADDCHECKSHEETDATA
@app.route("/checksheet/add", methods=["POST"])
def add_checksheetdata_controller():
    return obj.add_checksheetdata_model(request.form)

##GETPROCESSDATA
@app.route("/process/get", methods=["POST"])
def get_oneprocess_controller():
    return obj.get_oneprocess_model(request.form)

##SAVEWORK
@app.route("/work/save", methods=["POST"])
def savework_controller():
    return obj.savework_model(request.form)

##REASON
@app.route("/reason", methods=["POST"])
def reason_controller():
    return obj.reason_model(request.form)


##SAVEWORK
@app.route("/work/get", methods=["POST"])
def getwork_controller():
    return obj.getwork_model(request.form)


##SAVEWORK
# @app.route("/work/getoperator", methods=["POST"])
# def getworkforoperator_controller():
#     return obj.getworkforoperator_model(request.form)



##ADDSTATION
@app.route("/station/add", methods=["POST"])
def add_station_controller():
    return obj.add_station_model(request.json)


##VFT
@app.route("/user/getUsers")
def getAllUser_controller():
    return obj.getAllUsers_model()

@app.route("/user/addone", methods=["POST"])
def addOneUser_controller():
    # print(request.form)
    return obj.addOneUser_model(request.form)

@app.route("/user/updateone", methods=["PUT"])
def updateOneUser_controller():
    # print(request.form)
    return obj.updateOneUser_model(request.form)

@app.route("/user/deleteone/<id>", methods=["DELETE"])
def deleteOneUser_controller(id):
    # print(request.form)
    return obj.deleteOneUser_model(id)


#TabLogin check
@app.route("/user/login/<username>/<tabpassword>/<center>", methods=["GET"])
def verifyUser_controller(username,tabpassword,center):
    # print(request.form)
    return obj.verifyUser_model(username,tabpassword,center)


#PCLogin check
@app.route("/user/loginpc/<username>/<password>/<center>", methods=["GET"])
def verifyUser_controllerpc(username,password,center):
    # print(request.form)
    return obj.verifyUser_modelpc(username,password,center)


#TabLocVerify
@app.route("/authorize/mcenter/<id>/<lat>/<lon>", methods=["GET"])
def verifyCenter(id,lat,lon):
    return obj.verifyCenter_model(id,lat,lon)


#TABCHECKPENDINGTEST
@app.route("/authorize/test/<center>", methods=["GET"])
def checkPendingTest(center):
    return obj.checkPendingTest_model(center)    


#TABCHECKVEHICLE
@app.route("/authorize/vehicle/<id>", methods=["GET"])
def checkVehicle(id):
    return obj.checkVehicle_model(id)    

#TABTESTSTATUS, #PCTESTSTATUS
@app.route("/test/<id>", methods=["GET"])
def checkTest(id):
    return obj.checkTest_model(id)    

#TAB_HEADLAMPTEST_ONE
@app.route("/test/headlamp/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<remark>/<status>", methods=["POST"])
def addHeadlampTest_one(id,p1,p2,p3,p4,p5,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    # img = request_data.get('img', '')
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    # img = "hh"
    # img_bytes = base64.b64decode(img_base64)
    return obj.addHeadlampTest_one_model(id,p1,p2,p3,p4,p5,remark,status,img) 


#TAB_LIGHTTEST_TWO
@app.route("/test/toplight/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<p6>/<remark>/<status>", methods=["POST"])
def addTopLightTest_one(id,p1,p2,p3,p4,p5,p6,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTopLightTest_one_model(id,p1,p2,p3,p4,p5,p6,remark,status,img) 


#TAB_LIGHTTEST_THREE
@app.route("/test/stoplight/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<remark>/<status>", methods=["POST"])
def addStopLightTest_one(id,p1,p2,p3,p4,p5,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addStopLightTest_one_model(id,p1,p2,p3,p4,p5,remark,status,img) 


#TAB_LIGHTTEST_FOUR
@app.route("/test/parkinglight/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<remark>/<status>", methods=["POST"])
def addParkingLightTest_one(id,p1,p2,p3,p4,p5,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addParkingLightTest_one_model(id,p1,p2,p3,p4,p5,remark,status,img) 


#TAB_FOGLIGHTTEST_FIVE
@app.route("/test/foglight/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<remark>/<status>", methods=["POST"])
def addFogLightTest_one(id,p1,p2,p3,p4,p5,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addFogLightTest_one_model(id,p1,p2,p3,p4,p5,remark,status,img) 


#TAB_WARNINGLIGHTTEST_FIVE
@app.route("/test/warninglight/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<remark>/<status>", methods=["POST"])
def addWarningLightTest_one(id,p1,p2,p3,p4,p5,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addWarningLightTest_one_model(id,p1,p2,p3,p4,p5,remark,status,img) 


#TAB_NUMBEPLATELIGHTTEST_FIVE
@app.route("/test/numberplatelight/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<remark>/<status>", methods=["POST"])
def addPlateLightTest_one(id,p1,p2,p3,p4,p5,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addPlateLightTest_one_model(id,p1,p2,p3,p4,p5,remark,status,img) 


#TAB_MARKERLIGHTTEST_FIVE
@app.route("/test/markerlight/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<remark>/<status>", methods=["POST"])
def addMarkerLightTest_one(id,p1,p2,p3,p4,p5,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addMarkerLightTest_one_model(id,p1,p2,p3,p4,p5,remark,status,img) 


#TAB_DIRECTIONLIGHTTEST_FIVE
@app.route("/test/directionlight/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<remark>/<status>", methods=["POST"])
def addDirectionLightTest_one(id,p1,p2,p3,p4,p5,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addDirectionLightTest_one_model(id,p1,p2,p3,p4,p5,remark,status,img) 

#TAB_DIRECTIONLIGHTTEST_FIVE
@app.route("/test/hazardlight/<id>/<p1>/<p2>/<remark>/<status>", methods=["POST"])
def addHazardLightTest_one(id,p1,p2,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addHazardLightTest_one_model(id,p1,p2,remark,status,img) 



#TAB_SUPRESSORTEST_ONE
@app.route("/test/suppressor/<id>/<p1>/<p2>/<p3>/<remark>/<status>", methods=["POST"])
def addSupressorTest_one(id,p1,p2,p3,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addSupressorTest_one_model(id,p1,p2,p3,remark,status,img) 


#TAB_REAR_MIRROR
@app.route("/test/rearmirror/<id>/<p1>/<remark>/<status>", methods=["POST"])
def addRearMirror_one(id,p1,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addRearMirror_model(id,p1,remark,status,img) 





#TAB_SAFETYGLASSTEST_ONE
@app.route("/test/safetyglass/<id>/<p1>/<p2>/<p3>/<remark>/<status>", methods=["POST"])
def addSafetyGlassTest_one(id,p1,p2,p3,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addSafetyGlassTest_one_model(id,p1,p2,p3,remark,status,img) 


#TAB_HORNTEST_ONE
@app.route("/test/horn/<id>/<p1>/<p2>/<p3>/<p4>/<remark>/<status>", methods=["POST"])
def addHornTest_one(id,p1,p2,p3,p4,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addHornTest_one_model(id,p1,p2,p3,p4,remark,status,img) 

#TAB_WIPERBLADETEST_ONE
@app.route("/test/wblade/<id>/<p1>/<p2>/<remark>/<status>", methods=["POST"])
def addwbladeTest_one(id,p1,p2,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addwbladeTest_one_model(id,p1,p2,remark,status,img) 

#TAB_WIPERSYSTEMTEST_ONE
@app.route("/test/wsystem/<id>/<p1>/<p2>/<remark>/<status>", methods=["POST"])
def addwsystemTest_one(id,p1,p2,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addwsystemTest_one_model(id,p1,p2,remark,status,img) 

#TAB_EXHAUSTTEST_ONE
@app.route("/test/exhaust/<id>/<p1>/<p2>/<p3>/<p4>/<remark>/<status>", methods=["POST"])
def addexhaustTest_one(id,p1,p2,p3,p4,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addexhaustTest_one_model(id,p1,p2,p3,p4,remark,status,img) 


#TAB_DASHTEST_ONE
@app.route("/test/dash/<id>/<p1>/<p2>/<p3>/<p4>/<remark>/<status>", methods=["POST"])
def addDashTest_one(id,p1,p2,p3,p4,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addDashTest_one_model(id,p1,p2,p3,p4,remark,status,img) 


#TAB_BRAKING_MANUAL_ONE
@app.route("/test/brakingmanual/<id>/<p1>/<p2>/<p3>/<remark>/<status>", methods=["POST"])
def addTestBraking_one(id,p1,p2,p3,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestBraking_model(id,p1,p2,p3,remark,status,img) 


#TAB_PARKING_BRAKING_MANUAL_ONE
@app.route("/test/parkingbrakingmanual/<id>/<p1>/<p2>/<p3>/<remark>/<status>", methods=["POST"])
def addTestParkingBraking_one(id,p1,p2,p3,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestParkingBraking_model(id,p1,p2,p3,remark,status,img) 


#TAB_STEERING_ONE
@app.route("/test/steering/<id>/<p1>/<remark>/<status>", methods=["POST"])
def addTestSteering_one(id,p1,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestSteering_model(id,p1,remark,status,img) 


#TAB_JOINTPLAY
@app.route("/test/jointplay/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<p6>/<p7>/<p8>/<remark>/<status>", methods=["POST"])
def addTestJointPlay_one(id,p1,p2,p3,p4,p5,p6,p7,p8,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestJointPlay_model(id,p1,p2,p3,p4,p5,p6,p7,p8,remark,status,img) 


#TAB_SPEEDOMETERMANUAL
@app.route("/test/speedometermanual/<id>/<p1>/<p2>/<p3>/<p4>/<remark>/<status>", methods=["POST"])
def addTestSpeedometerManual_one(id,p1,p2,p3,p4,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestSpeedometerManual_model(id,p1,p2,p3,p4,remark,status,img) 


#TAB_LUPD
@app.route("/test/rupd/<id>/<p1>/<p2>/<p3>/<remark>/<status>", methods=["POST"])
def addTestrupd_one(id,p1,p2,p3,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestrupd_model(id,p1,p2,p3,remark,status,img) 

#TAB_RUPD
@app.route("/test/lupd/<id>/<p1>/<p2>/<p3>/<remark>/<status>", methods=["POST"])
def addTestlupd_one(id,p1,p2,p3,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestlupd_model(id,p1,p2,p3,remark,status,img) 


#TAB_FASTAG
@app.route("/test/fastag/<id>/<p1>/<p2>/<remark>/<status>", methods=["POST"])
def addTestfastag_one(id,p1,p2,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestfastag_model(id,p1,p2,remark,status,img) 

#TAB_OTHERS
@app.route("/test/others/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<p6>/<p7>/<p8>/<remark>/<status>", methods=["POST"])
def addTestothers_one(id,p1,p2,p3,p4,p5,p6,p7,p8,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestothers_model(id,p1,p2,p3,p4,p5,p6,p7,p8,remark,status,img) 


#TAB_WHEEL
@app.route("/test/wheel/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<p6>/<remark>/<status>", methods=["POST"])
def addTestWheel_one(id,p1,p2,p3,p4,p5,p6,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestWheel_model(id,p1,p2,p3,p4,p5,p6,remark,status,img) 



#TAB_VLT
@app.route("/test/vlt/<id>/<p1>/<p2>/<remark>/<status>", methods=["POST"])
def addTestVlt_one(id,p1,p2,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestVlt_model(id,p1,p2,remark,status,img) 



#TAB_HSRP
@app.route("/test/hsrp/<id>/<p1>/<p2>/<remark>/<status>", methods=["POST"])
def addTestHsrp_one(id,p1,p2,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestHsrp_model(id,p1,p2,remark,status,img) 


#TAB_BATTERY
@app.route("/test/battery/<id>/<p1>/<p2>/<p3>/<remark>/<status>", methods=["POST"])
def addTestBattery_one(id,p1,p2,p3,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestBattery_model(id,p1,p2,p3,remark,status,img) 

#TAB_SAFETYBELT
@app.route("/test/safetybelt/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<remark>/<status>", methods=["POST"])
def addTestSafetyBelt_one(id,p1,p2,p3,p4,p5,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestSafetyBelt_model(id,p1,p2,p3,p4,p5,remark,status,img) 

#TAB_SPEEDGOVERNER
@app.route("/test/speedgoverner/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<remark>/<status>", methods=["POST"])
def addTestSpeedG_one(id,p1,p2,p3,p4,p5,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestSpeedG_model(id,p1,p2,p3,p4,p5,remark,status,img) 

#TAB_TESTSPRAY
@app.route("/test/spray/<id>/<p1>/<remark>/<status>", methods=["POST"])
def addTestSpray_one(id,p1,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestSpray_model(id,p1,remark,status,img) 

#TAB_TYRES
@app.route("/test/tyres/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<p6>/<remark>/<status>", methods=["POST"])
def addTestTyres_one(id,p1,p2,p3,p4,p5,p6,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)  
    return obj.addTestTyres_model(id,p1,p2,p3,p4,p5,p6,remark,status,img) 

#TAB_RETRO
@app.route("/test/retro/<id>/<p1>/<p2>/<p3>/<p4>/<p5>/<p6>/<p7>/<p8>/<p9>/<remark>/<status>", methods=["POST"])
def addTestRetro_one(id,p1,p2,p3,p4,p5,p6,p7,p8,p9,remark,status):
    request_data = json.loads(request.data)
    print(request_data)
    img = request_data.get('nameValuePairs', {}).get('img', '')
    print(img)
    return obj.addTestRetro_model(id,p1,p2,p3,p4,p5,p6,p7,p8,p9,remark,status,img) 






##############   AUTOMATIC   ###################    
#TAB_BRAKETEST_ONE
@app.route("/test/brake/<id>/<status>", methods=["POST"])
def addBrakeTest_one(id,status):
    # request_data = json.loads(request.data)
    # print(request_data)
    # img = request_data.get('nameValuePairs', {}).get('img', '')
    # print(img)
    return obj.addBrakeTest_one_model(id,status) 


#TAB_COMPLETETEST_ONE
@app.route("/test/mcomplete/<id>/<mstatus>", methods=["POST"])
def addCompleteTest_one(id,mstatus):
    return obj.addCompleteTest_one_model(id,mstatus) 


#PC APIS
#CHECK TEST
@app.route("/test/check/<id>/<center>", methods=["POST"])
def CheckTest_one(id,center):
    return obj.checkTest_one_model(id,center) 

#CHECK TEST DATA
@app.route("/test/checkdata/<id>/<center>", methods=["POST"])
def CheckTestdata_one(id,center):
    return obj.checkTestData_one_model(id,center) 

#CHECK HEADLAMP TEST
@app.route("/test/check/headlamp/<id>", methods=["GET"])
def CheckTest_Headlamp(id):
    return obj.checkTest_headlamp_model(id) 

#CHECK TOP LIGHTS TEST
@app.route("/test/check/toplight/<id>", methods=["GET"])
def CheckTest_Toplight(id):
    return obj.checkTest_toplight_model(id) 

    
#CHECK TOP LIGHTS TEST
@app.route("/test/check/stoplight/<id>", methods=["GET"])
def CheckTest_stoplight(id):
    return obj.checkTest_stoplight_model(id) 


#CHECK TOP LIGHTS TEST
@app.route("/test/check/parkinglight/<id>", methods=["GET"])
def CheckTest_parkinglight(id):
    return obj.checkTest_parkinglight_model(id) 


#CHECK TOP LIGHTS TEST
@app.route("/test/check/foglight/<id>", methods=["GET"])
def CheckTest_foglight(id):
    return obj.checkTest_foglight_model(id) 


#CHECK TOP LIGHTS TEST
@app.route("/test/check/warninglight/<id>", methods=["GET"])
def CheckTest_warninglight(id):
    return obj.checkTest_warninglight_model(id) 


#CHECK TOP LIGHTS TEST
@app.route("/test/check/numberplate/<id>", methods=["GET"])
def CheckTest_numplatelight(id):
    return obj.checkTest_numberplatelight_model(id) 


#CHECK TOP LIGHTS TEST
@app.route("/test/check/markerlight/<id>", methods=["GET"])
def CheckTest_outlinemarkerlight(id):
    return obj.checkTest_outlinemarkerlight_model(id) 


#CHECK TOP LIGHTS TEST
@app.route("/test/check/directionlight/<id>", methods=["GET"])
def CheckTest_directionlight(id):
    return obj.checkTest_directionlight_model(id) 


#CHECK TOP LIGHTS TEST
@app.route("/test/check/hazardlight/<id>", methods=["GET"])
def CheckTest_hazardlight(id):
    return obj.checkTest_hazardlight_model(id) 


#CHECK TOP LIGHTS TEST
@app.route("/test/check/rearmirror/<id>", methods=["GET"])
def CheckTest_rearmirror(id):
    return obj.checkTest_rearmirror_model(id) 

#CHECK SUPRESOR TEST
@app.route("/test/check/Supressor/<id>", methods=["GET"])
def CheckTest_Supressor(id):
    return obj.checkTest_supressor_model(id) 

#CHECK REAR MIRROR TEST
@app.route("/test/check/Rearmirror/<id>", methods=["GET"])
def CheckTest_Rearmirror(id):
    return obj.checkTest_Rearmirror_model(id) 



#CHECK SAFETY GLASSES TEST
@app.route("/test/check/safetyglasses/<id>", methods=["GET"])
def CheckTest_Safetyglasses(id):
    return obj.checkTest_safetyglasses_model(id) 

#CHECK HORN TEST
@app.route("/test/check/horn/<id>", methods=["GET"])
def CheckTest_Horn(id):
    return obj.checkTest_horn_model(id) 

#CHECK EXHAUST TEST
@app.route("/test/check/exhaust/<id>", methods=["GET"])
def CheckTest_Exhaust(id):
    return obj.checkTest_exhaust_model(id) 

#CHECK WIPER BLADE TEST
@app.route("/test/check/wiperblade/<id>", methods=["GET"])
def CheckTest_Wiperblade(id):
    return obj.checkTest_wiperblade_model(id) 

#CHECK WIPER SYSTEM TEST
@app.route("/test/check/wipersystem/<id>", methods=["GET"])
def CheckTest_Wipersystem(id):
    return obj.checkTest_wipersystem_model(id) 

#CHECK DASHBOARD TEST
@app.route("/test/check/dashboard/<id>", methods=["GET"])
def CheckTest_Dashboard(id):
    return obj.checkTest_dashboard_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/brakingmanual/<id>", methods=["GET"])
def CheckTest_Brakingmanual(id):
    return obj.checkTest_Brakingmanual_model(id) 


#CHECK REAR MIRROR TEST
@app.route("/test/check/parkingbrakingmanual/<id>", methods=["GET"])
def CheckTest_Parkingbrakingmanual(id):
    return obj.checkTest_Parkingbrakingmanual_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/steering/<id>", methods=["GET"])
def CheckTest_Steering(id):
    return obj.checkTest_Steering_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/jointplay/<id>", methods=["GET"])
def CheckTest_Jointplay(id):
    return obj.checkTest_jointplay_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/speedometermanual/<id>", methods=["GET"])
def CheckTest_SPM(id):
    return obj.checkTest_Speedometermanual_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/rupd/<id>", methods=["GET"])
def CheckTest_RUPD(id):
    return obj.checkTest_RUPD_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/lupd/<id>", methods=["GET"])
def CheckTest_LUPD(id):
    return obj.checkTest_LUPD_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/fastag/<id>", methods=["GET"])
def CheckTest_Fastag(id):
    return obj.checkTest_Fastag_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/others/<id>", methods=["GET"])
def CheckTest_Others(id):
    return obj.checkTest_Others_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/wheel/<id>", methods=["GET"])
def CheckTest_Wheel(id):
    return obj.checkTest_Wheel_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/vlt/<id>", methods=["GET"])
def CheckTest_Vlt(id):
    return obj.checkTest_Vlt_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/hsrp/<id>", methods=["GET"])
def CheckTest_HSRP(id):
    return obj.checkTest_hsrp_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/battery/<id>", methods=["GET"])
def CheckTest_Battery(id):
    return obj.checkTest_battery_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/safetybelt/<id>", methods=["GET"])
def CheckTest_Safetybelt(id):
    return obj.checkTest_Safetybelt_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/speedgoverner/<id>", methods=["GET"])
def CheckTest_Speedgoverner(id):
    return obj.checkTest_Speedgoverner_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/spray/<id>", methods=["GET"])
def CheckTest_Spray(id):
    return obj.checkTest_Spray_model(id) 


#CHECK DASHBOARD TEST
@app.route("/test/check/tyres/<id>", methods=["GET"])
def CheckTest_Tyres(id):
    return obj.checkTest_tyres_model(id) 

#CHECK DASHBOARD TEST
@app.route("/test/check/retro/<id>", methods=["GET"])
def CheckTest_retro(id):
    return obj.checkTest_retro_model(id) 

#CHECK DASHBOARD TEST
@app.route("/test/getAllData/<id>", methods=["POST"])
def getAllTest(id):
    return obj.getAlltestData(id) 


#ADDTESTDATA
@app.route("/test/add", methods=["POST"])
def addTest_one():
    return  obj.add_test_data_model(request.json)