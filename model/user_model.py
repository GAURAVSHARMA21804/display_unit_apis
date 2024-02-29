from datetime import datetime
from io import BytesIO
import time
from tkinter import Image
import traceback
import mysql.connector
import base64
import json
import os
from flask import jsonify, make_response, request
import pytz
class user_model():
    def __init__(self):
        try:
            # self.con =  mysql.connector.connect(host="localhost",user="root",password="Hello123##",database="vft_app")
            # self.con.autocommit = True
            # self.con._connection_timeout = 60
            # self.cur = self.con.cursor(dictionary=True)
            self.con2 =  mysql.connector.connect(host="localhost",user="root",password="Hello123##",database="dunitv2")
            self.con2.autocommit = True
            self.con2._connection_timeout = 60
            self.cur2 = self.con2.cursor(dictionary=True)
            print("success")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.CR_SERVER_LOST:
                print("Server connection lost. Reconnecting...")
                self.con.reconnect()
                time.sleep(50)
            else:
                print(f"Error: {err}")


###############check API
    def operator_check_model(self):
        with self.con2.cursor(dictionary=True) as cur2:
            if not self.con2.is_connected():
                self.con2.reconnect()

            cur2.execute("SELECT * from login_operator")
            result = cur2.fetchall()

            if len(result)>0:
            # return json.dumps(result)
            # return{"payload": result}
                res = make_response({"payload": result},200)
                res.headers['Access-Control-Allow-Origin'] = "*"
                return res
            else:
            # return {"message":"No Data Found"}
                return make_response({"message":"No Data Found"},204)
             # message is not shown for 204    

