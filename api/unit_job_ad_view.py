from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response

class UnitJobAd(APIView):
    
    def get(self,request):
            
            response_object = {
                "success": False,
                "messages": []
            }
            
            try:
                if request.token:

                    user_id = request.token['user_id']
                    
                    cursor = connection.cursor()
                    if request.query_params.get('filter'):
                        filter = request.query_params.get('filter')
                        if str.lower(filter) == "all": 
                            cursor.execute("""SELECT uja.unit_ad_id,
                                        uja.unit_id,
                                        uja.convenor_id,
                                        uja.unit_requirements_text,
                                        uja.unit_ad_datetime,
                                        uja.job_ad_status,
                                        uja.unit_ad_datetime,
                                        un.unit_name,
                                        concat(us.user_first_name,' ',us.user_middle_name,' ',us.user_last_name) as convenor_name,
                                        ap.application_status
                                    FROM public.unit_job_advertisement uja 
                                    INNER JOIN public.unit un ON un.unit_id = uja.unit_id 
                                    INNER JOIN public.user us ON us.user_id = uja.convenor_id
                                    LEFT JOIN public.application ap ON ap.user_id =  %s AND ap.unit_ad_id = uja.unit_ad_id AND ap.application_status <> 'Withdrawn' ORDER BY uja.unit_ad_id;""", [user_id])
                        elif str.lower(filter) == "active":
                            cursor.execute("""SELECT uja.unit_ad_id,
                                        uja.unit_id,
                                        uja.convenor_id,
                                        uja.unit_requirements_text,
                                        uja.unit_ad_datetime,
                                        uja.job_ad_status,
                                        uja.unit_ad_datetime,
                                        un.unit_name,
                                        concat(us.user_first_name,' ',us.user_middle_name,' ',us.user_last_name) as convenor_name,
                                        ap.application_status
                                    FROM public.unit_job_advertisement uja
                                    INNER JOIN public.unit un ON un.unit_id = uja.unit_id
                                    INNER JOIN public.user us ON us.user_id = uja.convenor_id
                                    LEFT JOIN public.application ap ON ap.user_id =  %s AND ap.unit_ad_id = uja.unit_ad_id AND ap.application_status <> 'Withdrawn'
                                    WHERE uja.job_ad_status = 'Active' ORDER BY uja.unit_ad_id;""", [user_id])
                        elif str.lower(filter) == "expired":
                            cursor.execute("""SELECT uja.unit_ad_id,
                                        uja.unit_id,
                                        uja.convenor_id,
                                        uja.unit_requirements_text,
                                        uja.unit_ad_datetime,
                                        uja.job_ad_status,
                                        uja.unit_ad_datetime,
                                        un.unit_name,
                                        concat(us.user_first_name,' ',us.user_middle_name,' ',us.user_last_name) as convenor_name,
                                        ap.application_status
                                    FROM public.unit_job_advertisement uja
                                    INNER JOIN public.unit un ON un.unit_id = uja.unit_id
                                    INNER JOIN public.user us ON us.user_id = uja.convenor_id
                                    LEFT JOIN public.application ap ON ap.user_id =  %s AND ap.unit_ad_id = uja.unit_ad_id AND ap.application_status <> 'Withdrawn'
                                    WHERE uja.job_ad_status = 'Expired' ORDER BY uja.unit_ad_id;""", [user_id])
                    else:
                        cursor.execute("""SELECT uja.unit_ad_id,
                                        uja.unit_id,
                                        uja.convenor_id,
                                        uja.unit_requirements_text,
                                        uja.unit_ad_datetime,
                                        uja.job_ad_status,
                                        uja.unit_ad_datetime,
                                        un.unit_name,
                                        concat(us.user_first_name,' ',us.user_middle_name,' ',us.user_last_name) as convenor_name,
                                        ap.application_status
                                    FROM public.unit_job_advertisement uja 
                                    INNER JOIN public.unit un ON un.unit_id = uja.unit_id 
                                    INNER JOIN public.user us ON us.user_id = uja.convenor_id
                                    LEFT JOIN public.application ap ON ap.user_id =  %s AND ap.unit_ad_id = uja.unit_ad_id AND ap.application_status <> 'Withdrawn' ORDER BY uja.unit_ad_id;""", [user_id])

                    row = cursor.fetchall()
                    unit_job_ad_details = []
                    if row is None:
                        response_object["success"] = False
                        response_object["messages"].append("Job retreival failed")
                        return Response(response_object,status=400)
                    else:
                        for i in range(len(row)):
                            unit_job_ad_detail = {}
                            for j in range(len(row[i])):
                                unit_job_ad_detail[cursor.description[j][0]] = row[i][j]
                            unit_job_ad_details.append(unit_job_ad_detail)
                        
                        response_object["success"] = True
                        response_object["messages"].append("Jobs retrieved")
                        response_object["data"] = unit_job_ad_details
                        return Response(response_object,status=200)
            except Exception as e:
                response_object["success"] = False
                response_object["messages"] = e.args
                return Response(response_object,status=400)
            

    def post(self,request):
        response_object = {
            "success": False,
            "messages": []
        }


        try:
            unit_id = request.data["unit_id"]
            unit_requirements_text = request.data["unit_requirements_text"]
            job_ad_status = request.data["job_ad_status"]
            convenor_id = request.data["convenor_id"]
        except Exception as e:
            response_object["success"] = False
            response_object["messages"].append("Please provide all required fields")
            return Response(response_object,status=400)



        try:
            if request.token:
                user_type = request.token['user_type']
                if user_type != "Admin" and user_type != "Permanent":
                    response_object["success"] = False
                    response_object["messages"].append("User does not have permission")
                    return Response(response_object,status=400)
                
                cursor = connection.cursor()
                if request.query_params.get('unit_ad_id'):
                    unit_ad_id = request.query_params.get('unit_ad_id')
                    cursor.execute("""UPDATE public.unit_job_advertisement
                                        SET unit_id=%s, unit_requirements_text=%s, job_ad_status=%s, convenor_id=%s
                                        WHERE unit_ad_id=%s;""",[unit_id,unit_requirements_text,job_ad_status,convenor_id,unit_ad_id])
                    response_object["success"] = True
                    response_object["messages"].append("Job updated")
                    return Response(response_object,status=200)

                cursor.execute("""INSERT INTO public.unit_job_advertisement(
                                    unit_id, unit_requirements_text, job_ad_status, convenor_id,unit_ad_datetime)
                                    VALUES (%s, %s, %s,%s,'NOW()');""",[unit_id,unit_requirements_text,job_ad_status,convenor_id])
                response_object["success"] = True
                response_object["messages"].append("Job created")
                return Response(response_object,status=200)
        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=400)
        