import logging

logging.basicConfig(
    level=logging.INFO,  # Set log level to INFO
    format="%(levelname)s:%(name)s:%(message)s",
    handlers=[logging.StreamHandler()],  # Output logs to standard out
)
logger = logging.getLogger("jamie")
