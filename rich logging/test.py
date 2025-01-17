import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


log = logging.getLogger("rich")
log.info("Info")
log.debug("Debug")
log.warning("Warning")
log.error("Error")
log.fatal("Fatal")
