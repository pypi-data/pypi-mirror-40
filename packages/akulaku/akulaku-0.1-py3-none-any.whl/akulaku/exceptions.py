"""
Exceptions
==========

Specialized error types raised from AkuLaku.
"""
__all__ = ['AkuLakuError', ]


class AkuLakuError(Exception):
    """ Raised when the AkuLaku API
    """
    def __eq__(self, other):
        if type(other) != type(self):
            return False
        elif other.args == self.args:
            return True
        return False
