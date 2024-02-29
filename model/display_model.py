import mysql.connector
from datetime import timedelta
import re
import json
from flask import make_response,jsonify
from datetime import datetime
import pytz
import traceback
# class user_model():
#     def _init_(self):
#         try:
#             self.con=mysql.connector.connect(host="localhost",user="root",password="Ga2001pillu14##",database="dunit")
#             self.cur=self.con.cursor(dictionary=True)
#             self.con.autocommit=True
#             print("connected successfully")
#         except:
#             print("some error")
            
#     def user_getall_model(self):
#         self.cur.execute("SELECT * FROM stations")
#         result=self.cur.fetchall()
#         if len(result)>0:
#             res = make_response({'payload':result},200)
#             res.headers['Access-Control-Allow-Origin']="*"
#             return res
#         else:
#             return make_response({"message":"No Data found"},204)
        
        
#     def user_addone_model(self,data):
#         self.cur.execute(f"INSERT INTO users(id,name,email,phone,password,role) VALUES({data['id']},'{data['name']}','{data['email']}','{data['phone']}','{data['password']}','{data['role']}')")
        
        
#         return make_response({"message":"user created successfully"},201)
            

class display_unit_model():
    def __init__(self):
        try:
            self.con=mysql.connector.connect(host="localhost",user="root",password="Hello123##",database="dunitv2")
            self.cur=self.con.cursor(dictionary=True)
            self.con.autocommit=True
            self.con2=mysql.connector.connect(host="localhost",user="root",password="Hello123##",database="dunitv2")
            self.cur2=self.con2.cursor(dictionary=True)
            self.con2.autocommit=True
            print("connected successfully")
        except:
            print("some error")
            
    def Station_model(self, data):
        try:
            qry = "INSERT INTO stations(station_id, e_one, e_one_name, e_one_skill, e_two, e_two_name, e_two_skill, process_id, process_name, process_skill) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = [(stationdata.get('station_id'),
                stationdata.get('e_one'),
                stationdata.get('e_one_name'),
                stationdata.get('e_one_skill'),
                stationdata.get('e_two_skill'),
                stationdata.get('e_two_name'),
                stationdata.get('e_two_skill'),
                stationdata.get('process_id'),
                stationdata.get('process_name'),
                stationdata.get('process_skill')
                ) for stationdata in data]
            self.cur.executemany(qry, values)
            if self.cur.rowcount > 0 :
                res= make_response({"message": "Stations(s) added successfully"}, 201)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res
            else:
                res= make_response({"message": "Stations(s) not successfully"}, 202)
                res.headers['Access-Control-Allow-Origin'] = "*"
                res.headers['Content-Type'] = 'application/json'
                return res

        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
            
        
        # print(data)
        # qry="INSERT INTO stations(station_id, e_one, e_two, process_id) VALUES "
        # for stationdata in data:
        #     qry +=f"('{stationdata['station_id']}','{stationdata['e_one']}','{stationdata['e_two']}','{stationdata['process_id']}')"
        # finalqry = qry.rstrip(",")
        # self.cur.execute(finalqry)
        
        # # res.headers['Access-Control-Allow-Origin']="*"
        # # res.headers['Content-Type']="application/json"
        # return make_response({"message":"Station added successfully"},201)
    def get_process(self,data):
        try:
            qry = "SELECT process_id,process_name,prrocess_skill FROM processes WHERE part_id = %s"  
            values = [data.get('part_id')]
            self.cur.execute(qry,values)
            result = self.cur.fetchall()
            if len(result)>0:
                res = make_response({'payload':result},200)
                res.headers['Access-Control-Allow-Origin']="*"
                return res
            else:
             return make_response({"message":"No Data found"},204)
        
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
        

    def get_process_and_login_data(self,data):
        try:
            qry = "SELECT process_id,process_name,prrocess_skill FROM processes WHERE part_id = %s"  
            values = [data.get('part_id')]
            self.cur.execute(qry,values)
            process_result = self.cur.fetchall()

            qry_login_operators= "SELECT CONCAT(first_name, ' ', last_name) AS full_name, employee_code, skill FROM login_operator"
            self.cur.execute(qry_login_operators)
            employees_result=self.cur.fetchall()

            response_data={
                'process_data':process_result,
                'employess_data':employees_result
            }

            if len(process_result) > 0 or len(employees_result) > 0:
                res = make_response({'payload':response_data},200)
                res.headers['Access-Control-Allow-Origin']="*"
                return res
            else:
             return make_response({"message":"No Data found"},204)
        
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
    
    def task_assigned_model(self, data):
        try:
            now_utc = datetime.now(pytz.utc)
            ist = pytz.timezone('Asia/Kolkata')
            now_ist = now_utc.astimezone(ist)
            assigned_for_date = now_ist.strftime('%Y-%m-%d')
            

            qry = "INSERT INTO task_assigned(floor_id, line_id, part_id, part_name, prev_quantity, quantity, assigned_for_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = [(taskassigned.get('floor_id'),
                taskassigned.get('line_id'),
                taskassigned.get('part_id'),
                taskassigned.get('part_name'),
                taskassigned.get('prev_quantity'),
                taskassigned.get('quantity'),
                assigned_for_date) for taskassigned in data]
           
            self.cur.executemany(qry, values)
            return make_response({"message": "task_assigned successfully"}, 201)
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
    
    # def get_task_assigend_model(self):
    #     try:
    #         self.cur.execute("SELECT * FROM task_assigned WHERE floor_id = 1")
    #         result=self.cur.fetchall()
    #         if len(result)>0:
    #           res = make_response({'payload':result},200)
    #           res.headers['Access-Control-Allow-Origin']="*"
    #           return res
    #         else:
    #             return make_response({"message":"No Data found"},204)
    #     except mysql.connector.Error as err:
    #         print(f"MySQL Error: {err}")
    #         return make_response({"error": "Internal Server Error"}, 500)
    
    def get_asssigned_parts_model(self):
        try:
            self.cur.execute("SELECT * FROM assigned_parts")
            result=self.cur.fetchall()
            if len(result)>0:
              res = make_response({'payload':result},200)
              res.headers['Access-Control-Allow-Origin']="*"
              return res
            else:
                return make_response({"message":"No Data found"},204)
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
    
    def get_task_assigend_model(self,data):
        try:
            qry = "SELECT * FROM task_assigned WHERE assigned_for_date = %s"  
            values = [data.get('assigned_for_date')]
            self.cur.execute(qry,values)
            process_result = self.cur.fetchone()

            # qry_login_operators= "SELECT CONCAT(first_name, ' ', last_name) AS full_name, employee_code, skill FROM login_operator"
            # self.cur.execute(qry_login_operators)
            # employees_result=self.cur.fetchall()

            # response_data={
            #     'process_data':process_result,
            #     'employess_data':employees_result
            # }

            if len(process_result) > 0 :
                res = make_response({'payload':process_result},200)
                res.headers['Access-Control-Allow-Origin']="*"
                return res
            else:
             return make_response({"message":"No Data found"},204)
        
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
        
    def update_assigned_parts_model(self,data):
        try:
            self.con.start_transaction()
            line_id = data.get('line_id')
            part_id = data.get('part_id')
            part_name = data.get('part_name')

        # Update assigned_parts table
            qry1 = """UPDATE assigned_parts SET part_id = %s, part_name = %s WHERE line_id = %s"""
            values1 = [part_id, part_name, line_id]
            self.cur.execute(qry1, values1)

        # Update stations table
            qry2 = """UPDATE stations SET process_id = NULL, process_name = NULL, process_skill = NULL WHERE station_id LIKE %s"""
            pattern = f'% L{line_id} S%'

            values2 = [pattern]
            # qry2="SELECT * FROM stations"
            # self.cur.execute(qry2)
            # result= self.cur.fetchall()
            # print(result)
            self.cur.execute(qry2,values2)

            self.con.commit()

            if self.cur.rowcount > 0:
                return make_response({"status": "Data updated successfully"}, 200)
            else:
                return make_response({"status": "No matching records found for update"}, 401)
        except Exception as e:
            print(e)
            self.con.rollback()
            return make_response({"status": "Rolled Back"}, 400)
        # try:
        #     self.con.start_transaction()
        #     line_id = data.get('line_id')
        #     part_id = data.get('part_id')
        #     part_name = data.get('part_name')

        # # Update assigned_parts table
        #     qry1 = """UPDATE assigned_parts SET part_id = %s, part_name = %s WHERE line_id = %s"""
        #     values1 = [part_id, part_name, line_id]
        #     self.cur.execute(qry1, values1)

        # # Update stations table
        #     # qry2 = """UPDATE stations SET process_id = NULL, process_name = NULL, process_skill = NULL WHERE station_id LIKE %s"""
        #     # pattern = f'% F1 L{line_id} S%'
        #     # values2 = [pattern]
        #     # self.cur.execute(qry2, values2)
        #     qry2 = "SELECT * FROM stations"
        #     self.cur2.execute(qry2)
        #     result = self.cur2.fetchall()
        #     if result is not None:
        #         for row in result:
        #             floor_num, line_num, station_num = row['station_id'].split(' ')
        #             transformed_row = {
        #                 'station_id': row['station_id'],
        #                 'floor_num': int(floor_num[1:]),
        #                 'line_num': int(line_num[1:]),
        #                 'station_num': int(station_num[1:]),
        #                 'e_one': row['e_one'],
        #                 'e_one_name': row['e_one_name'],
        #                 'e_one_skill': row['e_one_skill'],
        #                 'e_two': row['e_two'],
        #                 'e_two_name': row['e_two_name'],
        #                 'e_two_skill': row['e_two_skill'],
        #                 'process_id': row['process_id'],
        #                 'process_name': row['process_name'],
        #                 'process_skill': row['process_skill']
        #             }
        #             if str(int(line_num[1:])) == str(line_id):
        #                 row['process_id'] = None
        #                 row['process_name'] = None
        #                 row['process_skill'] = None



        #     self.con.commit()

        #     if self.cur.rowcount > 0:
        #         return make_response({"status": "Data updated successfully"}, 200)
        #     else:
        #         return make_response({"status": "No matching records found for update"}, 401)
        # except Exception as e:
        #     print(e)
        #     self.con.rollback()
        #     return make_response({"status": "Rolled Back"}, 400)
    
    def get_task_model(self):
        try:
            now_utc = datetime.now(pytz.utc)
            ist = pytz.timezone('Asia/Kolkata')
            now_ist = now_utc.astimezone(ist)
            assigned_for_date = now_ist.strftime('%Y-%m-%d')
            values = [assigned_for_date]
            qry = "SELECT * FROM task_assigned WHERE assigned_for_date = %s"
            self.cur.execute(qry,values)
            result=self.cur.fetchall()
            if len(result)>0:
              res = make_response({'payload':result},200)
              res.headers['Access-Control-Allow-Origin']="*"
              return res
            else:
                return make_response({"message":"No Data found"},204)
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
      
    def task_assigned_version_two_model(self, data):
        try:
            now_utc = datetime.now(pytz.utc)
            ist = pytz.timezone('Asia/Kolkata')
            now_ist = now_utc.astimezone(ist)
            assigned_for_date = now_ist.strftime('%Y-%m-%d')
            values = []

            for taskassigned in data:
                floor_id=taskassigned.get('floor_id')
                line_id=taskassigned.get('line_id')
                is_task_completed = taskassigned.get('is_task_completed',0)
                parts_completed=taskassigned.get('parts_completed',0)
                parts_filled=taskassigned.get('parts_filled',0)
                parts_passed=taskassigned.get('parts_passed',0)
                parts_failed=taskassigned.get('parts_failed',0)



                check_query = "SELECT COUNT(*) FROM task_assigned WHERE floor_id = %s AND line_id = %s AND assigned_for_date = %s AND is_task_completed = 0"
                check_values = (floor_id, line_id, assigned_for_date)
                self.cur.execute(check_query, check_values)
                existing_task_count_result = self.cur.fetchone()
                print(existing_task_count_result)
                # if existing_task_count_result and existing_task_count_result[0] > 0:
                #     # Task is already running
                #     return make_response({"message": "Task is already running"}, 200)
                # else:
                if existing_task_count_result and existing_task_count_result['COUNT(*)'] > 0:
                    return make_response({"message": "Task is already running"}, 200)
                
                else:

                    qry = "INSERT INTO task_assigned(floor_id, line_id, part_id, part_name, prev_quantity, quantity, assigned_for_date, is_task_completed, parts_completed, parts_filled, parts_passed, parts_failed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    
                    
                    values.append((taskassigned.get('floor_id'),
                              taskassigned.get('line_id'),
                              taskassigned.get('part_id'),
                              taskassigned.get('part_name'),
                              taskassigned.get('prev_quantity'),
                              taskassigned.get('quantity'),
                              assigned_for_date,
                              is_task_completed,
                              parts_completed,
                              parts_filled,
                              parts_passed,
                              parts_failed))
                    self.cur.executemany(qry, values)
                    return make_response({"message": "Task assigned successfully"}, 201)

                

        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
        

    def savework_model_version_two(self,data):
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
            
    def get_max_station_model(self,data):
        try:
            station_id=data.get('station_id')
            indian_timezone = pytz.timezone('Asia/Kolkata')
            # # Get the current time in UTC
            current_time_utc = datetime.utcnow()
            # # Convert UTC time to Indian time
            current_time_indian = current_time_utc.replace(tzinfo=pytz.utc).astimezone(indian_timezone)
            # # Print the formatted Indian time
            formatted_time = current_time_indian.strftime("%A, %B %d, %Y %H:%M:%S")
            parsed_time = datetime.strptime(formatted_time, "%A, %B %d, %Y %H:%M:%S")
            formatted_parsed_time = parsed_time.strftime("%Y-%m-%d")
            print(formatted_parsed_time)
            print(formatted_time)
            # # Format the datetime object as a string
            # formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            # print(formatted_time)

            
            # process_id = data.get('process_id')
            # part_id = data.get('part_id')
            # timestamp = formatted_time
            # floor_id = data.get('floor_id')
            # line_id = data.get('line_id')
            # status = data.get('status')
            # reason = data.get('reason')
            # remark = data.get('remark')
            # isfilled = data.get('isfilled')
            
            floor_id, line_id, station_id_num = map(int, re.findall(r'\d+', station_id))
            print(floor_id)
            print(line_id)
            print(station_id_num)
            parts = station_id.split(' ')
            if len(parts) == 3:
                floor_id_num = parts[0]
                print(floor_id_num)
                
                line_id_num = parts[1]
                print(line_id_num)
                station_num = parts[2]
                print(station_num)
            else:
                # Handle incorrect format of station_id
                raise ValueError("Invalid station_id format")
            
            

            # EXECUTE TRANSACTION
            self.con2.start_transaction()
            
            # Construct and execute the query
            # query = f"INSERT INTO work_f1 (station_id, process_id, part_id, timestamp, floor_id, line_id, status, reason, remark, isfilled) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # query = "INSERT INTO work_f1 (station_id, process_id, part_id, timestamp, floor_id, line_id, status, reason, remark, isfilled) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # values = (station_id, process_id, part_id, timestamp, floor_id, line_id, status, reason, remark, isfilled)
            # with self.con2.cursor(dictionary=True) as cur2:
            #     if not self.con2.is_connected():
            #         self.con2.reconnect()
       
            #     cur2.execute(query,values)
            query_work_assigned = "SELECT * FROM work_f1 WHERE station_id = %s"
            values_work_assigned = (station_id,)
            with self.con2.cursor(dictionary=True) as cur2:
                cur2.execute(query_work_assigned, values_work_assigned)
                work_assigned_result = cur2.fetchone()
                print(work_assigned_result)

            query_task_assigned = "SELECT * FROM task_assigned WHERE floor_id = %s AND line_id = %s AND assigned_for_date = %s"
            values_task_assigned = (floor_id, line_id, formatted_parsed_time)
            with self.con2.cursor(dictionary=True) as cur2:
                cur2.execute(query_task_assigned, values_task_assigned)
                task_assigned_result = cur2.fetchone()
                print(task_assigned_result)
        
            if task_assigned_result and work_assigned_result:
                # Matching record found, check the status
                status_version_two = work_assigned_result['status']
                print(status_version_two)
                max_station_num=None
                if status_version_two == '0':
                    # Increment parts_failed in task_assigned table
                    query_update_failed = "UPDATE task_assigned SET parts_failed = parts_failed + 1 WHERE floor_id = %s AND line_id = %s AND assigned_for_date = %s"
                    print(task_assigned_result['parts_failed'])
                    values_update_failed = (floor_id, line_id, formatted_parsed_time)
                    with self.con2.cursor() as cur2:
                        cur2.execute(query_update_failed, values_update_failed)
                        print('failed updated succesfully')
                elif status_version_two == '1':
                     query = "SELECT MAX(CAST(SUBSTRING_INDEX(station_id, 'S', -1) AS UNSIGNED)) AS max_station_num FROM stations WHERE station_id LIKE %s"
                     values = (f"{floor_id_num} {line_id_num} S%",)
                     with self.con2.cursor() as cur2:
                         cur2.execute(query, values)
                         result = cur2.fetchone()
                         max_station_num = result[0] if result else None
                         print("max_station_num:", max_station_num)
                         print("station_num:", station_num)
                         if max_station_num is not None:
                             if station_id_num==max_station_num:
                                 query_update_passed = "UPDATE task_assigned SET parts_passed = parts_passed + 1 WHERE floor_id = %s AND line_id = %s AND assigned_for_date = %s"
                                 values_update_passed = (floor_id, line_id, formatted_parsed_time)
                                 cur2.execute(query_update_passed, values_update_passed)
                                 print('passed updated succesfully')
                             else:
                                 pass
                             
                                 
                    # Increment parts_passed in stations table
                    # query_update_passed = "UPDATE stations SET parts_passed = parts_passed + 1 WHERE floor_id = %s AND line_id = %s AND station_num = %s"
                    # values_update_passed = (floor_id, line_id, station_num)
                    # cur2.execute(query_update_passed, values_update_passed)
                else:
                    # No matching record found in task_assigned table, handle accordingly
                    pass

                self.con2.commit()

        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            return make_response({"error": "Internal Server Error"}, 500)
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.con2.rollback()
            return make_response({"workdata": "got error"}, 202)
        else:
            return make_response({"workdata": "completed"}, 200)
        

        