###########################   LOGIN API   ##########3################
    def operator_login_model(self,data):
        try:
            employee_code = data.get('employee_code')
            password = data.get('password')

            # Construct and execute the query
            query = f"SELECT * FROM login_operator WHERE employee_code = '{employee_code}' AND password = '{password}'"
            
            with self.con2.cursor(dictionary=True) as cur2:
                if not self.con2.is_connected():
                    self.con2.reconnect()
            
                cur2.execute(query)
                result = cur2.fetchone()
                cur2.nextset()


                if result is not None:
                    # return json.dumps(result)
                # return{"payload": result}
                    res = make_response({"logindata": result},200)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                else:
                # return {"message":"No Data Found"}
                    print("good")
                    res = make_response({"logindata":"No Data Found"},401)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                # message is not shown for 204    
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            res =  make_response({"logindata":"Got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'
            return res




###########################   GET TASK API   ##########################
    def operator_gettask_model(self,data):
        try:
            station_id = data.get('station_id')
            split_items = station_id.split()
            # print(split_items)
            if len(split_items) == 3:
                F1, L1, S1 = split_items

                # Further split each part
                F1_part1, F1_part2 = F1[0], F1[1:]
                L1_part1, L1_part2 = L1[0], L1[1:]
                S1_part1, S1_part2 = S1[0], S1[1:]

                # print("F1:", F1_part1, F1_part2)
                # print("L1:", L1_part1, L1_part2)
                # print("S1:", S1_part1, S1_part2)

                query = f"SELECT * FROM task_assigned WHERE line_id = '{L1_part2}' AND floor_id = '{F1_part2}'"
                
                with self.con2.cursor(dictionary=True) as cur2:
                    if not self.con2.is_connected():
                        self.con2.reconnect()
                    
                    cur2.execute(query)
                    result = cur2.fetchone()
                    cur2.nextset()

                    if result is not None:
                        res = make_response({"taskdata": result},200)
                        res.headers['Access-Control-Allow-Origin'] = "*"
                        res.headers['Content-Type'] = 'application/json'
                        return res
                    else:
                        print("good")
                        res = make_response({"taskdata":"No task assigned"},201)
                        res.headers['Access-Control-Allow-Origin'] = "*"
                        res.headers['Content-Type'] = 'application/json'
                        return res
                     
            else:
                res = make_response({"taskdata": "Invalid Station ID"},202)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res 
        except:
            traceback.print_exc()
            res = make_response({"taskdata":"Got error"},203)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'
            return res



###########################   LOGIN ADMIN API   ##########################
    def operator_loginadmin_model(self,data):
        try:
            employee_code = data.get('employee_code')
            password = data.get('password')

            # Construct and execute the query
            query = f"SELECT * FROM login_admin WHERE employee_code = '{employee_code}' AND password = '{password}'"
            
            with self.con2.cursor(dictionary=True) as cur2:
                if not self.con2.is_connected():
                    self.con2.reconnect()

                cur2.execute(query)
                result = cur2.fetchone()
                cur2.nextset()


                if result is not None:
                    # return json.dumps(result)
                    # return{"payload": result}
                    res = make_response({"logindata": result},200)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                else:
                    # return {"message":"No Data Found"}
                    print("good")
                    res = make_response({"logindata":"No Data Found"},401)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                    # message is not shown for 204    
        except Exception as e:
            print(e)
            traceback.print_exc()
            res = make_response({"logindata":"Got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'
            return res

###########################   GET FLOOR DETAILS API   ##########################
    def floor_model(self,data):
        try:
            floor_id = data.get('floor_id')
        
            # Construct and execute the query
            query = f"SELECT * FROM floors WHERE floor_id = '{floor_id}'"

            with self.con2.cursor(dictionary=True) as cur2:

                if not self.con2.is_connected():
                    self.con2.reconnect()

                cur2.execute(query)
                result = cur2.fetchone()
                cur2.nextset()

                if result is not None:
                    # return json.dumps(result)
                    # return{"payload": result}
                    res = make_response({"floordata": result},200)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                else:
                    # return {"message":"No Data Found"}
                    print("good")
                    res = make_response({"floordata":"No Data Found"},401)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                    # message is not shown for 204    
        except Exception as e:
            print(e)
            traceback.print_exc()
            res = make_response({"floordata":"Got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'
            return res



###########################   GET STATIONS DETAILS API   ##########################
    def station_model(self,data):
        try:
            floor_id = data.get('floor_id')
            # Construct and execute the query
            query = f"SELECT * FROM stations"
            with self.con2.cursor(dictionary=True) as cur2:
                if not self.con2.is_connected():
                    self.con2.reconnect()
                cur2.execute(query)
                result = cur2.fetchall()
                print(result)

                if result is not None:
                    transformed_data = []
                    for row in result:
                        floor_num, line_num, station_num = row['station_id'].split(' ')
                        transformed_row = {
                            'station_id': row['station_id'],
                            'floor_num': int(floor_num[1:]),  # Extract numeric part and convert to int
                            'line_num': int(line_num[1:]),
                            'station_num': int(station_num[1:]),
                            'e_one': row['e_one'],
                            'e_one_name': row['e_one_name'],
                            'e_one_skill': row['e_one_skill'],
                            'e_two': row['e_two'],
                            'e_two_name': row['e_two_name'],
                            'e_two_skill': row['e_two_skill'],
                            'process_id': row['process_id'],
                            'process_name': row['process_name'],
                            'process_skill': row['process_skill']
                        }

                        # print(floor_id)
                        print(transformed_row.get('station_num'))
                        if str(int(floor_num[1:])) == str(floor_id):
                            transformed_data.append(transformed_row)

                    # Return the transformed data in JSON format
                    print(transformed_data)
                    response = make_response(jsonify({'stationdata': transformed_data}), 200)
                    response.headers['Access-Control-Allow-Origin'] = "*"
                    response.headers['Content-Type'] = 'application/json'
                    return response
                else:
                    # return {"message":"No Data Found"}
                    print("good")
                    res = make_response({"stationdata":"No Data Found"},401)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                # message is not shown for 204    
        except Exception as e:
            print(e)
            print(f"An error occurred: {e}")
            traceback.print_exc()
            res = make_response({"stationdata":"got error"},401)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'
            return res

###########################   ADD LINE API   ##########################
    def add_line_model(self,data):
        try:
            floor_id = data.get('floor_id')
            part_id = data.get('part_id')
            part_name = data.get('part_name')
            # Construct and execute the query
            query = f"SELECT number_of_lines FROM floors WHERE floor_id = '{floor_id}'"
            with self.con2.cursor(dictionary=True) as cur2:
                if not self.con2.is_connected():
                    self.con2.reconnect()
        
                cur2.execute(query)
                result = cur2.fetchone()
                cur2.nextset()
           
                if result is not None:
                    number_of_lines = int(result.get('number_of_lines', 0))
                    a = "Vivo_PCB_x48"
                    b = "1"
                    c = number_of_lines + 1
                    # print(result)
                    # print(number_of_lines)
                    self.con2.start_transaction()
                    query_update = f"UPDATE floors SET number_of_lines = '{number_of_lines}' + 1 WHERE floor_id = '{floor_id}'"
                    cur2.execute(query_update)
                    query = "INSERT INTO assigned_parts (line_id, part_id, part_name) VALUES (%s, %s, %s)"
                    values = (c, part_id,part_name)
                    cur2.execute(query,values)
                    result = cur2.fetchall()
                    self.con2.commit()
                    if cur2.rowcount > 0:          

                        res = make_response({"floordata":"Added"},200)
                        res.headers['Access-Control-Allow-Origin'] = "*"
                        res.headers['Content-Type'] = 'application/json'
                        return res
                    
                    else:
                        print("not good")
                        self.con2.rollback()
                        res = make_response({"floordata":"No Data Found"},201)
                        res.headers['Access-Control-Allow-Origin'] = "*"
                        res.headers['Content-Type'] = 'application/json'
                        return res
                else:
                    # return {"message":"No Data Found"}
                    print("good")
                    res = make_response({"floordata":"No Data Found"},201)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                # message is not shown for 204    
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.con2.rollback()
            res = make_response({"floordata":"got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'
            return res


###########################   GET FLOOR PARTS API   ##########################
    def get_floor_parts_model(self,data):
        try:
            floor_id = data.get('floor_id')
            # Construct and execute the query
            query = f"SELECT * FROM parts WHERE floor_id = '{floor_id}'"
            with self.con2.cursor(dictionary=True) as cur2:
                if not self.con2.is_connected():
                    self.con2.reconnect()

                cur2.execute(query)
                result = cur2.fetchall()
            
                if result is not None:
                
                    res = make_response({"floorpartsdata": result},200)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                else:
                    # return {"message":"No Data Found"}
                    print("good")
                    res = make_response({"floorpartsdata":"No Data Found"},201)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                # message is not shown for 204    
        except Exception as e:
            traceback.print_exc()
            res = make_response({"floorpartsdata":"got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'
            return res

###########################   GET CHECKSHEET API   ##########################
    def get_checksheet_model(self):
        try:
            # Construct and execute the query
            query = f"SELECT * FROM checksheet"
            with self.con2.cursor(dictionary=True) as cur2:
                if not self.con2.is_connected():
                    self.con2.reconnect()
        
                cur2.execute(query)
                result = cur2.fetchall()
           
                if result is not None:
                    res = make_response({"checksheet": result},200)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                else:
                    # return {"message":"No Data Found"}
                    print("good")
                    res = make_response({"checksheet":"No Data Found"},201)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                # message is not shown for 204    
        except:
            res = make_response({"checksheet":"got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'            

 
###########################   GET INSTRUCTION API   ##########################
    def get_instructionimage_model(self,data):
        try:
            station_id = data.get('station_id')
            query = f"SELECT process_id FROM stations WHERE station_id = '{station_id}'"
            with self.con2.cursor(dictionary=True) as cur2:
                if not self.con2.is_connected():
                    self.con2.reconnect()
        
                self.cur2.execute(query)
                result = self.cur2.fetchone()
                cur2.nextset()

           
                if result is not None:
                    process_id = int(result.get('process_id', 0))
                    query = f"SELECT * FROM processes WHERE process_id = '{process_id}'"
                    cur2.execute(query)
                    result = cur2.fetchone()
                    cur2.nextset()


                    if result is not None:
                        res = make_response({"instructionImage": result},200)
                        res.headers['Access-Control-Allow-Origin'] = "*"
                        res.headers['Content-Type'] = 'application/json'
                        return res
                    else:
                        print("not good")
                        res = make_response({"instructionImage":"No Data Found"},201)
                        res.headers['Access-Control-Allow-Origin'] = "*"
                        res.headers['Content-Type'] = 'application/json'
                        return res

                else:
                    # return {"message":"No Data Found"}
                    print("good")
                    res = make_response({"instructionImage":"No Data Found"},201)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                    # message is not shown for 204    
        except:
            res = make_response({"instructionImage":"got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'            



###########################   ADD CHECKSHEET DATA API   ##########################
    def add_checksheetdata_model(self,data):
        try:

            indian_timezone = pytz.timezone('Asia/Kolkata')

# Get the current time in UTC
            current_time_utc = datetime.utcnow()

# Convert UTC time to Indian time
            current_time_indian = current_time_utc.replace(tzinfo=pytz.utc).astimezone(indian_timezone)

# Print the formatted Indian time
            formatted_time = current_time_indian.strftime("%A, %B %d, %Y %H:%M:%S")
            print(formatted_time)

            # Format the datetime object as a string
            # formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            # print(formatted_time)
            
            # return "A"
        
            station_id = data.get('station_id')
            employee_id = data.get('employee_id')
            employee_name = data.get('employee_name')
            timestamp = str(formatted_time)
            p1 = data.get('p1')
            p2 = data.get('p2')
            p3 = data.get('p3')
            p4 = data.get('p4')
            p5 = data.get('p5')
            p6 = data.get('p6')
            p7 = data.get('p7')
            p8 = data.get('p8')
            p9 = data.get('p9')
            p10 = data.get('p10')
            # Construct and execute the query
            # query = f"INSERT INTO checksheet_data (station_id, employee_id, employee_name, timestamp, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10) VALUES ({station_id}, {employee_id}, {employee_name}, {timestamp}, {p1}, {p2}, {p3}, {p4}, {p5}, {p6}, {p7}, {p8}, {p9}, {p10})"
            # query = f""
            query = "INSERT INTO checksheet_data (station_id, employee_id, employee_name, timestamp, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (station_id, employee_id, employee_name, timestamp, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10)
            with self.con2.cursor(dictionary=True) as cur2:
                if not self.con2.is_connected():
                    self.con2.reconnect()

                cur2.execute(query, values)
                # self.cur2.execute(query)
                result = cur2.fetchall()
            
                if result is not None:
                    res = make_response({"checksheetadd": "added"},200)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                else:
                    # return {"message":"No Data Found"}
                    print("good")
                    res = make_response({"checksheetadd":"No Data Found"},201)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                    # message is not shown for 204    
        except Exception as e:
            print(e)
            res = make_response({"checksheetadd":"got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'  
            return res



###########################   GET PROCESS DATA API   ##########################
    def get_oneprocess_model(self,data):
        try:
            station_id = data.get('station_id')
            # Construct and execute the query
            query = f"SELECT * FROM stations WHERE station_id = '{station_id}'"
            with self.con2.cursor(dictionary=True) as cur2:
                if not self.con2.is_connected():
                    self.con2.reconnect()
        
                self.cur2.execute(query)
                result = self.cur2.fetchone()
                cur2.nextset()

                # print("start")
           
                if result is not None:
                    process_id = int(result.get('process_id', 0))
                    query = f"SELECT * FROM processes WHERE process_id = '{process_id}'"
                    cur2.execute(query)
                    result = cur2.fetchone()
                    cur2.nextset()

                    # print("not null 1")

                    if result is not None:
                        res = make_response({"processdata": result},200)
                        res.headers['Access-Control-Allow-Origin'] = "*"
                        res.headers['Content-Type'] = 'application/json'
                        return res
                    else:
                        # print("not good")
                        res = make_response({"processdata":"No Data Found"},201)
                        res.headers['Access-Control-Allow-Origin'] = "*"
                        res.headers['Content-Type'] = 'application/json'
                        return res
 
                else:
                    # return {"message":"No Data Found"}
                    # print("good")
                    res = make_response({"processdata":"No Data Found"},201)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                    # message is not shown for 204    
        except Exception as e:
            print(e)
            res = make_response({"processdata":"got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'            
            return res
            


###########################   SAVE WORK DATA API   ##########################
    def savework_model(self,data):
        try:

            indian_timezone = pytz.timezone('Asia/Kolkata')
            # Get the current time in UTC
            current_time_utc = datetime.utcnow()
            # Convert UTC time to Indian time
            current_time_indian = current_time_utc.replace(tzinfo=pytz.utc).astimezone(indian_timezone)
            # Print the formatted Indian time
            formatted_time = current_time_indian.strftime("%A, %B %d, %Y %H:%M:%S")
            # Format the datetime object as a string
            # formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            print(formatted_time)

            month = data.get('month')
            date = data.get('date')
            station_id = data.get('station_id')
            process_id = data.get('process_id')
            part_id = data.get('part_id')
            timestamp = formatted_time
            floor_id = data.get('floor_id')
            line_id = data.get('line_id')
            status = data.get('status')
            reason = data.get('reason')
            remark = data.get('remark')
            isfilled = data.get('isfilled')
            
            p1 = data.get('p1')
            p2 = data.get('p2')
            p3 = data.get('p3')
            p4 = data.get('p4')
            p5 = data.get('p5')

            # EXECUTE TRANSACTION
            self.con2.start_transaction()
            
            # Construct and execute the query
            # query = f"INSERT INTO work_f1 (station_id, process_id, part_id, timestamp, floor_id, line_id, status, reason, remark, isfilled) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            query = "INSERT INTO work_f1 (station_id, process_id, part_id, timestamp, floor_id, line_id, status, reason, remark, isfilled) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (station_id, process_id, part_id, timestamp, floor_id, line_id, status, reason, remark, isfilled)
            with self.con2.cursor(dictionary=True) as cur2:
                if not self.con2.is_connected():
                    self.con2.reconnect()
       
                cur2.execute(query,values)
                #Execute another query
                


                result = cur2.fetchone()

                # print("start")
                # print(result)
                if cur2.rowcount > 0:
                    cur2.nextset()
                    if isfilled == "0":
                        self.con2.commit()
                        if result is not None:

                            myIsFilled = 0
                            myPass = 0
                            myFail = 0
                            mCount = 0

                            for entry in result:
                                mStation_id = entry["station_id"]
                                if(mStation_id == station_id):
                                    mIsFilled = entry["isfilled"]
                                    # floor_id = entry["floor_id"]
                                    # line_id = entry["line_id"]
                                    mStatus = entry["status"]
                                    mCount = mCount + 1
                                
                                    if(mIsFilled == "1"):
                                        myIsFilled = myIsFilled + 1
                                    if(mStatus == "1"):
                                        myPass = myPass + 1
                                    else:
                                        myFail = myFail + 1  

                            # Create a dictionary with the variables
                            response_dict = {
                                "myIsFilled": myIsFilled,
                                "myPass": myPass,
                                "myFail": myFail,
                                "mCount": mCount
                            }

                            # Use make_response and jsonify to create a response with the desired structure
                            res = make_response(jsonify({"workdata": response_dict}), 200)  
                            res.headers['Access-Control-Allow-Origin'] = "*"
                            res.headers['Content-Type'] = 'application/json'
                            return res
                
                    query =  "INSERT INTO process_data (process_id, station_id, timestamp, p1, p2, p3, p4, p5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (process_id, station_id, timestamp, p1, p2, p3, p4, p5)
                    cur2.execute(query, values)
                
                    result = cur2.fetchone()

                    # print("not null 1")

                    if cur2.rowcount > 0:
                        cur2.nextset()

                        query = f"SELECT * FROM work_f1 WHERE MONTH(STR_TO_DATE(timestamp, '%W, %M %d, %Y %H:%i:%s')) = '{month}' AND DAY(STR_TO_DATE(timestamp, '%W, %M %d, %Y %H:%i:%s')) = '{date}'"
                        cur2.execute(query)
                        result = cur2.fetchall()
                        self.con2.commit()

                        if result is not None:

                            myIsFilled = 0
                            myPass = 0
                            myFail = 0
                            mCount = 0

                            for entry in result:
                                mStation_id = entry["station_id"]
                                if(mStation_id == station_id):
                                    mIsFilled = entry["isfilled"]
                                    # floor_id = entry["floor_id"]
                                    # line_id = entry["line_id"]
                                    mStatus = entry["status"]
                                    mCount = mCount + 1
                                
                                    if(mIsFilled == "1"):
                                        myIsFilled = myIsFilled + 1
                                    if(mStatus == "1"):
                                        myPass = myPass + 1
                                    else:
                                        myFail = myFail + 1  

                        # Create a dictionary with the variables
                            response_dict = {
                                "myIsFilled": myIsFilled,
                                "myPass": myPass,
                                "myFail": myFail,
                                "mCount": mCount
                            }

                            # Use make_response and jsonify to create a response with the desired structure
                            res = make_response(jsonify({"workdata": response_dict}), 200)            
                            # res = make_response({"workdata": result},200)
                            res.headers['Access-Control-Allow-Origin'] = "*"
                            res.headers['Content-Type'] = 'application/json'
                            return res   

                        else:
                            self.con2.rollback()
                            res = make_response({"workdata":"Cannot fetch 3"},201)
                            res.headers['Access-Control-Allow-Origin'] = "*"
                            res.headers['Content-Type'] = 'application/json'
                            return res 

 
                    else:
                        # print("not good")
                        cur2.nextset()
                        self.con2.rollback()
                        res = make_response({"workdata":"Cannot add 2"},201)
                        res.headers['Access-Control-Allow-Origin'] = "*"
                        res.headers['Content-Type'] = 'application/json'
                        return res
                
                else:
                    # return {"message":"No Data Found"}
                    # print("good")
                    cur2.nextset()

                    self.con2.rollback()
                    res = make_response({"workdata":"Cannot add"},201)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                    # message is not shown for 204    
        except Exception as e:
            print(e)
            cur2.nextset()

            traceback.print_exc()
            self.con2.rollback()
            res = make_response({"workdata":"got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'            
            return res
            
###########################   GET WORK DATA API   ##########################
    def getworkforoperator_model(self):
        try:
            
            
            # month = data.get('month')
            # date = data.get('date')

            # current_date = datetime.now()

            # Extract the month and date
            # month = current_date.strftime('%m')
            # date = current_date.strftime('%d')

            # Construct and execute the query
            query = "SELECT * FROM work_f1 WHERE DATE(STR_TO_DATE(timestamp, '%W, %M %d, %Y %H:%i:%s')) = CURDATE()"

            with self.con2.cursor(dictionary=True) as cur2:
                if not self.con2.is_connected():
                    self.con2.reconnect()

                cur2.execute(query)
                result = cur2.fetchall()
                print(result)
           
                if result is not None:



                    for entry in result:
                        station_id = entry["station_id"]
                        split_items = station_id.split()
                        # print(split_items)
                        if len(split_items) == 3:
                            F1, L1, S1 = split_items

                    # Further split each part
                            F1_part1, F1_part2 = F1[0], F1[1:]
                            L1_part1, L1_part2 = L1[0], L1[1:]
                            S1_part1, S1_part2 = S1[0], S1[1:]

                            # print("F1:", F1_part1, F1_part2)
                            # print("L1:", L1_part1, L1_part2)
                            # print("S1:", S1_part1, S1_part2)                
                        # station_num = "".join(filter(str.isdigit, station_id_parts[-1]))

                        entry["station_num"] = S1_part2
                    # print(result)
                    res = make_response({"processdata": result},200)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    # print(res)
                    return res
    
                else:
                    res = make_response({"processdata":"No Data Found"},201)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
        except Exception as e:
            print(e)
            traceback.print_exc()
            res = make_response({"processdata":"got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'            
            return res
            
###########################   REJECTED_REASON API   ##########################
    def reason_model(self,data):
        try:
            process_id = data.get('process_id')

            # Construct and execute the query
            query = f"SELECT * FROM rejected_reason WHERE process_id = '{process_id}'"
            with self.con2.cursor(dictionary=True) as cur2:
                if not self.con2.is_connected():
                    self.con2.reconnect()
        
                cur2.execute(query)
                result = cur2.fetchone()
                cur2.nextset()


                if result is not None:
                    # return json.dumps(result)
                    # return{"payload": result}
                    res = make_response({"reasondata": result},200)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                else:
                # return {"message":"No Data Found"}
                    print("good")
                    res = make_response({"reasondata":"No Data Found"},401)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                # message is not shown for 204    
        except Exception as e:
            print(e)
            res = make_response({"reasondata":"Got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'
            return res

###########################   GET WORK DATA API   ##########################
    def getwork_model(self,data):
        try:
           
            floor_id = data.get('floor_id')

            query = f"SELECT * FROM work_f1 WHERE floor_id='{floor_id}'"
            with self.con2.cursor(dictionary=True) as cur2:
                if not self.con2.is_connected():
                    self.con2.reconnect()
        
                cur2.execute(query)
                result = cur2.fetchall()
                # print("start")
                # print(result)
                if cur2.rowcount > 0:
                        res = make_response({"workdata": result},200)
                        res.headers['Access-Control-Allow-Origin'] = "*"
                        res.headers['Content-Type'] = 'application/json'
                        return res
                else:
                    res = make_response({"workdata":"Cannot fetch"},201)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                # message is not shown for 204    
        except Exception as e:
            print(e)
            traceback.print_exc()
            res = make_response({"workdata":"got error"},202)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'            
            return res
        

            
###########################   ADD_STATION API   ##########################
    def add_station_model(self,data):
        print(data)
        try:
            qry = "INSERT INTO stations(station_id, e_one, e_one_name, e_one_skill, e_two, e_two_name, e_two_skill, process_id, process_name, process_skill) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = [
                (
                stationdata.get('station_id'),
                stationdata.get('e_one'),
                stationdata.get('e_one_name'),
                stationdata.get('e_one_skill'),
                stationdata.get('e_two'),
                stationdata.get('e_two_name'),
                stationdata.get('e_two_skill'),
                stationdata.get('process_id'),
                stationdata.get('process_name'),
                stationdata.get('process_skill')
                ) 
                for stationdata in data]
            
            with self.con2.cursor(dictionary=True) as cur2:
                if not self.con2.is_connected():
                    self.con2.reconnect()
                cur2.executemany(qry, values)
                result = cur2.fetchone()


                if cur2.rowcount > 0:
                    cur2.nextset()
                    res = make_response({"addStation": "added successfully"},201)
                    # res = make_response({"addStation": result},200)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res
                else:
                    cur2.nextset()
                    res = make_response({"addStation":"cannot add"},202)
                    res.headers['Access-Control-Allow-Origin'] = "*"
                    res.headers['Content-Type'] = 'application/json'
                    return res

        except Exception as e:
            print(e)
            traceback.print_exc()
            cur2.nextset()
            res = make_response({"addStation":"Got error"},500)
            res.headers['Access-Control-Allow-Origin'] = "*"
            res.headers['Content-Type'] = 'application/json'
            return res

#VFT

    def getAllUsers_model(self):
        self.cur.execute("SELECT * FROM centers")
        result =  self.cur.fetchall()

        if len(result)>0:
            # return json.dumps(result)
            # return{"payload": result}
            res = make_response({"payload": result},200)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res
        else:
            # return {"message":"No Data Found"}
            return make_response({"message":"No Data Found"},204)
             # message is not shown for 204
        

    def addOneUser_model(self, data):
        self.cur.execute(f"INSERT INTO users(name, roll, password) VALUES('{data['name']}','{data['roll']}','{data['password']}')")
        # print(data['name'])
        return make_response({"message":"User Created Successfully"},201)
    

    def updateOneUser_model(self, data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}', roll='{data['roll']}' WHERE id={data['id']}")
        if self.cur.rowcount>0:
            return make_response({"message":"User Updated Successfully"},201)
        else:
            return make_response({"message":"No Data Found"},202)
   
        # print(data['name'])
        # return "updating data"    


    def deleteOneUser_model(self, id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"User Deleted Successfully"},201)
        else:
        # print(data['name'])
            return make_response({"message":"No Data Found"},202)
    
             
        # return result


        # USER VERIFY
    def verifyUser_model(self, username, tabpassword,center):
        self.cur.execute(f"SELECT * FROM users WHERE username='{username}' AND tabpassword='{tabpassword}' AND center = '{center}'")
        result = self.cur.fetchone()

        if result:
            return make_response({"message": "Login Successful"}, 200)
        else:
            return make_response({"message": "Authentication Error"}, 401)

        #USER VERIFY DESKTOP
    def verifyUser_modelpc(self, username, password,center):
        self.cur.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}' AND center = '{center}'")
        result = self.cur.fetchone()

        if result:
            return make_response({"message": "Login Successful"}, 200)
        else:
            return make_response({"message": "Authentication Error"}, 401)


            #CENTER VERIFY
    def verifyCenter_model(self, id, lat, lon):
        # self.cur.execute(f"SELECT * FROM centers WHERE id='{id}' AND (lat - {lat} < 2.5 OR lat - {lat} < 2.5) AND (lon - {lon} < 2.5 OR lon - {lon} < 2.5)")
        # self.cur.execute(f"SELECT * FROM centers WHERE (lat > {lat} - 0.5 OR lat < {lat} + 0.5) AND (lon > {lon} - 0.5 OR lon < {lon} + 0.5)")
        self.cur.execute(f"SELECT * FROM centers WHERE id='{id}' AND (lat >= {lat} - 1 AND lat <= {lat} + 1) AND (lon >= {lon} - 1 AND lon <= {lon} + 1)")

        result =  self.cur.fetchall()

        print(result)
        if len(result)>0:
            # return json.dumps(result)
            # return{"payload": result}
            return make_response({"status": "Found"},200)
            res.headers['Access-Control-Allow-Origin'] = "*"
            # return res
        else:
            # return {"message":"No Data Found"}
            return make_response({"status":"No Data Found"},204)
            # return "failed"
             # message is not shown for 204


     #Check Pending Test
    def checkPendingTest_model(self, center):
        # self.cur.execute(f"SELECT * FROM centers WHERE id='{id}' AND (lat - {lat} < 2.5 OR lat - {lat} < 2.5) AND (lon - {lon} < 2.5 OR lon - {lon} < 2.5)")
        # self.cur.execute(f"SELECT * FROM centers WHERE (lat > {lat} - 0.5 OR lat < {lat} + 0.5) AND (lon > {lon} - 0.5 OR lon < {lon} + 0.5)")
        try:
            print(center)
            self.cur.execute(f"SELECT * FROM tests WHERE center='{center}' AND stage = 1")
            result =  self.cur.fetchone()
            print(result)
            if  result:
                test_id = result['id']
                mStage = result['stage']
                print(f"Test ID: {test_id}")

                self.cur.execute(f"SELECT * FROM appointments WHERE id = '{test_id}' AND testcenter='{center}'")
                result =  self.cur.fetchone()

            # return json.dumps(result)
                return{"payload": result,"id":test_id, "stage": mStage}
            # return make_response({"status": "Found"},200)
                res.headers['Access-Control-Allow-Origin'] = "*"
            # return res
            else:
            # return {"message":"No Data Found"}
                return make_response({"status":"No Data Found"},400)
            # return "failed"
             # message is not shown for 204
        except Exception as e: 
                print(e)
        
    #GETVEHICLEDATA
    def checkTest_model(self, id):
        # self.cur.execute(f"SELECT * FROM centers WHERE id='{id}' AND (lat - {lat} < 2.5 OR lat - {lat} < 2.5) AND (lon - {lon} < 2.5 OR lon - {lon} < 2.5)")
        # self.cur.execute(f"SELECT * FROM centers WHERE (lat > {lat} - 0.5 OR lat < {lat} + 0.5) AND (lon > {lon} - 0.5 OR lon < {lon} + 0.5)")
        self.cur.execute(f"SELECT * FROM tests WHERE id='{id}'")

        result =  self.cur.fetchone()

        print(result)
   
        return{"payload2": result}
        
        

    #TEST STATUS
    def checkVehicle_model(self, id):
        self.cur.execute(f"SELECT * FROM appointments WHERE vehicalnumber='{id}'")

        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

        
        

        #HEADLAMP STATUS
        


       #ADD HEADLMAP TEST ONE
      


    #ADD HEADLMAP TEST ONE
    def addHeadlampTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testheadlamp(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testheadlamp = '{status}' WHERE id='{id}'")
            self.con.commit()
            # print(len(img))
            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},402)

    #ADD TOPLIGHT TEST ONE
    def addTopLightTest_one_model(self, id,p1,p2,p3,p4,p5,p6,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testtoplight(id,p1,p2,p3,p4,p5,p6,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{p6}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testtoplight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD STOPLIGHT TEST ONE
    def addStopLightTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO teststoplight(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET teststoplight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            traceback.print_exc()
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD PARKINGLIGHT TEST ONE
    def addParkingLightTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testparkinglight(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testparkinglight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD FOGLIGHT TEST ONE
    def addFogLightTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testfoglight(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testfoglight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD WARNINGLIGHT TEST ONE
    def addWarningLightTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testwarninglight(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testwarninglight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD NUMBEPLATELIGHT TEST ONE
    def addPlateLightTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testnumberplatelight(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testnumberplatelight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD MARKERLIGHT TEST ONE
    def addMarkerLightTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testoutlinemarkerlight(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testoutlinemarkerlight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD MARKERLIGHT TEST ONE
    def addDirectionLightTest_one_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testdirectionlight(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testdirectionlight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

#ADD HAZARDLIGHT TEST ONE
    def addHazardLightTest_one_model(self, id,p1,p2,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testhazardlight(id,p1,p2,remark,status,img) VALUES('{id}','{p1}','{p2}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testhazardlight = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)


    #ADD SUPRESSOR TEST ONE
    def addSupressorTest_one_model(self, id,p1,p2,p3,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testsupressor(id,p1,p2,p3,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testsupressor = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            traceback.print_exc()
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)


    #ADD REAR MIRROR ONE
    def addRearMirror_model(self, id,p1,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testrearmirror(id,p1,remark,status,img) VALUES('{id}','{p1}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testrearmirror = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

  
    #ADD SAFETY GLASS TEST ONE
    def addSafetyGlassTest_one_model(self, id,p1,p2,p3,remark,status,img):
        try:
            self.con.start_transaction()
            
            self.cur.execute(f"INSERT INTO testsafetyglass(id,p1,p2,p3,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testsafetyglass = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

    #ADD HORN TEST ONE
    def addHornTest_one_model(self, id,p1,p2,p3,p4,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testhorn(id,p1,p2,p3,p4,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testhorn = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            print(e)
            return make_response({"status":"Rolled Back"},400)

    #ADD EXHAUST TEST ONE
    def addexhaustTest_one_model(self, id,p1,p2,p3,p4,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testsilencer(id,p1,p2,p3,p4,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testsilencer = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

    #ADD WIPER SYSTEM TEST ONE
    def addwsystemTest_one_model(self, id,p1,p2,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testwipersystem(id,p1,p2,remark,status,img) VALUES('{id}','{p1}','{p2}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testwipersystem = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

    #ADD WIPER BLADE TEST ONE
    def addwbladeTest_one_model(self, id,p1,p2,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testwiperblade(id,p1,p2,remark,status,img) VALUES('{id}','{p1}','{p2}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testwiperblade = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

    #ADD DASH TEST ONE
    def addDashTest_one_model(self, id,p1,p2,p3,p4,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testdashboard(id,p1,p2,p3,p4,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testdashboard = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

    #ADD TEST BRAKING MANUAL
    def addTestBraking_model(self, id,p1,p2,p3,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testbrakingmanual(id,p1,p2,p3,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testbrakingmanual = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

    #ADD TEST PARKING BRAKING MANUAL
    def addTestParkingBraking_model(self, id,p1,p2,p3,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testparkingbrakingmanual(id,p1,p2,p3,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testparkingbrakingmanual = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

    #ADD TEST STEERING MANUAL
    def addTestSteering_model(self, id,p1,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO teststeering(id,p1,remark,status,img) VALUES('{id}','{p1}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET teststeering = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)


    #ADD TEST JOINTPLAY MANUAL
    def addTestJointPlay_model(self, id,p1,p2,p3,p4,p5,p6,p7,p8,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testjointplay(id,p1,p2,p3,p4,p5,p6,p7,p8,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{p6}','{p7}','{p8}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testjointplay = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)


    #ADD TEST SPEEDOMETER MANUAL
    def addTestSpeedometerManual_model(self, id,p1,p2,p3,p4,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testspeedometermanual(id,p1,p2,p3,p4,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testspeedometermanual = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)


    #ADD TEST RUPD MANUAL
    def addTestrupd_model(self, id,p1,p2,p3,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testrupd(id,p1,p2,p3,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testrupd = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)


    #ADD TEST LUPD MANUAL
    def addTestlupd_model(self, id,p1,p2,p3,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testlupd(id,p1,p2,p3,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testlupd = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)


    #ADD TEST FASTAG MANUAL
    def addTestfastag_model(self, id,p1,p2,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testfastag(id,p1,p2,remark,status,img) VALUES('{id}','{p1}','{p2}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testfastag = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)
 

    #ADD TEST OTHERS
    def addTestothers_model(self, id,p1,p2,p3,p4,p5,p6,p7,p8,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testothers(id,p1,p2,p3,p4,p5,p6,p7,p8,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{p6}','{p7}','{p8}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testothers = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)


    #ADD TEST WHEEL
    def addTestWheel_model(self, id,p1,p2,p3,p4,p5,p6,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testwheel(id,p1,p2,p3,p4,p5,p6,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{p6}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testwheel = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)


    #ADD TEST VLT
    def addTestVlt_model(self, id,p1,p2,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testvlt(id,p1,p2,remark,status,img) VALUES('{id}','{p1}','{p2}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testvlt = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)
 

    #ADD TEST HSRP
    def addTestHsrp_model(self, id,p1,p2,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testhsrp(id,p1,p2,remark,status,img) VALUES('{id}','{p1}','{p2}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testhsrp = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)
 
 
    #ADD TEST BATTERY
    def addTestBattery_model(self, id,p1,p2,p3,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testbattery(id,p1,p2,p3,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testbattery = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)
 
  
    #ADD TEST SAFETYBELT
    def addTestSafetyBelt_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testsafetybelt(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testsafetybelt = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)
 
  
    #ADD TEST SPEED GOVERNER
    def addTestSpeedG_model(self, id,p1,p2,p3,p4,p5,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testspeedgoverner(id,p1,p2,p3,p4,p5,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testspeedgoverner = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)
 


    #ADD TEST SPRAY
    def addTestSpray_model(self, id,p1,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testspray(id,p1,remark,status,img) VALUES('{id}','{p1}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testspray = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)
 


    #ADD TEST TYRES
    def addTestTyres_model(self, id,p1,p2,p3,p4,p5,p6,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testtyres(id,p1,p2,p3,p4,p5,p6,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{p6}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testtyres = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)

  #ADD TEST TYRES
    def addTestRetro_model(self, id,p1,p2,p3,p4,p5,p6,p7,p8,p9,remark,status,img):
        try:
            self.con.start_transaction()

            self.cur.execute(f"INSERT INTO testretro(id,p1,p2,p3,p4,p5,p6,p7,p8,p9,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{p5}','{p6}','{p7}','{p8}','{p9}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testretro = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)





    #ADD BRAKE TEST ONE
    def addBrakeTest_one_model(self, id, status):
        try:
            self.con.start_transaction()
            # self.cur.execute(f"INSERT INTO testdashboard(id,p1,p2,p3,p4,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{remark}','{status}','{img}')")
            self.cur.execute(f"UPDATE tests SET testbrake = '{status}' WHERE id='{id}'")
            self.con.commit()

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Added"},200)
            else:
                return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            self.con.rollback()
            return make_response({"status":"Rolled Back"},400)
                  
 
    #ADD DASH TEST ONE
    def addCompleteTest_one_model(self, id,mstatus):
        try:

            self.cur.execute(f"UPDATE tests SET stage = 2,mtest = '{mstatus}' WHERE id='{id}'")

            result =  self.cur.fetchone()
            if self.cur.rowcount>0:
                return make_response({"status":"Test Submitted"},200)
            else:
                return make_response({"status":"Cannot submit"},401)
        except Exception as e:
            print(e)
            return make_response({"status":"Error"},400)  
             
     #CHECK TEST
    def checkTest_one_model(self, id, center):
        try:
            # self.cur.execute(f"INSERT INTO testdashboard(id,p1,p2,p3,p4,remark,status) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{remark}','{status}')")
            self.cur.execute(f"SELECT * FROM tests WHERE stage = 1")
            result = self.cur.fetchone()

            if result:
                print(result)
                return make_response({"status":"Test Already Running"},401)
            else:
                self.cur.execute(f"INSERT INTO tests(id,center,stage) VALUES('{id}','{center}',1)")
                result =  self.cur.fetchone()
                if self.cur.rowcount>0:
                    return make_response({"status":"Test Added"},200)
                else:
                    return make_response({"status":"Cannot add test"},401)
        except Exception as e:
            print(e)
            return make_response({"status":"Error"},400)

    #CHECK TEST DATA
    def checkTestData_one_model(self, id, center):
        try:
            
            # self.cur.execute(f"INSERT INTO testdashboard(id,p1,p2,p3,p4,remark,status) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{remark}','{status}')")

            self.cur.execute(f"SELECT * FROM tests WHERE id = '{id}'")
            result = self.cur.fetchone()

            if result:
                return make_response({"payload":result},200)
            else:
                return make_response({"payload":"Not found"},401)
        except Exception as e:
            print(e)
            return make_response({"status":"Error"},400)

    #HEADLAMP TEST STATUS
    def checkTest_headlamp_model(self, id): 
        
        try:
            self.cur.execute(f"SELECT * FROM testheadlamp WHERE id='{id}'")
            result =  self.cur.fetchone()

            if result:
                print(result)
                return{"payload": result}

            else: 
                return make_response({"status":"No Data Found"},204)
        except Exception as e: 
                print(e)
                  
    #TOP LIGHT STATUS
    def checkTest_toplight_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testtoplight WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)


                  
    #TOP LIGHT STATUS
    def checkTest_stoplight_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM teststoplight WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)


                  
    #TOP LIGHT STATUS
    def checkTest_parkinglight_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testparkinglight WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)


                  
    #TOP LIGHT STATUS
    def checkTest_foglight_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testfoglight WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)


                  
    #TOP LIGHT STATUS
    def checkTest_warninglight_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testwarninglight WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)


                  
    #TOP LIGHT STATUS
    def checkTest_numberplatelight_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testnumberplatelight WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)


                  
    #TOP LIGHT STATUS
    def checkTest_outlinemarkerlight_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testoutlinemarkerlight WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)


                  
    #TOP LIGHT STATUS
    def checkTest_directionlight_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testdirectionlight WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)


                  
    #TOP LIGHT STATUS
    def checkTest_hazardlight_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testhazardlight WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)


                  
    #TOP LIGHT STATUS
    def checkTest_rearmirror_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testrearmirror WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

    #HEADLAMP TEST STATUS
    def checkTest_supressor_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testsupressor WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

    #HEADLAMP TEST STATUS
    def checkTest_safetyglasses_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testsafetyglass WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

    #HEADLAMP TEST STATUS
    def checkTest_horn_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testhorn WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)
        
      #HEADLAMP TEST STATUS
    def checkTest_exhaust_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testsilencer WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)    

    #HEADLAMP TEST STATUS
    def checkTest_wiperblade_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testwiperblade WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

    #HEADLAMP TEST STATUS
    def checkTest_wipersystem_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testwipersystem WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

    #HEADLAMP TEST STATUS
    def checkTest_dashboard_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testdashboard WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

    #HEADLAMP TEST STATUS
    def checkTest_Rearmirror_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testrearmirror WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)


                #HEADLAMP TEST STATUS
    def checkTest_Brakingmanual_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testbrakingmanual WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)


                #HEADLAMP TEST STATUS
    def checkTest_Parkingbrakingmanual_model(self, id): 
        self.cur.execute(f"SELECT * FROM testparkingbrakingmanual WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_Steering_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM teststeering WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_jointplay_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testjointplay WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_Speedometermanual_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testspeedometermanual WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_RUPD_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testrupd WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_LUPD_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testlupd WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_Fastag_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testfastag WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_Others_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testothers WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_Wheel_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testwheel WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_Vlt_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testvlt WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_hsrp_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testhsrp WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_battery_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testbattery WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_Safetybelt_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testsafetybelt WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_Speedgoverner_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testspeedgoverner WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_Spray_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testspray WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                #HEADLAMP TEST STATUS
    def checkTest_tyres_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testtyres WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

                             #HEADLAMP TEST STATUS
    def checkTest_retro_model(self, id): 
        
        self.cur.execute(f"SELECT * FROM testretro WHERE id='{id}'")
        result =  self.cur.fetchone()

        if result:
            print(result)
            return{"payload": result}
        else: 
            return make_response({"status":"No Data Found"},204)

    def getAlltestData(self, id):
        try:
            self.con.start_transaction()

            # Define a dictionary to store results
            all_results = {}

            # List of queries
            queries = [
                "testheadlamp", "testtoplight", "teststoplight", "testparkinglight",
                "testfoglight", "testwarninglight", "testnumberplatelight",
                "testoutlinemarkerlight", "testdirectionlight", "testhazardlight",
                "testrearmirror", "testsupressor", "testsafetyglass", "testhorn",
                "testsilencer", "testwiperblade", "testwipersystem", "testdashboard",
                "testbrakingmanual", "testparkingbrakingmanual", "teststeering",
                "testjointplay", "testspeedometermanual", "testrupd", "testlupd",
                "testfastag", "testothers", "testwheel", "testvlt", "testhsrp",
                "testbattery", "testsafetybelt", "testspeedgoverner", "testspray",
                "testretro", "testtyres"
            ]

            # Execute queries and store results
            for query in queries:
                self.cur.execute(f"SELECT * FROM {query} WHERE id='{id}'")
                all_results[query] = self.cur.fetchone()

            # Commit the transaction
            self.con.commit()

            # Check the results and return the response
            if any(self.cur.rowcount > 0 for query in queries):
                return make_response({"testdata": all_results}, 200)
            else:
                self.con.rollback()
                return make_response({"status": "Cannot get test"}, 401)

        except Exception as e:
            traceback.print_exc()
            self.con.rollback()
            return make_response({"status": "Rolled Back"}, 400)
                                                                                                                                                
    # def getAlltestData(self,id):
    #     try:
    #         self.con.start_transaction()
    #         # self.cur.execute(f"INSERT INTO testdashboard(id,p1,p2,p3,p4,remark,status,img) VALUES('{id}','{p1}','{p2}','{p3}','{p4}','{remark}','{status}','{img}')")
    #         # self.cur.execute(f"UPDATE tests SET testbrake = '{status}' WHERE id='{id}'")
    #           # Execute the first query


    #         self.cur.execute(f"SELECT * FROM testheadlamp WHERE id='{id}'")
    #         resultheadlamp =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testtoplight WHERE id='{id}'")
    #         resulttoplight =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM teststoplight WHERE id='{id}'")
    #         resultstoplight =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testparkinglight WHERE id='{id}'")
    #         resultparkinglight =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testfoglight WHERE id='{id}'")
    #         resultfoglight =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testwarninglight WHERE id='{id}'")
    #         resultwarninglight =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testnumberplatelight WHERE id='{id}'")
    #         resultnumberplate =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testoutlinemarkerlight WHERE id='{id}'")
    #         resultoutlinemarker =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testdirectionlight WHERE id='{id}'")
    #         resultdirectionlight =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testhazardlight WHERE id='{id}'")
    #         resulthazardlight =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testrearmirror WHERE id='{id}'")
    #         resultrearmirror =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testsupressor WHERE id='{id}'")
    #         resultsupressor =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testsafetyglass WHERE id='{id}'")
    #         resultsafetyglass =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testhorn WHERE id='{id}'")
    #         resulthorn =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testsilencer WHERE id='{id}'")
    #         resultsilencer =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testwiperblade WHERE id='{id}'")
    #         resultwiperblade =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testwipersystem WHERE id='{id}'")
    #         resultwipersystem =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testdashboard WHERE id='{id}'")
    #         resultdashboard =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testbrakingmanual WHERE id='{id}'")
    #         resultbrakingmanual =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testparkingbrakingmanual WHERE id='{id}'")
    #         resultparkingbrakingmanual =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM teststeering WHERE id='{id}'")
    #         resultsteering =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testjointplay WHERE id='{id}'")
    #         resultjointplay =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testspeedometermanual WHERE id='{id}'")
    #         resultspeedometermanual =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testrupd WHERE id='{id}'")
    #         resultrupd =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testlupd WHERE id='{id}'")
    #         resultlupd =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testfastag WHERE id='{id}'")
    #         resultfastag =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testothers WHERE id='{id}'")
    #         resultothers =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testwheel WHERE id='{id}'")
    #         resultwheel =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testvlt WHERE id='{id}'")
    #         resultvlt =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testhsrp WHERE id='{id}'")
    #         resulthsrp =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testbattery WHERE id='{id}'")
    #         resultbattery =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testsafetybelt WHERE id='{id}'")
    #         resultsafetybelt =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testspeedgoverner WHERE id='{id}'")
    #         resultspeedgoverner =  self.cur.fetchone()

    #         self.cur.execute(f"SELECT * FROM testspray WHERE id='{id}'")
    #         resultspray =  self.cur.fetchall()

    #         self.cur.execute(f"SELECT * FROM testretro WHERE id='{id}'")
    #         result_retro = self.cur.fetchall()

    #     # Execute the second query
    #         self.cur.execute(f"SELECT * FROM testtyres WHERE id='{id}'")
    #         result_tyres = self.cur.fetchall()
    #         self.con.commit()

    #         if self.cur.rowcount>0:
    #             return make_response({"testretro": result_retro, "testtyres": result_tyres}, 200)

    #         else:
    #             self.con.rollback()
    #             return make_response({"status":"Cannot get test"},401)
    #     except Exception as e:
    #         traceback.print_exc()
    #         self.con.rollback()
    #         return make_response({"status":"Rolled Back"},400)

    def add_test_data_model(self, request_data):
        try:
            # request_data = request.get_json()
            # print(request_data)
            # id = request_data.get('id')
            # table_name = request_data.get('table_name')
            # params = request_data.get('params')
            # status = request_data.get('status')
            # img = request_data.get('img')
            # remark = request_data.get('remark')
            # self.con.start_transaction()

            # print(params)

            nested_data = request_data.get('nameValuePairs', {})
            id = nested_data.get('id')
            table_name = nested_data.get('table_name')
            params = nested_data.get('params')
            status = nested_data.get('status')
            img = nested_data.get('img')
            remark = nested_data.get('remark')

            query = f"INSERT INTO {table_name}({','.join(params.keys())}, img, remark, status) VALUES({','.join(['%s']*len(params))}, %s, %s, %s)"
            values = [params[key] for key in params] + [img, remark, status]

            # Execute the INSERT query
            self.cur.execute(query, values)

            # Update the status in the 'tests' table
            self.cur.execute(f"UPDATE tests SET {table_name} = %s WHERE id = %s", (status, id))

            # Commit the transaction
            self.con.commit()

            if self.cur.rowcount > 0:
                return make_response({"status": "Test Added"}, 200)
            else:
                return make_response({"status": "Cannot add test"}, 401)

        except Exception as e:
            traceback.print_exc()
            self.con.rollback()
            return make_response({"status": "Rolled Back"}, 400)