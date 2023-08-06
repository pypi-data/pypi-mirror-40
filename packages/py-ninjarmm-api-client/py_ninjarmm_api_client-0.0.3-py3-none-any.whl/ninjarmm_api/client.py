#-*- coding: utf-8 -*-

import logging
import requests
from urllib.parse import urlparse

from ninjarmm_api.auth import auth

class client(object):

    NINJA_API_US_URLBASE          = "https://api.ninjarmm.com"
    NINJA_API_EU_URLBASE          = "https://eu-api.ninjarmm.com"
    NINJA_API_PING                = "/v1/ping"
    NINJA_API_GET_CUSTOMERS       = "/v1/customers"
    NINJA_API_GET_DEVICES         = "/v1/devices"
    NINJA_API_GET_ALERTS          = "/v1/alerts"
    NINJA_API_GET_ALERTS_SINCE    = "/v1/alerts/since"

    STATUS_PING_OK                = 204
    STATUS_OK                     = 200


    def __init__(self, accessKeyId, secretAccessKey, iseu = False, debug = False):
        self.access_key_id = accessKeyId
        self.secret_access_key = secretAccessKey
        self.baseurl = self.NINJA_API_US_URLBASE if not iseu else self.NINJA_API_EU_URLBASE
        self.debug = debug
        if debug:
            logging.basicConfig(format='%(levelname)s %(asctime)s   %(message)s', level=logging.NOTSET)


    def log_request(self, r):
        logging.debug("--- BEGIN REQUEST ---")
        logging.debug(r.method + " " + r.path_url)
        logging.debug("Host: " + urlparse(r.url).hostname)
        for k, v in r.headers.items():
            logging.debug(k + ": " + v)
        logging.debug("--- END REQUEST ---")


    def log_response(self, r):
        logging.debug("--- BEGIN RESPONSE ---")
        logging.debug("STATUS : " + str(r.status_code))
        logging.debug("HEADERS:\n" + str(r.headers))
        logging.debug("CONTENT:\n" + str(r.content))
        logging.debug("--- END RESPONSE ---")


    def api_get_request(self, uri):
        ses = requests.Session()
        req = requests.Request("GET", self.baseurl + uri,
                                      auth=auth(self.access_key_id, self.secret_access_key))
        preq = req.prepare()
        resp = ses.send(preq)

        if self.debug:
            self.log_request(preq)
            self.log_response(resp)
        return resp


    def ping(self):
        resp = self.api_get_request(self.NINJA_API_PING)
        if not resp.status_code == self.STATUS_PING_OK:
            if self.debug:
                logging.error("PING FAILED!")
            return False

        logging.info("PING was successful")
        return True


    def get_customers(self):
        resp = self.api_get_request(self.NINJA_API_GET_CUSTOMERS)
        if not resp.status_code == self.STATUS_OK:
            return False
        return resp.json()


    def get_customer(self, customer_id):
        resp = self.api_get_request(self.NINJA_API_GET_CUSTOMERS + "/" + str(customer_id))
        if not resp.status_code == self.STATUS_OK:
            return False
        return resp.json()


    def get_devices(self):
        resp = self.api_get_request(self.NINJA_API_GET_DEVICES)
        if not resp.status_code == self.STATUS_OK:
            return False
        return resp.json()


    def get_device(self, device_id):
        resp = self.api_get_request(self.NINJA_API_GET_DEVICES + "/" + str(device_id))
        if not resp.status_code == self.STATUS_OK:
            return False
        return resp.json()


    def get_alerts(self):
        resp = self.api_get_request(self.NINJA_API_GET_ALERTS)
        if not resp.status_code == self.STATUS_OK:
            return False
        return resp.json()


    def get_alerts_since(self, last_known_alert_id):
        resp = self.api_get_request(self.NINJA_API_GET_ALERTS_SINCE + "/" + str(last_known_alert_id))
        if not resp.status_code == self.STATUS_OK:
            return False
        return resp.json()


    def delete_alert(self):
        # not implemented
        pass

