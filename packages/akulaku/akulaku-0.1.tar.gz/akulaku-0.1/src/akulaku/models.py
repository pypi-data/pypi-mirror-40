"""
Models
======

Represent data that is sent to the the AkuLaku APIs as part of a request.
"""
from enum import IntEnum

__all__ = ['AkuLakuStatus', 'OrderDetail', 'NewOrderRequest', ]


class AkuLakuStatus(IntEnum):
    """ The status code for an API response from AkuLaku
    """
    PENDING = 1
    REFUND = 91
    FAILED = 90
    CANCELLED = 92
    SUCCESS = 100
    RECEIPTED = 101


class OrderDetail:
    """ An order line item (generally as part of a `NewOrderRequest`)
    """
    def __init__(self, sku, name, unit_price, quantity):
        """
        :param `str` sku: A product SKU for one of the line items that was ordered.
        :param `str` name: The human-readable name of the product that was ordered.
        :param `int` unit_price: The price per item.
        :param `int` quantity: The number of products that were ordered.
        """
        self.sku = sku
        self.name = name
        self.unit_price = unit_price
        self.quantity = quantity

    def serialize(self):
        """ Converts this object to a string representation, suitable for sending to the AkuLaku API.

        :return: A string representation of this instance.
        :rtype: str
        """
        return (f'[{{"skuId": "{self.sku}", '
                f'"skuName": "{self.name}", '
                f'"unitPrice": {self.unit_price}, '
                f'"qty": {self.quantity}}}]')


class NewOrderRequest:
    """ An order which is sent to the AkuLaku API.
    """
    def __init__(self,
                 ref_number,
                 total_price,
                 user_account,
                 receiver_name,
                 receiver_phone,
                 province,
                 city,
                 street,
                 postcode,
                 details):
        self.ref_number = ref_number
        self.total_price = total_price
        self.user_account = user_account
        self.receiver_name = receiver_name
        self.receiver_phone = receiver_phone
        self.province = province
        self.city = city
        self.street = street
        self.postcode = postcode
        self.details = details if type(details) is str else details.serialize()

    @property
    def content(self):
        """ Generates a stringified verision of this object not for API consumption, but for generating signatures.

        :rtype: str
        """
        # TODO: Fuad -- IS THIS CORRECT??? 'ref_number' twice??
        required_attributes = [
            'ref_number', 'ref_number', 'user_account', 'receiver_name', 'receiver_phone', 'province',
            'city', 'street', 'postcode', 'details',
        ]
        return ''.join([getattr(self, attr) for attr in required_attributes])

    def serialize(self):
        """ Converts this object to a dictionary, suitable for serializing in an HTTP request.

        :return: A dictionary that representation of this class
        :rtype: dict
        """
        return {
            "refNo": self.ref_number,
            "totalPrice": self.total_price,
            "userAccount": self.user_account,
            "receiverName": self.receiver_name,
            "receiverPhone": self.receiver_phone,
            "province": self.province,
            "city": self.city,
            "street": self.street,
            "postcode": self.postcode,
            "details": self.details,
        }
