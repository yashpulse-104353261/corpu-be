from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response


class Application(APIView):
    
    def get(self, request):

        response_object = {
            "success": False,
            "messages": []
        }

        try:
            if request.token:
                    
                user_id = request.token['user_id']                                     

                cursor = connection.cursor()

                user_type = request.token['user_type']  

                if user_type == "Permanent":
                    cursor.execute("""SELECT a.application_id,
                    a.unit_ad_id,
                    a.application_datetime,
                    u.user_id,
                    u.user_first_name,
                    u.user_middle_name,
                    u.user_last_name,
                    uja.unit_id,
                    un.unit_name,
                    concat(st.user_first_name,' ',st.user_middle_name,' ',st.user_last_name) as convenor_name,
                    a.application_status
                    FROM public.application a
                    INNER JOIN public.user u on u.user_id = a.user_id
                    INNER JOIN public.unit_job_advertisement uja ON uja.unit_ad_id = a.unit_ad_id
                    INNER JOIN public.unit un ON un.unit_id = uja.unit_id
                    INNER JOIN public.user st ON st.user_id = uja.convenor_id
                    WHERE uja.convenor_id = %s ORDER BY a.application_id DESC;""", [user_id])
                elif user_type == "Admin":
                    cursor.execute("""SELECT a.application_id,
                    a.unit_ad_id,
                    a.application_datetime,
                    u.user_id,
                    u.user_first_name,
                    u.user_middle_name,
                    u.user_last_name,
                    uja.unit_id,
                    un.unit_name,
                    concat(st.user_first_name,' ',st.user_middle_name,' ',st.user_last_name) as convenor_name,
                    a.application_status
                    FROM public.application a
                    INNER JOIN public.user u on u.user_id = a.user_id
                    INNER JOIN public.unit_job_advertisement uja ON uja.unit_ad_id = a.unit_ad_id
                    INNER JOIN public.unit un ON un.unit_id = uja.unit_id
                    INNER JOIN public.user st ON st.user_id = uja.convenor_id
                    ORDER BY a.application_id DESC;""")
                else:              
                # check is user has already applied for this job
                    cursor.execute("""SELECT a.application_id,
                    a.unit_ad_id,
                    a.application_datetime,
                    u.user_id,
                    u.user_first_name,
                    u.user_middle_name,
                    u.user_last_name,
                    uja.unit_id,
                    un.unit_name,
                    concat(st.user_first_name,' ',st.user_middle_name,' ',st.user_last_name) as convenor_name,
                    a.application_status
                    FROM public.application a
                    INNER JOIN public.user u on u.user_id = a.user_id
                    INNER JOIN public.unit_job_advertisement uja ON uja.unit_ad_id = a.unit_ad_id
                    INNER JOIN public.unit un ON un.unit_id = uja.unit_id
                    INNER JOIN public.user st ON st.user_id = uja.convenor_id
                    WHERE a.user_id = %s ORDER BY a.application_id DESC;""", [user_id])

                row = cursor.fetchall()
                applications = []
                if row is None:
                    response_object["success"] = True
                    response_object["messages"].append("No applications found")
                    response_object["data"] = applications
                    return Response(response_object,status=200)
                else:
                    for i in range(len(row)):
                        application = {}
                        for j in range(len(row[i])):
                            application[cursor.description[j][0]] = row[i][j]
                        applications.append(application)
                    
                    response_object["success"] = True
                    response_object["messages"].append("Applications retrieved successfully")
                    response_object["data"] = applications
                    return Response(response_object,status=200)

            else:
                response_object["success"] = False
                response_object["messages"].append("Invalid token")
                return Response(response_object,status=400)
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
            if request.token:


                user_id = request.token['user_id']        

                try:        
                    application_id = request.data['application_id']
                    application_status = request.data['application_status']
                except:
                    response_object["success"] = False
                    response_object["messages"].append("Missing data")
                    return Response(response_object,status=400)            



                if request.token['user_type'] == "Permanent" or request.token['user_type'] == "Admin":
                    
                    # change application status
                    cursor = connection.cursor()
                    
                    cursor.execute("""UPDATE public.application 
                    SET application_status = %s
                    WHERE application_id = %s;""", [application_status, application_id])

                    if application_status == "Successful":
                        cursor.execute("""
                        UPDATE public.user SET user_type = 'Casual' WHERE user_id = (SELECT user_id FROM public.application WHERE application_id = %s);""", [application_id])
                        
                
                else:
                    cursor = connection.cursor()
                    application_status = "Withdrawn"
                    cursor.execute("""UPDATE public.application
                    SET application_status = %s
                    WHERE application_id = %s AND user_id = %s;""", ['Withdrawn', application_id, user_id])

                if cursor.rowcount < 0:
                    response_object["success"] = False
                    response_object["messages"].append("Application status changed")
                    return Response(response_object,status=400)
                else:
                    response_object["success"] = True
                    response_object["messages"].append("Application status changed to "+ application_status)
                    return Response(response_object,status=200)

            else:
                response_object["success"] = False
                response_object["messages"].append("Invalid token")
                return Response(response_object,status=400)
        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=400)
        

