from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/content/<subor>")
def obsah(subor):
    try:
        return send_from_directory("content", f"{subor}.html")
    except:
        return "Obsah sa nenašiel", 404


if __name__ == "__main__":
    app.run(debug=True)
