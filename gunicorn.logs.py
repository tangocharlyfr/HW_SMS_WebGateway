import logging
import gunicorn

def when_ready(server):
    logger = logging.getLogger("gunicorn.error")
    logger.info(f"🦄 Gunicorn est UP")

def post_fork(server, worker):
    logger = logging.getLogger("gunicorn.error")
    logger.info("✅ La passerelle SMS est prête !")
