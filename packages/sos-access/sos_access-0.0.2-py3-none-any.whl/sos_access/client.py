import logging
import socket
import ssl

from sos_access.exceptions import (IncorrectlyConfigured, InvalidLength,
                                   InvalidXML, WrongContent, NotAuthorized,
                                   NotTreatedNotDistributed,
                                   MandatoryDataMissing, ServiceUnavailable,
                                   DuplicateAlarm, OtherError, XMLHeaderError,
                                   PingToOften, ServerSystemError,
                                   TCPTransportError)
from sos_access.schemas import (AlarmRequestSchema, AlarmRequest,
                                AlarmResponseSchema, PingRequest,
                                PingRequestSchema, PingResponseSchema,
                                NewAuthRequestSchema, NewAuthResponseSchema,
                                NewAuthRequest, PingResponse, AlarmResponse,
                                NewAuthResponse)

from sos_access.decorators import alternating_retry

logger = logging.getLogger(__name__)


# TODO: Implement Point class for different ways of generation a geografical
#       point and use to position.
# TODO: Implement way of adding additionalText to an alarm. List of info?
# TODO: What event codes are there? An official list?
# TODO: Find better description on what Section and detector is used for in the recieiver
# TODO: Document monitored connections
# TODO: add proper logging
# TODO: convert time to utc aware


class SOSAccessClient:
    """
    Client implementing the SOS Access v4 protocol to be used for sending Alarm
    Requests to alarm operators.

    :param transmitter_code:
    :param transmitter_type:
    :param authentication:
    :param receiver_id:
    :param receiver_address:
    :param secondary_receiver_address:
    :param use_single_receiver:
    :param use_tls:
    """
    MAX_RETRY = 3
    ENCODING = 'latin-1'  # it is in the specs only to allow iso-8859-1

    def __init__(self, transmitter_code, transmitter_type, authentication,
                 receiver_id, receiver_address, secondary_receiver_address=None,
                 use_single_receiver=False, use_tls=False):
        self.transmitter_code = transmitter_code
        self.transmitter_type = transmitter_type
        self.authentication = authentication
        self.receiver_id = receiver_id
        self.receiver_address = receiver_address
        self.secondary_receiver_address = secondary_receiver_address
        self.use_single_receiver = use_single_receiver
        self.use_tls = use_tls

        if self.secondary_receiver_address is None and not use_single_receiver:
            raise IncorrectlyConfigured(
                'Both primary and secondary receiver address is needed.')

        # load all schemas so we don't have to remember to do it again.
        self.alarm_request_schema = AlarmRequestSchema()
        self.alarm_response_schema = AlarmResponseSchema()
        self.ping_request_schema = PingRequestSchema()
        self.ping_response_schema = PingResponseSchema()
        self.new_auth_request_schema = NewAuthRequestSchema()
        self.new_auth_response_schema = NewAuthResponseSchema()

    def send_alarm(self, event_code, transmitter_time=None, reference=None,
                   transmitter_area=None, section=None, section_text=None,
                   detector=None, detector_text=None, additional_info=None,
                   position=None) -> AlarmResponse:
        """
        Sends an alarm in the receiver.

        :param event_code:
        :param transmitter_time:
        :param reference:
        :param transmitter_area:
        :param section:
        :param section_text:
        :param detector:
        :param detector_text:
        :param additional_info:
        :param position:
        :return:
        """
        alarm_request = AlarmRequest(event_code=event_code,
                                     transmitter_type=self.transmitter_type,
                                     transmitter_code=self.transmitter_code,
                                     authentication=self.authentication,
                                     receiver=self.receiver_id, alarm_type='AL',
                                     transmitter_time=transmitter_time,
                                     reference=reference,
                                     transmitter_area=transmitter_area,
                                     section=section, section_text=section_text,
                                     detector=detector,
                                     detector_text=detector_text,
                                     additional_info=additional_info,
                                     position=position)

        return self._send_alarm(alarm_request)

    def restore_alarm(self, event_code, transmitter_time=None, reference=None,
                      transmitter_area=None, section=None, section_text=None,
                      detector=None, detector_text=None, additional_info=None,
                      position=None) -> AlarmResponse:
        """
        Restores an alarm in the receiver.

        :param event_code:
        :param transmitter_time:
        :param reference:
        :param transmitter_area:
        :param section:
        :param section_text:
        :param detector:
        :param detector_text:
        :param additional_info:
        :param position:
        :return:
        """
        alarm_request = AlarmRequest(event_code=event_code,
                                     transmitter_type=self.transmitter_type,
                                     transmitter_code=self.transmitter_code,
                                     authentication=self.authentication,
                                     receiver=self.receiver_id, alarm_type='RE',
                                     transmitter_time=transmitter_time,
                                     reference=reference,
                                     transmitter_area=transmitter_area,
                                     section=section, section_text=section_text,
                                     detector=detector,
                                     detector_text=detector_text,
                                     additional_info=additional_info,
                                     position=position)

        return self._send_alarm(alarm_request)

    @alternating_retry
    def _send_alarm(self, alarm_request: AlarmRequest,
                    secondary=False) -> AlarmResponse:
        out_data = self.alarm_request_schema.dump(alarm_request)
        logger.debug(f'Sending: {out_data}')
        in_data = self.transmit(out_data, secondary=secondary)
        logger.debug(f'Received: {in_data}')
        alarm_response = self.alarm_response_schema.load(in_data)
        self._check_response_status(alarm_response)
        print(out_data)
        print(in_data)
        return alarm_response

    def ping(self, reference=None) -> PingResponse:
        """
        Sends a heart beat message to indicate to the alarm operator that
        the alarm device is still operational
        """

        ping_request = PingRequest(authentication=self.authentication,
                                   transmitter_code=self.transmitter_code,
                                   transmitter_type=self.transmitter_type,
                                   reference=reference)
        return self._send_ping(ping_request)

    @alternating_retry
    def _send_ping(self, ping_request: PingRequest,
                   secondary=False) -> PingResponse:
        """
        To send ping request
        """
        out_data = self.ping_request_schema.dump(ping_request)
        logger.debug(f'Sending: {out_data}')
        in_data = self.transmit(out_data, secondary=secondary)
        logger.debug(f'Received: {in_data}')
        ping_response = self.ping_response_schema.load(in_data)
        self._check_response_status(ping_response)
        return ping_response

    def request_new_auth(self, reference=None) -> NewAuthResponse:
        """
        Send a request for new password on the server. This is used so that
        you can have a standard password when deploying devices but it is
        changed to something the alarm installer does not know when the alarm
        is operational
        """

        new_auth_request = NewAuthRequest(authentication=self.authentication,
                                          transmitter_code=self.transmitter_code,
                                          transmitter_type=self.transmitter_type,
                                          reference=reference)

        return self._send_request_new_auth(new_auth_request)

    @alternating_retry
    def _send_request_new_auth(self, new_auth_request: NewAuthRequest,
                               secondary=False) -> NewAuthResponse:
        """
        To send request new auth request
        """
        out_data = self.new_auth_request_schema.dump(new_auth_request)
        logger.debug(f'Sending: {out_data}')
        in_data = self.transmit(out_data, secondary=secondary)
        logger.debug(f'Received: {in_data}')
        new_auth_response = self.new_auth_response_schema.load(in_data)
        self._check_response_status(new_auth_response)
        return new_auth_response

    def transmit(self, data, secondary=False):
        """
        Will create a TCP connection and send the request and received the
        response
        """
        if secondary:
            address = self.secondary_receiver_address
        else:
            address = self.receiver_address

        with TCPTransport(address, secure=self.use_tls) as transport:
            transport.connect()
            transport.send(data.encode(self.ENCODING))
            response = transport.receive().decode(self.ENCODING)
            return response

    @staticmethod
    def _check_response_status(response):
        """
        Checks the status of the response and raise appropriate errors if the
        request wasn't successful.

        :param response:
        """
        # TODO: Test!
        if response.status == 1:
            raise InvalidLength(f'{response.info}: Message is too long.')
        elif response.status == 2:
            raise InvalidXML(f'{response.info}: Invalid XML content.')
        elif response.status == 3:
            raise WrongContent(f'{response.info}: Wrong data content. '
                               f'Ex: too long text in a field.')
        elif response.status == 4:
            raise NotAuthorized(f'{response.info}: Wrong combination of '
                                f'transmitter, instance and password')
        elif response.status == 5:
            # Fail over should kick in.
            raise NotTreatedNotDistributed(f'{response.info}: Error in '
                                           f'processing. It has neither been '
                                           f'treated or distributed')
        elif response.status == 7:
            raise MandatoryDataMissing(f'{response.info}: Mandatory XML tag '
                                       f'missing')
        elif response.status == 9:
            raise ServiceUnavailable(
                (f'{response.info}: Heartbeat is not enabled on the server for '
                 f'this transmitter or you are not authorized to use it.'))
        elif response.status == 10:
            raise DuplicateAlarm(f'{response.info}: The same alarm was received'
                                 f' multiple times')
        elif response.status == 98:
            raise ServerSystemError(f'{response.info}: General receiver error')
        elif response.status == 99:
            # Failover should kick in.
            raise OtherError(f'{response.info}: Unknown receiver error')
        elif response.status == 100:
            raise XMLHeaderError(f'{response.info}: Invalid or missing XML '
                                 f'header')
        elif response.status == 101:
            raise PingToOften(f'{response.info}: Heartbeat is sent too often')


