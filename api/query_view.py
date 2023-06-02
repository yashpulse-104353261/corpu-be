from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response


class Query(APIView):

    def post(self, request):

        response_object = {
            "success": False,
            "messages": []
        }


        try:
            query = request.data['query_text']
        except Exception as e:
            response_object["success"] = False
            response_object["messages"].append("Missing Query")
            return Response(response_object,status=400)

        try:
            if request.token:

                if (request.token['user_type'] != "Admin"):
                    response_object["success"] = False
                    response_object["messages"].append("User does not have permission to query")
                    return Response(response_object,status=400)

                cursor = connection.cursor()
                cursor.execute(query)
                
                if cursor.rowcount == 0:
                    response_object["success"] = False
                    response_object["messages"].append("Query returned no results")
                    return Response(response_object,status=400)

                if cursor.rowcount >= 0:
                    response_object["success"] = True
                    response_object["messages"].append("Query Executed Successfully")
                    response_object["rowcount"] = str(cursor.rowcount) + " Records Affected"
                
                try:
                    row = cursor.fetchall()
                    query_details = []
                except Exception as e:
                    row = None

                if row is None:
                    return Response(response_object,status=200)
                
                for i in range(len(row)):
                    query_detail = {}
                    for j in range(len(row[i])):
                        query_detail[cursor.description[j][0]] = row[i][j]
                    query_details.append(query_detail)
                
                response_object["success"] = True
                response_object["messages"].append("Query results retrieved")
                response_object["data"] = query_details
                return Response(response_object,status=200)


        except Exception as e:
            response_object["success"] = False
            response_object["messages"] = e.args
            return Response(response_object,status=400)
