import logging
import threading
from typing import List

logger = logging.getLogger(__name__)


def wait_for_workers(workers: List[threading.Thread], join_timeout=0.1):
    while workers:
        logger.debug("Joining %s", workers[0].name)
        workers[0].join(join_timeout)
        if not workers[0].is_alive():
            del(workers[0])
        else:
            logger.debug("%s is still alive!", workers[0].name)

    return []


def name_from_stdname(prefix: str, thread: threading.Thread):
    return prefix + (next(iter(thread.name.split('-')[1:])) or 'X')
