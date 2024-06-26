from HTTP_Client.utilities.request_builder_helpers import (
    api_params_reformat,
    check_api_link,
    check_http_method,
    encode_excel_base_x64,
    check_status,
)


from HTTP_Client.cores.requestMethods.get import Get
from HTTP_Client.cores.requestMethods.del_ import Delete
from HTTP_Client.cores.requestMethods.patch import Patch
from HTTP_Client.cores.requestMethods.put import Put
from HTTP_Client.cores.requestMethods.post import Post


class RequestBuilder:
    def __init__(self, http_method, api):
        self.__http_method: str = check_http_method(http_method)
        self.__api: str = check_api_link(api)
        self.__authentication_token: str = None
        self.__headers = dict()
        self.__parameters = dict()
        self.__body = dict()
        self.__file: str = None

    def bearer_token(self, token: str):
        self.__authentication_token = token
        self.__headers["Authorization"] = (
            "Bearer " + self.__authentication_token.strip()
        )
        return self

    def headers(self, headers: dict):
        for key, val in headers.items():
            if type(key) is str:
                key = key.strip()
            if type(val) is str:
                val = val.strip()
            self.__headers[key] = val
        return self

    def files(self, path):
        self.__file[path] = encode_excel_base_x64(path)
        return self

    def custom_header(self, key, value):
        if type(key) is str:
            key = key.strip()
        if type(value) is str:
            value = value.strip()
        self.__headers[key] = value
        return self

    def parameters(self, parameters: dict):
        self.__parameters = parameters
        self.__api = api_params_reformat(self.__api, self.__parameters)
        return self

    def body(self, body):
        self.__body = body
        return self

    def send(self):
        __request = None
        self.__http_method = self.__http_method.upper()
        if self.__http_method == "GET":
            __request = Get().sendRequest(
                self.__api, json=self.__body, headers=self.__headers
            )
        elif self.__http_method == "POST":
            __request = Post().sendRequest(
                self.__api, json=self.__body, headers=self.__headers, files=self.__file
            )
        elif self.__http_method == "PUT":
            __request = Put().sendRequest(
                self.__api, json=self.__body, headers=self.__headers, files=self.__file
            )
        elif self.__http_method == "PATCH":
            __request = Patch().sendRequest(
                self.__api, json=self.__body, headers=self.__headers, files=self.__file
            )
        elif self.__http_method == "DELETE":
            __request = Delete().sendRequest(
                self.__api, json=self.__body, headers=self.__headers
            )
        print(__request.status_code, check_status(__request.status_code))
        return __request
