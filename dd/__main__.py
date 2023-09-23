import os

from loguru import logger

from dd.webapp.main import app


logger.info("Due Diligence is starting...")

project_directory: str = f"{os.sep}".join(os.path.realpath(__file__).split(os.sep)[:-1])
try:
    os.mkdir(os.path.join(project_directory, "webapp", "out"))
except FileExistsError:
    pass

app.run(host="127.0.0.1", port=8080, debug=True)
