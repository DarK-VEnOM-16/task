from rest_framework.renderers import BaseRenderer, JSONRenderer
from rest_framework.utils import json


class CustomApiRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code

        status = True
        message = ""
        response_data = None

        if not str(status_code).startswith("2"):
            status = False
            response_data = data
            if "data" in data:
                response_data = data["data"]

        elif data is not None:
            try:
                status = data["status"]
            except KeyError:
                pass
            try:
                response_data = data["data"]
            except KeyError:
                pass

        try:
            message = data["message"]
        except (TypeError, KeyError):
            message = ""

        response = {
            "status": status,
            "data": response_data,
            "message": message,
        }
        return super().render(response, accepted_media_type, renderer_context)
