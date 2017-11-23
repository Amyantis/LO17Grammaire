import logging

logging.basicConfig(
    level=logging.DEBUG,
    datefmt='%H:%M:%S',
    format='%(asctime)s, %(levelname)s:\n%(message)s')
logging.getLogger(__name__)
logger = logging.getLogger()
