from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response

class Staff(APIView):

    def get(self,request):
            
            response_object = {
                "success": False,
                "messages": []
            }
    
            try:
                if request.token:

                    if (request.token['user_type'] != "Permanent" and request.token['user_type'] != "Admin"):
                        response_object["success"] = False
                        response_object["messages"].append("User is not authorized")
                        return Response(response_object,status=400)
                    
                    cursor = connection.cursor()
                    cursor.execute("""SELECT u.user_id as staff_id,concat(u.user_first_name,' ',u.user_middle_name,' ',u.user_last_name) as staff_name,u.user_email as staff_email
                            FROM public.user u WHERE u.user_type = 'Permanent';""")
                    row = cursor.fetchall()
                    staff_details = []
                    if row is None:
                        response_object["success"] = False
                        response_object["messages"].append("Staff does not exsist")
                        return Response(response_object,status=400)
                    else:
                        for i in range(len(row)):
                            staff_detail = {}
                            for j in range(len(row[i])):
                                staff_detail[cursor.description[j][0]] = row[i][j]
                            staff_details.append(staff_detail)
                        
                        response_object["success"] = True
                        response_object["messages"].append("Staff retrieved")
                        response_object["data"] = staff_details
                        return Response(response_object,status=200)
            except Exception as e:
                response_object["success"] = False
                response_object["messages"] = e.args
                return Response(response_object,status=400)
        