import base64
import hashlib
import re
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from api.jwtAuth import generate_auth_token,generate_refresh_token

# Create your views here.
class UserLogin(APIView):
    
    def get(self, request):
        response_object = {
            "success": False,
            "messages": []
        }

        try:
            # get request parameters from header as Baisc then base64 decode it
            auth = request.headers['X-Authorization']
            auth = auth.split(" ")[1]
            

            if(auth == "Og=="):
                raise Exception("Please fill all fields")
            
            auth = base64.b64decode(auth).decode("utf-8")

            if(auth.find(":") == -1):
                raise Exception("Invalid email or password")
            email = auth.split(":")[0]
            password = auth.split(":")[1]

        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=401)
        
        try:
            if email and password:
                # Use sha256 to hash the password
                hashed_password = hashlib.sha256(password.encode()).hexdigest()

                # check if the email and password match
                cursor = connection.cursor()
                cursor.execute("SELECT a.login_email as email,u.user_type,u.user_id,u.authentication_id FROM public.authentication a INNER JOIN public.user u ON a.authentication_id = u.authentication_id WHERE a.login_email = %s and a.user_hashed_password = %s;", [email, hashed_password])
                row = cursor.fetchone()
                user_details = {}
                if row is None:
                    response_object["success"] = False
                    response_object["messages"].append("Invalid email or password")
                    return Response(response_object,status=403)
                else:
                    for i in range(len(row)):
                        user_details[cursor.description[i][0]] = row[i]
                    response_object["success"] = True
                    response_object["messages"].append("Login successful")
                    response_object["data"] = user_details
                    response_object["refresh_token"] = generate_refresh_token(user_details)
                    response_object["auth_token"] = generate_auth_token(user_details)
                    return Response(response_object,status=200)
        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=400)
        
class UserRefreshAuthToken(APIView):
        
    def get(self, request):
        response_object = {
            "success": False,
            "messages": []
        }
        
        try:
            if request.token:
                response_object["success"] = True
                response_object["messages"].append("Token refreshed")
                response_object["auth_token"] = generate_auth_token(request.token)
                return Response(response_object,status=200)
        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=400)
    

class UserSignUp(APIView):
    
    def post(self, request):
        # Get user email, password, and create_password from body
        response_object = {
                "success": False,
                "messages": []
        }

        try:        
            email = request.data['email']
            password = request.data['password']
            create_password = request.data['create_password']
        except:
            response_object["success"] = False
            response_object["messages"].append("Missing data")
            return Response(response_object,status=400)
            

        try:
            # check is all the data exists and is not empty
            if email and password and create_password:
                    
                # check valid email using regex
                if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                    response_object["success"] = False
                    response_object["messages"].append("Invalid email")
                    return Response(response_object,status=400)
                            
                # check if password and create_password are the same
                if password == create_password:
                    # Use sha256 to hash the password
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()

                    # check if the email is already in use
                    cursor = connection.cursor()
                    cursor.execute("SELECT login_email FROM public.authentication WHERE login_email = %s", [email])
                    row = cursor.fetchone()
                    if row is None:
                        # create new user
                        cursor.execute("SELECT create_user(%s, %s);", [email, hashed_password])

                        if cursor.rowcount > 0:
                            response_object["success"] = True
                            response_object["messages"].append("User created successfully")
                            return Response(response_object,status=200)
                        else:
                            response_object["success"] = False
                            response_object["messages"].append("User creation failed")
                            return Response(response_object,status=400)
                    else:
                        response_object["success"] = False
                        response_object["messages"].append("Email already in use")
                        return Response(response_object,status=400)
                else:
                    response_object["success"] = False
                    response_object["messages"].append("Passwords do not match")
                    return Response(response_object,status=400)
            else:
                response_object["success"] = False
                response_object["messages"].append("Please fill all fields")
                return Response(response_object,status=400)   
        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=400)
