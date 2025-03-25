from django.utils import timezone
import logging

logging.basicConfig(
    filename='ip_logs.log',
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LogIPWriter:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        now = timezone.now()
        ip = request.META.get('REMOTE_ADDR', 'Unknown IP address')
        logger.info(f"{ip}")
        return self.get_response(request)


class BlockIP:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        now = timezone.now()


        return self.get_response(request)