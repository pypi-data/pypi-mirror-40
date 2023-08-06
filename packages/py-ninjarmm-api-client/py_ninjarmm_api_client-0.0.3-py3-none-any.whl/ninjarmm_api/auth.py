#-*- coding: utf-8 -*-

from requests.auth import AuthBase
from email.utils import formatdate

import base64
import hmac
import hashlib

class auth(AuthBase):

    NINJA_HDR_AUTH = "Authorization"
    NINJA_HDR_DATE = "Date"
    NINJA_ENCODING = "utf-8"


    def __init__(self, accessKeyId, secretAccessKey):
        self.access_key_id = accessKeyId
        self.secret_access_key = secretAccessKey
        self.tstamp = formatdate(timeval=None, localtime=False, usegmt=True)


    def __call__(self, request):
        sts_clear = request.method + "\n"             # HTTP verb
        sts_clear += "\n"                             # Content MD5
        sts_clear += "\n"                             # Content type
        sts_clear += self.tstamp + "\n"               # Date
        sts_clear += request.path_url                 # Canonicalized resource

        sts_base64 = base64.b64encode(sts_clear.encode(self.NINJA_ENCODING))
        sts_digest = hmac.new(self.secret_access_key.encode(self.NINJA_ENCODING), sts_base64, hashlib.sha1)
        signature = base64.b64encode(sts_digest.digest())

        request.headers[self.NINJA_HDR_AUTH] = "NJ " + self.access_key_id + ":" + signature.decode(self.NINJA_ENCODING)
        request.headers[self.NINJA_HDR_DATE] = self.tstamp
        return request


