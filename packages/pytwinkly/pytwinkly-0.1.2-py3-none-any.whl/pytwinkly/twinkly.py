import base64, os
import requests

class TwinklyClient:
    def __init__(self, ipaddress):
        self.ipaddress = ipaddress
        self.baseUrl = "http://{}/xled/v1/".format(self.ipaddress)
        self.loginUrl = "{}login".format(self.baseUrl)
        self.verifyUrl = "{}verify".format(self.baseUrl)
        self.modeUrl = "{}led/mode".format(self.baseUrl)
        self.deviceUrl = "{}gestalt".format(self.baseUrl)

        # populated after first request
        self.challenge = None
        self.challenge_response = None
        self.authentication_token = None
    
    def generate_challenge(self):
        """
        Generates random challenge string
        :rtype: str
        """
        return os.urandom(32)

    def send_challenge(self):
        b64_challenge = base64.b64encode(self.challenge).decode("utf-8")
        body = {"challenge": b64_challenge}
        _r = requests.post(self.loginUrl, json=body)
        if _r.status_code != 200:
            return False
        content = _r.json()
        if content[u"code"] != 1000:
            return False
        self.challenge_response = content["challenge-response"]
        self.authentication_token = content["authentication_token"]
        return True

    def send_challenge_response(self):
        headers = {"X-Auth-Token": self.authentication_token}
        body = {u"challenge-response": self.challenge_response}
        _r = requests.post(self.verifyUrl, headers=headers, json=body)
        if _r.status_code != 200:
            return False
        return True
        
    def authenticate(self):
        """Handles user authentication with challenge-response"""

        self.challenge = self.generate_challenge()
        #log.debug("authenticate(): Challenge: %s", repr(self.challenge))
        login_successful = self.send_challenge()
        if not login_successful:
            return False

        verify_successful = self.send_challenge_response()
        if not verify_successful:
            return False

        self.headers = {"X-Auth-Token": self.authentication_token}
        return True
        
    def get_device_info(self):       
        response = requests.get(self.deviceUrl, headers=self.headers)
        return response.json()
        
    def get_mode(self):       
        response = requests.get(self.modeUrl, headers=self.headers)
        return response.json()["mode"]

    def set_mode(self, mode):
        assert mode in ("movie", "demo", "off")
        json_payload = {"mode": mode}
        response = requests.post(self.modeUrl, json=json_payload, headers=self.headers)
        return response.json()

    def turn_on(self):
        return self.set_mode("movie")[u"code"] == 1000

    def turn_off(self):
        return self.set_mode("off")[u"code"] == 1000

    def is_on(self):
        """
        Returns True if device is on
        """
        return self.get_mode() != "off"