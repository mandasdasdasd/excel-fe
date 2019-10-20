import hmac, random


class Encryption(object):

    def __init__(self):
        self.key = "bigdata"

    def hmac_md5(self, s):
        return hmac.new(self.key.encode('utf-8'), s.encode('utf-8'), 'MD5').hexdigest()
