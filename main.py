from flask import Flask, render_template, request, flash
import sqlite3 as sq

app = Flask(__name__)
app.config["SECRET_KEY"] = "giuewrgrt645tdhtr7rstwe4dsgdffh"

menu = [{"name": "Внести данные", "url": "input"}, {"name": "Получить данные", "url": "output"}]

with sq.connect('io_data.db') as con:
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
    user_id TEXT,
    message TEXT
    )''')

@app.route("/")
def main_page():
    return render_template('index.html', menu=menu)

@app.route("/input", methods=['POST', "GET"])
def data_input():
    if request.method == "POST":
        if len(request.form["userID"]) > 0 and len(request.form["message"]) > 0:
            with sq.connect("io_data.db") as con:
                cur = con.cursor()
                cur.execute(f"""INSERT INTO users VALUES("{request.form["userID"]}", "{request.form["message"]}")""")
            flash("Сообщение отправлено.")
        else:
            flash("Заполнены не все поля.")

    return render_template("input.html")

@app.route("/output", methods=['POST', "GET"])
def data_output():
    if request.method == "POST":
        if len(request.form["userID"]) > 0:
            with sq.connect("io_data.db") as con:
                cur = con.cursor()
                cur.execute(f"""SELECT message FROM users WHERE user_id = '{request.form["userID"]}'""")
                message = cur.fetchall()

                if len(message) > 0:
                    message_all = [i[0] for i in message]
                    flash(", ".join(message_all))
                else:
                    flash("Нет такого пользователя или он не оставлял сообщений.")
        else:
            flash("Введите UserID.")
    return render_template("output.html")

@app.route("/<userID>")
def user_output(userID):
    with sq.connect("io_data.db") as con:
        cur = con.cursor()
        cur.execute(f"""SELECT message FROM users WHERE user_id = '{userID}'""")
        message = cur.fetchall()
    if len(message) > 1:
        message_all = [i[0] for i in message]
        return f'<h1>{", ".join(message_all)}</h1>'
    else:
        return "<h1>Нет такого пользователя или он не оставлял сообщений.</h1>"

if __name__ == '__main__':
    app.run(debug=True)