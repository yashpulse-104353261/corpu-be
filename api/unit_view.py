from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response


class Unit(APIView):

    def get(self, request):

        response_object = {
            "success": False,
            "messages": []
        }

        try:
            if request.token:

                cursor = connection.cursor()
                cursor.execute("""SELECT un.unit_id,un.unit_name FROM public.unit un;""")
                row = cursor.fetchall()
                unit_details = []
                if row is None:
                    response_object["success"] = False
                    response_object["messages"].append("Unit does not exsist")
                    return Response(response_object,status=400)
                else:
                    for i in range(len(row)):
                        unit_detail = {}
                        for j in range(len(row[i])):
                            unit_detail[cursor.description[j][0]] = row[i][j]
                        unit_details.append(unit_detail)
                    
                    response_object["success"] = True
                    response_object["messages"].append("Units retrieved")
                    response_object["data"] = unit_details
                    return Response(response_object,status=200)
        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=400)

    def post(self, request):

        response_object = {
            "success": False,
            "messages": []
        }

        try:
            unit_id = request.data['unit_id']
            unit_name = request.data['unit_name']
        except Exception as e:
            response_object["success"] = False
            response_object["messages"].append("Missing data")
            return Response(response_object,status=400)

        try:
            if request.token:
                user_type = request.token['user_type']
                if user_type != "Admin" and user_type != "Permanent":
                    response_object["success"] = False
                    response_object["messages"].append("User does not have permission")
                    return Response(response_object,status=400)
                
                cursor = connection.cursor()
                cursor.execute(""" INSERT INTO public.unit (unit_id, unit_name)
                VALUES(%s,%s);""", [unit_id, unit_name])

                if cursor.rowcount < 0:
                    response_object["success"] = False
                    response_object["messages"].append("Unit Creation Failed")
                    return Response(response_object,status=400)
                else:
                    response_object["success"] = True
                    response_object["messages"].append("Unit Created Successfully")
                    return Response(response_object,status=200)
        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=400)
        

    def delete(self, request):

        response_object = {
            "success": False,
            "messages": []
        }

        try:
            if request.token:

                user_type = request.token['user_type']
                if user_type != "Admin" and user_type != "Permanent":
                    response_object["success"] = False
                    response_object["messages"].append("User does not have permission")
                    return Response(response_object,status=400)
                
                if request.query_params.get('unit_id'):
                    unit_id = request.query_params.get('unit_id')
                else:
                    response_object["success"] = False
                    response_object["messages"].append("Unit ID not provided")
                    return Response(response_object,status=400)

                cursor = connection.cursor()

                cursor.execute("""DELETE FROM public.application WHERE unit_ad_id IN (SELECT unit_ad_id FROM public.unit_job_advertisement WHERE unit_id = %s);""",[unit_id])
                cursor.execute("""DELETE FROM public.unit_job_advertisement WHERE unit_id = %s;""",[unit_id])
                cursor.execute("DELETE FROM public.assignment WHERE unit_id = %s;",[unit_id])
                cursor.execute("""DELETE FROM public.unit un WHERE un.unit_id = %s;""",[unit_id])
                if cursor.rowcount < 0:
                    response_object["success"] = False
                    response_object["messages"].append("Unit Deletion Failed")
                    return Response(response_object,status=400)            
                    
                response_object["success"] = True
                response_object["messages"].append("Unit ID: "+unit_id+" Deleted Successfully")
                return Response(response_object,status=200)
        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=400)

