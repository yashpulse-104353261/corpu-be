from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response

class Apply(APIView):

    def get(self, request):

        response_object = {
            "success": False,
            "messages": []
        }

        try:
            if request.token:
                    
                user_id = request.token['user_id']
                if (request.token['user_type'] == "Permanent" or request.token['user_type'] == "Admin"):
                    response_object["success"] = False
                    response_object["messages"].append("Permanent and Admin users cannot apply for jobs")
                    return Response(response_object,status=400)
                
                if request.query_params.get('unit_ad_id'):
                    unit_ad_id = request.query_params.get('unit_ad_id')
                else:
                    response_object["success"] = False
                    response_object["messages"].append("Missing data")
                    return Response(response_object,status=400)
                
    

                cursor = connection.cursor()

                # check is user has already applied for this job
                cursor.execute("""SELECT * FROM public.application WHERE user_id = %s AND unit_ad_id = %s;""", [user_id, unit_ad_id])

                if cursor.fetchone() is not None:
                    response_object["success"] = False
                    response_object["messages"].append("User has already applied for this job")
                    return Response(response_object,status=400)

                # Apply to job
                cursor.execute("""INSERT INTO public.application (user_id, unit_ad_id) VALUES(%s,%s);""",[user_id, unit_ad_id])

                if cursor.rowcount < 0:
                    response_object["success"] = False
                    response_object["messages"].append("Job application failed")
                    return Response(response_object,status=400)
                else:
                    response_object["success"] = True
                    response_object["messages"].append("Job applied successfully")
                    return Response(response_object,status=200)
        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=400)
        