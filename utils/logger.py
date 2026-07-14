import logging

logger = logging.getLogger('careerpulse')
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Convenience methods
info = logger.info
warning = logger.warning
error = logger.error
debug = logger.debug
