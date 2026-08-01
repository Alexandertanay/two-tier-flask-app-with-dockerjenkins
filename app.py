from flask import Flask, render_template, request, redirect, url_for
from db import connection, cursor

app = Flask(__name__)


@app.route("/")
def home():
    cursor.execute("SELECT * FROM feedback ORDER BY id DESC")
    feedbacks = cursor.fetchall()
    return render_template("index.html", feedbacks=feedbacks)


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    feedback = request.form["feedback"]

    sql = "INSERT INTO feedback (name, feedback) VALUES (%s, %s)"
    cursor.execute(sql, (name, feedback))
    connection.commit()

    return redirect(url_for("home"))


@app.route("/health")
def health():
    return {"status": "UP"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)