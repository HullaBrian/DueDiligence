from threading import Thread

from flask import Flask
from flask import request, escape

from dd.data.main import build_assignments
from dd.sheets.main import export

app = Flask(__name__)


@app.route("/")
def index():
    token = str(escape(request.args.get("token", "")))
    export(*build_assignments())
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


# @app.route("/<token>")
# def generate_spreadsheet(token):
#     export(*build_assignments())
#     return str(token)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
