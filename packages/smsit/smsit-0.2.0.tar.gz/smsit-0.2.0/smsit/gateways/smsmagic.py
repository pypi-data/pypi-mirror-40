
from requests import request
from requests.exceptions import RequestException

from smsit import SMSGateway, SMSGatewayError


class SMSMagicGateway(SMSGateway):
    """
    SMS-Magic

    Documentation: https://api.sms-magic.com/doc/#api-Send_SMS-Send_SMS___get

    Note: BulkSMS not working (returns 404)
    """
    __gateway_name__ = 'sms_magic'
    __config_params__ = ('api_key', 'sender_id')
    _server_url = 'https://api.sms-magic.com/v1/sms/send'

    def send(self, sms):
        headers = {
            'apikey': self.config['api_key'],
            'cache-control': 'no-cache'
        }

        for receiver in sms.receiver:
            payload = {
                'mobile_number': receiver,
                'sms_text': sms.text,
                'sender_id': sms.sender or self.config['sender_id']
            }

            try:
                response = request(
                    'POST', self._server_url, headers=headers, json=payload
                )
                if response.status_code != 200:
                    raise SMSGatewayError('Cannot send sms %s' % sms.__repr__())

            except RequestException:
                raise SMSGatewayError('Cannot send SMS')

        return True
