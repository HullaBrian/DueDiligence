import os
from threading import Thread

from flask import Flask, redirect, url_for, send_from_directory, jsonify
from flask import request, escape
from loguru import logger

from dd.data.main import build_assignments
from dd.sheets.main import export

app = Flask(__name__)


@app.route("/")
def index():
    token = str(escape(request.args.get("token", "")))

    if token:
        logger.info(f"Starting generation for token '{token}'")
        return redirect(url_for('loading', token=token))

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
def loading(token: str):
    export(*build_assignments(token=token))

    return redirect((url_for("done")))


@app.route("/loading/")
def loading_style():
    return (
        """
        <div style="text-align: center;">
            <h1>Loading...</h1>
            <p>Please wait for DueDiligence to finish building your spreadsheet!</p>
        </div>
        """
    )


@app.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir("/home/hullabrian/Documents/Programming/DueDiligence/"):
        path = os.path.join("/home/hullabrian/Documents/Programming/DueDiligence/", filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@app.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory("~", "School.xlsx", as_attachment=True)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
