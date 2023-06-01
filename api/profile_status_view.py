from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response

class ProfileStatus(APIView):

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
                cursor.execute("""SELECT CAST((CAST(SUM(totalCompleted) AS DECIMAL)/9)*100 AS INTEGER) as profile_completion_percentage
                        ,CASE WHEN CAST((CAST(SUM(totalCompleted) AS DECIMAL)/9)*100 AS INTEGER) = 100 THEN true ELSE false END as is_profile_completed
                          FROM (SELECT
                            first_name_exists + last_name_exists + street_address_exists + city_exists + state_exists + postcode_exists + email_exists + cv_exists as totalCompleted
                            FROM
                            (SELECT Case WHEN u.user_first_name IS NULL OR trim(u.user_first_name) = '' THEN 0 ELSE 1 END as first_name_exists,
                                Case WHEN u.user_last_name IS NULL OR trim(u.user_last_name) = '' THEN 0 ELSE 1 END as last_name_exists,
                                Case WHEN u.user_street_address IS NULL OR trim(u.user_street_address) = '' THEN 0 ELSE 1 END as street_address_exists,
                                Case WHEN u.user_city IS NULL OR trim(u.user_city) = '' THEN 0 ELSE 1 END as city_exists,
                                Case WHEN u.user_state IS NULL OR trim(u.user_state) = '' THEN 0 ELSE 1 END as state_exists,
                                Case WHEN u.user_postcode IS NULL OR trim(u.user_postcode) = '' THEN 0 ELSE 1 END as postcode_exists,
                                Case WHEN u.user_email IS NULL OR trim(u.user_email) = '' THEN 0 ELSE 1 END as email_exists,
                                Case WHEN u.user_cv IS NULL OR trim(u.user_cv) = '' THEN 0 ELSE 1 END as cv_exists
                            FROM public.user u
                            WHERE user_id = %s) as ud
                            UNION ALL
                            SELECT 1 as totalCompleted FROM public.availability a
                            WHERE a.user_id = %s LIMIT 2) as profileCompletionStatus;""", [user_id,user_id])
                row = cursor.fetchone()
                user_profile = {}
                if row is None:
                    response_object["success"] = False
                    response_object["messages"].append("User does not exsist")
                    return Response(response_object,status=400)
                else:
                    for i in range(len(row)):
                        user_profile[cursor.description[i][0]] = row[i]
                    response_object["success"] = True
                    response_object["messages"].append("Profile Completion Status Retrieved")
                    response_object["data"] = user_profile
                    return Response(response_object,status=200)
        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=400)
        
