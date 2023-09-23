import os

from uuid import uuid4

from flask import Flask, redirect, url_for, send_from_directory
from flask import request, escape
from loguru import logger

from dd.data.main import build_assignments
from dd.sheets.main import export

app = Flask(__name__)
project_directory: str = f"{os.sep}".join(os.path.realpath(__file__).split(os.sep)[:-1])


@app.route("/")
def index():
    token = str(escape(request.args.get("token", "")))

    if token:
        logger.info(f"Starting generation for token '{token}'")
        return redirect(url_for("wait", token=token))

    return (
            """
        <div style="text-align: center;">
            <h1>DueDiligence</h1>
            <form action="" method="get">
                    <input type="text" name="token">
                    <input type="submit" value="Submit">
            </form>
        </div>
        """
            + token
    )


@app.route("/loading/<token>")
def wait(token: str):
    id = uuid4()
    export(*build_assignments(token=token), file_name=os.path.join(project_directory, "out", f"{id}.xlsx"))
    return redirect(url_for("get_file", uuid=id))


@app.route("/completed/<uuid>")
def get_file(uuid: str):
    """Download a file."""
    return send_from_directory(
        os.path.join(project_directory, "out"),
        f"{uuid}.xlsx",
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
