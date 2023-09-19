from loguru import logger

from dd.data.main import build_assignments
from dd.sheets.main import export
from dd.webapp.main import app


logger.info("Due Diligence is starting...")
app.run(host="127.0.0.1", port=8080, debug=True)
#export(*build_assignments())
