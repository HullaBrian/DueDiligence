from loguru import logger

from dd.data.main import build_assignments
from dd.sheets.main import export


logger.info("Due Diligence is starting...")
export(*build_assignments())
