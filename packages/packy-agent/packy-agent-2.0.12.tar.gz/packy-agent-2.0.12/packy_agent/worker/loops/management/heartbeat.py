import logging

import packy_agent
from packy_agent.configuration.settings import settings
from packy_agent.worker.loops.base.periodic import PeriodicLoop
from packy_agent.clients.packy_server import get_packy_server_client
from packy_agent.constants import HEARTBEAT_LOOP
from packy_agent.utils.network import get_actual_ip_address

logger = logging.getLogger(__name__)


def send_heartbeat():
    if not settings.is_worker_heartbeat_enabled():
        logger.debug('Heartbeat is disabled')
        return

    try:
        get_packy_server_client().update_status(version=packy_agent.__version__,
                                                ip_address=get_actual_ip_address())
    except Exception:
        logger.warning('Error while sending heartbeat', exc_info=True)


class HeartbeatLoop(PeriodicLoop):

    formal_name = HEARTBEAT_LOOP

    def __init__(self, period):
        super().__init__(period=period, callable_=send_heartbeat)
