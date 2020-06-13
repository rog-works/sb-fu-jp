from datetime import datetime
import logging

from rogw.timezone import Timezone


formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
formatter.converter = lambda *args: datetime.now(tz=Timezone()).timetuple()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)
