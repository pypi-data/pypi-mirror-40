settings = """settings = {
    "secret_key": "unknown",
    "iss": "Yingde"
}
"""

urlpatterns = """from views import *

urlpatterns=[]
"""

main = """from apigateway.base import Case
from apigateway.event import Event
from apigateway.request import Request
from apigateway.response import Response

from urls import urlpatterns
from settings import db_host, db_name, db_user, db_pass


def handler(event, context):
    # simulate flask request
    with Case(db_host, db_name, db_user, db_pass) as db:
        try:
            request = Request(Event(event), urlpatterns, db)
            # router
            flask_response = request.route()
            # turn flask response to api gateway response
            response = Response(flask_response)
        except Exception as e:
            response = Response(({'error': f"服务器运行错误：{e}"}, 500))
        return response.response

"""
