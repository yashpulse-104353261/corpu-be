from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response

class Profile(APIView):

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
                cursor.execute("""SELECT user_id,
                            user_first_name,
                            user_middle_name,
                            user_last_name,
                            user_street_address,
                            user_city,
                            user_state,
                            user_postcode,
                            user_email,
                            user_phone,
                            user_type
                        FROM public.user WHERE user_id = %s;""", [user_id])
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
                    response_object["messages"].append("User profile retrieved")
                    response_object["data"] = user_profile
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
            first_name = request.data['first_name']
            middle_name = request.data['middle_name']
            last_name = request.data['last_name']
            street_address = request.data['street_address']
            city = request.data['city']
            state = request.data['state']
            postcode = request.data['postcode']
            phone = request.data['phone']
        except Exception as e:
            response_object["success"] = False
            response_object["messages"].append("Missing data")
            return Response(response_object,status=400)
        
        if(first_name is None or first_name == ""):
            response_object["success"] = False
            response_object["messages"].append("First name is required")
            return Response(response_object,status=400)
        if(last_name is None or last_name == ""):
            response_object["success"] = False
            response_object["messages"].append("Last name is required")
            return Response(response_object,status=400)
        if(street_address is None or street_address == ""):
            response_object["success"] = False
            response_object["messages"].append("Street address is required")
            return Response(response_object,status=400)
        if(city is None or city == ""):
            response_object["success"] = False
            response_object["messages"].append("City is required")
            return Response(response_object,status=400)
        if(state is None or state == ""):
            response_object["success"] = False
            response_object["messages"].append("State is required")
            return Response(response_object,status=400)
        if(postcode is None or postcode == ""):
            response_object["success"] = False
            response_object["messages"].append("Postcode is required")
            return Response(response_object,status=400)
        if(phone is None or phone == ""):
            response_object["success"] = False
            response_object["messages"].append("Phone is required")
            return Response(response_object,status=400)
        


        try:
            if request.token:
                user_id = request.token['user_id']
                cursor = connection.cursor()
                cursor.execute(""" UPDATE public.user
                    SET user_first_name = %s,
                        user_middle_name = %s,
                        user_last_name = %s,
                        user_street_address = %s,
                        user_city = %s,
                        user_state = %s,
                        user_postcode = %s,
                        user_phone = %s
                    WHERE user_id = %s;
                """, [first_name, middle_name, last_name, street_address, city, state, postcode, phone, user_id])
                if cursor.rowcount < 0:
                    response_object["success"] = False
                    response_object["messages"].append("User does not exsist")
                    return Response(response_object,status=400)
                else:
                    response_object["success"] = True
                    response_object["messages"].append("User profile updated")
                    return Response(response_object,status=200)
        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=400)
        
        



