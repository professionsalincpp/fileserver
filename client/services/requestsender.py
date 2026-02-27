"""
"""
import requests
from .datachecker import DataChecker
from logger import MultiLogger
import http

_logger = MultiLogger("requestsender")

class Sender:
    @classmethod
    def send(cls, data: dict, url: str, method: http.HTTPMethod=http.HTTPMethod.POST) -> requests.Response:
        request_headers = {
            "Content-Type": "application/json",
        }
        if "data" in data.keys():
            request_headers["Content-Length"] = str(len(data["data"]))
        
        try:
            if method == http.HTTPMethod.POST:
                response = requests.post(
                    url,
                    headers=request_headers,
                    json=data
                )
                return response
            if method == http.HTTPMethod.GET:
                response = requests.get(
                    url,
                    headers=request_headers,
                    json=data
                )
                return response
            if method == http.HTTPMethod.PUT:
                response = requests.put(
                    url,
                    headers=request_headers,
                    json=data
                )
                return response
            if method == http.HTTPMethod.DELETE:
                response = requests.delete(
                    url,
                    headers=request_headers,
                    json=data
                )
                return response
        except Exception as e:
            cls.handle_error(e)

    @classmethod
    def handle_error(cls, exception: Exception) -> None:
        if isinstance(exception, requests.exceptions.ConnectionError):
            _logger.error(f"Connection error: {exception}", context="requestsender")
        elif isinstance(exception, requests.exceptions.HTTPError):
            _logger.error(f"HTTP error: {exception}", context="requestsender")
        elif isinstance(exception, requests.exceptions.Timeout):
            _logger.error(f"Timeout error: {exception}", context="requestsender")
        elif isinstance(exception, requests.exceptions.InvalidURL):
            _logger.error(f"Invalid URL: {exception}", context="requestsender")
        else:
            _logger.error(f"Unknown error: {exception}", context="requestsender")