from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response

class CV(APIView):

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
                cursor.execute("""SELECT user_cv
                        FROM public.user WHERE user_id = %s;""", [user_id])
                row = cursor.fetchone()
                user_cv = {}
                if row is None:
                    response_object["success"] = False
                    response_object["messages"].append("User does not exsist")
                    return Response(response_object,status=400)
                else:
                    for i in range(len(row)):
                        user_cv[cursor.description[i][0]] = row[i]

                    if user_cv["user_cv"] is None:
                        response_object["success"] = False
                        response_object["messages"].append("User does not have a CV")
                        return Response(response_object,status=400)  
                    elif len(user_cv["user_cv"]) < 100:
                        response_object["success"] = False
                        response_object["messages"].append("User does not have a CV")
                        return Response(response_object,status=400)
                    
                    response_object["success"] = True
                    response_object["messages"].append("User CV retrieved")
                    response_object["data"] = user_cv
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
            cv = request.data['cv']
        except Exception as e:
            response_object["success"] = False
            response_object["messages"].append("Missing data")
            return Response(response_object,status=400)

        try:
            if request.token:
                user_id = request.token['user_id']
                cursor = connection.cursor()
                cursor.execute(""" UPDATE public.user
                    SET user_cv = %s
                    WHERE user_id = %s;
                """, [cv, user_id])
                if cursor.rowcount < 0:
                    response_object["success"] = False
                    response_object["messages"].append("User does not exsist")
                    return Response(response_object,status=400)
                else:
                    response_object["success"] = True
                    response_object["messages"].append("User CV Uploaded")
                    return Response(response_object,status=200)
        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=400)