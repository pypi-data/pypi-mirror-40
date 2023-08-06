
from smsit import SMSGateway


class DummyGateway(SMSGateway):  # pragma: nocover
    """
    Dummy Gateway

    """
    __gateway_name__ = 'dummy'
    __config_params__ = ('api_key',)

    def send(self, sms):
        print('SMS Sent from dummy gateway, ', sms.__repr__())
        return True
