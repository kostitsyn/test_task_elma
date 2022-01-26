import re
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class BaseApiView(APIView):
    """
    ## Parses the specified addresses and counts the number
    ## of occurrences in the response body of the specified string.
    ### Request body:
        {
             "urls": [
               {"url": "https://python.org", "query": "python"},
               {"url": "https://www.djangoproject.com", "query": "django"},
               {"url": "https://python.org", "query": "python"}
             ],
             "maxTimeout": 3000
        }
    ### Response body:
        {
             "urls": [
               {"url": "https://python.org", "count": 10, "status": "ok"},
               {"url": "https://www.djangoproject.com", "status": "error"},
               {"url": "https://sanic.dev/en/", "count": 20, "status": "ok"}
             ]
        }
    """
    def post(self, request):
        try:
            urls = request.data['urls']
            result = []
            for url_data in urls:
                data = dict()
                data['url'] = url_data['url']
                is_fail = False
                try:
                    response = requests.get(url_data['url'])
                except Exception:
                    is_fail = True
                response_time = response.elapsed.total_seconds()
                if response.status_code == 200 and response_time < request.data['max_timeout'] / 1000 and not is_fail:
                    data['status'] = 'ok'
                    ocurrences_count = len(re.findall(url_data['query'], response.text, re.IGNORECASE))
                    data['count'] = ocurrences_count
                else:
                    data['status'] = 'error'
                result.append(data)
            response = {'urls': result}
            return Response(response)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
