import logging
import ecs-logging
import time

logger = logging.getLogger("grafana-backup-tool")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('/opt/grafana-backup-tool/grafana-backup-tool.log')
handler.setFormatter(ecs_logging.StdlibFormatter())
logger.addHandler(handler)