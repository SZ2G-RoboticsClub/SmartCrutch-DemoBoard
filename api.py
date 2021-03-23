from urequests import urequests

class CrutchClient(object):
    def __init__(self, root_url="127.0.0.1"):
        self.root_url = root_url
        self.session = urequests.Session()

    def heartbeat(self, uuid: str, battery: int,
                  loc_status: str, longitude: float, latitude: float) -> bool:
        """Send heartbeat pkg, interval: 20 times per min
        """
        url = self.root_url + "/api/demoboard/heartbeat"
        headers = {'uuid': uuid}
        data = {}