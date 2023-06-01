from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response

class Availability(APIView):

    def get(self, request):

        response_object = {
            "success": False,
            "messages": []
        }

        try:
            if request.token:
                    
                user_id = request.token['user_id']
                if (request.token['user_type'] == "Permanent" or request.token['user_type'] == "Admin"):
                    if request.query_params.get('user_id'):
                        user_id = request.query_params.get('user_id')

                cursor = connection.cursor()
                cursor.execute("""SELECT availability_weekday || '--' || availability_from || '--' || availability_until as availability
                        FROM public.availability WHERE user_id = %s;""", [user_id])
                row = cursor.fetchall()
                availability = []
                if row is None:
                    response_object["success"] = False
                    response_object["messages"].append("Availability does not exsist")
                    return Response(response_object,status=400)
                else:
                    for i in range(len(row)):
                        for j in range(len(row[i])):
                            availability.append(row[i][j])

                    response_object["success"] = True
                    response_object["messages"].append("Availability retrieved")
                    response_object["data"] = availability
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
            availability = request.data['availability']
        except Exception as e:
            response_object["success"] = False
            response_object["messages"].append("Missing data")
            return Response(response_object,status=400)
        
        if(availability is None or len(availability) <= 0):
            response_object["success"] = False
            response_object["messages"].append("Availabilty update failed as it was empty")
            return Response(response_object,status=400)
        
        


        try:
            if request.token:
                user_id = request.token['user_id']
                cursor = connection.cursor()

                # First delete all the availability for the user
                cursor.execute("""DELETE FROM public.availability WHERE user_id = %s;""", [user_id])

                # Insert Availability into table
                for i in range(len(availability)):
                    cursor.execute("""INSERT INTO public.availability(user_id, availability_weekday, availability_from, availability_until)
                        VALUES (%s, %s, %s, %s);""", [user_id, availability[i].split("--")[0], availability[i].split("--")[1], availability[i].split("--")[2]])

                if cursor.rowcount < 0:
                    response_object["success"] = False
                    response_object["messages"].append("Availability update failed")
                    return Response(response_object,status=400)
                else:
                    response_object["success"] = True
                    response_object["messages"].append("Availability updated")
                    return Response(response_object,status=200)
        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=400)
        
        



