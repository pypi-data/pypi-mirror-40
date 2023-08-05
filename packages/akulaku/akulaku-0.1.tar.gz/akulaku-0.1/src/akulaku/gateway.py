"""
Gateway
=======

This module is the primary class for communicating with the AkuLaku API.
"""
import logging
import requests

from akulaku.exceptions import AkuLakuError
from akulaku.helpers import generate_signature

log = logging.getLogger('akulaku')

__all__ = ['AkuLakuGateway', ]


class AkuLakuGateway:

    def __init__(self, app_id, secret_key, use_sandbox=False):
        self.app_id = app_id
        self.secret_key = secret_key
        self.use_sandbox = use_sandbox

    @property
    def base_url(self):
        return "http://testmall.akulaku.com" if self.use_sandbox \
            else "https://mall.akulaku.com"

    def get_redirect_url(self, order_number):
        sign = generate_signature(self.app_id, self.secret_key, order_number)
        params = f'appId={self.app_id}&refNo={order_number}&sign={sign}&lang=id'
        return f'{self.base_url}/v2/openPay.html?{params}'

    def create_order(self, order_request):
        """ Sends a new order to the AkuLaku API

        :param `akulaku.models.NewOrderRequest` order_request:
        :return: the 'OrderId' from AkuLaku.  Needed for subsequent actions.
        :rtype: int
        """
        data = order_request.serialize()

        data.update({
            "appId": self.app_id,
            "sign": generate_signature(self.app_id, self.secret_key, order_request.content)
        })

        try:
            url = f'{self.base_url}/api/json/public/openpay/new.do'
            header = {
                'Content-Type': "application/x-www-form-urlencoded"
            }

            response = requests.post(url, headers=header, data=data)

            json_response = response.json()
            if json_response["success"]:
                return json_response['data']['orderId']
            else:
                raise AkuLakuError(f'AkuLaku return an error: code={json_response.get("errCode")}')

        except Exception:
            log.exception(f"Failed to create new akulaku payment for order {order_request.ref_number}")
            raise

    def get_order(self, order_number):
        try:
            url = f'{self.base_url}/api/json/public/openpay/status.do'
            params = {
                "appId": self.app_id,
                "refNo": str(order_number),
                "sign": self.get_sign(str(order_number))
            }

            response = requests.get(url=url, params=params)
            json_response = response.json()

            if json_response["success"]:
                return json_response['data']
            else:
                log.error(f"Failed to create new akulaku payment for order because data not valid")

        except Exception as e:
            log.exception(f"Failed to create new akulaku payment for order {order_number}")
            raise e
