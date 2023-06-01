from django.utils.deprecation import MiddlewareMixin
from api.jwtAuth import validate_auth_token,validate_refresh_token
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer



class AuthMiddleware(MiddlewareMixin):
    
    def process_request(self, request):

        if 'login' in request.path[:6] or 'signup' in request.path[:7]:
            return None
        

        auth_header = request.headers.get('X-Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            if auth_token:
                try:
                    if 'refresh' in request.path[:8]:
                        payload = validate_refresh_token(auth_token)
                        if payload and payload['token_type']:
                            if payload['token_type'] == 'refresh':
                                del payload['token_type']
                                request.token = payload
                                return None 
                            else:
                                response = Response({"success": False, "messages": ["Invalid or Expired Refresh Token"]}, status=401)
                                response.accepted_renderer = JSONRenderer()
                                response.accepted_media_type = "application/json"
                                response.renderer_context = {}
                                response.render()
                                return response                           
                        else:
                            response = Response({"success": False, "messages": ["Invalid or Expired Refresh Token"]}, status=401)
                            response.accepted_renderer = JSONRenderer()
                            response.accepted_media_type = "application/json"
                            response.renderer_context = {}
                            response.render()
                            return response
                    else:
                        payload = validate_auth_token(auth_token)
                        if payload:
                            request.token = payload
                            return None
                except Exception as e:
                        response = Response({"success": False, "messages": e.args}, status=401)
                        response.accepted_renderer = JSONRenderer()
                        response.accepted_media_type = "application/json"
                        response.renderer_context = {}
                        response.render()
                        return response
                else:
                    response = Response({"success": False, "messages": ["Invalid or Expired Auth Token"]}, status=401)
                    response.accepted_renderer = JSONRenderer()
                    response.accepted_media_type = "application/json"
                    response.renderer_context = {}
                    response.render()
                    return response
            else:
                response = Response({"success": False, "messages": ["Missing Auth Token"]}, status=401)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
                return response