class TCPTransport:

    def __init__(self, address, secure=False, timeout=5):
        self.address = address
        self.timeout = timeout
        self.socket = self._get_socket(secure, timeout)

    def __enter__(self):
        # If we dont do anything in __enter__ we dont have to handle exceptions
        # twice....
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()
        # Catch any error related to the socket and raise as TCP error
        if exc_type in (
                OSError, IOError, ssl.SSLError, socket.error, socket.timeout):
            raise TCPTransportError from exc_type(exc_val, exc_tb)

    def _get_socket(self, secure=False, timeout=None):
        """
        Returns socket. If secure is True the socket is wrapped in an
        SSL Context
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout or self.timeout)

        if secure:
            # Setting Purpose to CLIENT_AUTH might seem a bit backwards. But
            # SOS Access v4 is using SSL/TLS for encryption not authentications
            # and verification. There is no cert and no hostname to check so
            # setting the purpose to Client Auth diables that in a nifty way.
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            return self.context.wrap_socket(sock)

        else:
            return sock

    def connect(self, address=None):
        _address = address or self.address
        self.socket.connect(_address)

    def send(self, data):
        """Send data over socket with correct encoding"""
        self.socket.sendall(data)

    def receive(self):
        """Receive data on socket and decode using correct encoding"""
        data = self.socket.recv(4096)
        return data
