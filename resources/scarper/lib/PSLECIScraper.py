from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

import requests
import json


class PSLECIScraper():
    __version__ = '20082018'

    @property
    def _s2l(self):
        return BuiltIn().get_library_instance('Selenium2Library')

    def get_all_states(self):
        #return self._get_all_text('xpath=//*[@id="ddlState"]')
        return ["Karnataka"]

    def get_all_districts(self):
        #return self._get_all_text('xpath=//*[@id="ddlDistrict"]')
        return ["B.B.M.P(CENTRAL)","B.B.M.P(NORTH)","B.B.M.P(SOUTH)","BANGALORE RURAL","BANGALORE URBAN"]

    def get_all_AC(self):
        return self._get_all_text('xpath=//*[@id="ddlAC"]')

    def _get_all_text(self, selector):
        elements = self._s2l.get_webelements(selector)

        texts = []
        for element in elements:
            if element is not None:
                texts.append(element.text)
        texts = texts[0].split('\n')
        texts.remove('-- Select --')
        return texts if texts else None

    def get_polling_station_data(self, value):
        headers = {
                "Accept": "*/*", 
                "Accept-Encoding": "gzip, deflate", 
                "Accept-Language": "en-US,en;q=0.9", 
                "Cache-Control": "no-cache", 
                "Connection": "keep-alive", 
                "Content-Length": "0", 
                "Content-Type": "application/json; charset=UTF-8", 
                "Host": "psleci.nic.in", 
                "Origin": "http://psleci.nic.in", 
                "Pragma": "no-cache", 
                "Referer": "http://psleci.nic.in/Default.aspx", 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
            }
        headers["Cookie"] = "ASP.NET_SessionId=" + value
        json_data = requests.post("http://psleci.nic.in/GService.asmx/GetGoogleObject", headers=json.loads(json.dumps(headers))).json()
        logger.console("Scrapping Polling Station Data")
        logger.console(json_data)
        
        # logger.console(json_data["ToolTip"])
        # logger.console(json_data["Latitude"])
        # logger.console(json_data["Longitude"])
        return json_data