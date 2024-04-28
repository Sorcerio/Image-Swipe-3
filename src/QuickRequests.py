# Image Swipe 3: Quick Requests
# Utility class for making HTTP requests.

# Imports
import requests
from typing import Optional, Any
from requests.exceptions import HTTPError

# Classes
class QuickRequests:
    """
    Utility class for making HTTP requests.

    Adopt as a base class or import and assign functionality.
    """
    # Constants
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"

    # Constructor
    def __init__(self, baseUrl: str = ""):
        """
        baseUrl: The base URL to use for all requests.
        """
        self.baseUrl = baseUrl

    # Functions
    def apiGet(self, endpoint: str, reqArgs: Optional[dict[str, Any]] = None, expectedStatus: Optional[int] = 200) -> requests.Response:
        """
        Makes an API GET Request to the given endpoint.

        endpoint: The endpoint to make API requests to. For example, `sdapi/v1/img2img`.
        reqArgs: A dict of arguments to pass to the `requests.get()` function.
        expectedStatus: The expected status code of the request. If supplied and the request returns a different status code, a `requests.exceptions.HTTPError` error will be raised. If `None` is supplied, no error will be raised for any status code.

        Returns the `requests` Response object.
        """
        return self.__makeRequest(False, endpoint, reqArgs, expectedStatus=expectedStatus)

    def apiPost(self, endpoint: str, reqArgs: Optional[dict[str, Any]] = None, expectedStatus: Optional[int] = 200) -> requests.Response:
        """
        Makes an API POST Request to the given endpoint.

        endpoint: The endpoint to make API requests to. For example, `sdapi/v1/img2img`.
        reqArgs: A dict of arguments to pass to the `requests.post()` function.
        expectedStatus: The expected status code of the request. If supplied and the request returns a different status code, a `requests.exceptions.HTTPError` error will be raised. If `None` is supplied, no error will be raised for any status code.

        Returns the `requests` Response object.
        """
        return self.__makeRequest(True, endpoint, reqArgs, expectedStatus=expectedStatus)

    # Private Functions
    def __makeRequest(self,
        isPost: bool,
        endpoint: str,
        reqArgs: Optional[dict[str, Any]],
        expectedStatus: Optional[int] = 200
    ) -> requests.Response:
        """
        Makes an API GET Request to the given endpoint.

        isPost: If `True`, the request will be a POST request. Otherwise, it will be a GET request.
        endpoint: The endpoint to make API requests to. For example, `sdapi/v1/img2img`.
        reqArgs: A dict of arguments to pass to the `requests.get()` function.
        expectedStatus: The expected status code of the request. If supplied and the request returns a different status code, a `requests.exceptions.HTTPError` error will be raised. If `None` is supplied, no error will be raised for any status code.

        Returns the `requests` Response object.
        """
        # Build the URL
        url = f"{self.baseUrl}/{endpoint}"

        # Scope the request arguments
        if reqArgs == None:
            reqArgs = {}

        # Check for headers
        if "headers" not in reqArgs:
            # Add the user agent
            reqArgs["headers"] = {
                "User-Agent": self.USER_AGENT
            }
        elif "User-Agent" not in reqArgs["headers"]:
            # Add the user agent
            reqArgs["headers"]["User-Agent"] = self.USER_AGENT

        # Watch for connection errors
        try:
            # Make the request
            if isPost:
                req = requests.post(url, **reqArgs)
            else:
                req = requests.get(url, **reqArgs)

            # Check for errors
            if (expectedStatus == None) or (req.status_code == expectedStatus):
                # Good
                return req
            else:
                # Bad
                raise HTTPError(f"Could not connect to: {url}.\nBecause: {req.status_code} recieved (expected {expectedStatus}).")
        except requests.exceptions.ConnectionError as err:
            raise HTTPError(f"Could not connect to: {url}.\nBecause: {err}")

# Command Line
if __name__ == "__main__":
    print("No command line has been implemented for this file.")
