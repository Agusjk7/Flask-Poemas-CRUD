from flask import request, redirect, url_for, render_template
from json import dumps, loads
from requests import get
from os import getenv
from website import create_app
from constants import *

app = create_app()

@app.route("/")
def index():
    try:
        # Obtener los parámetros de la petición.
        args = loads(dumps(request.args))

        # Verificar si existe el parámetro de alerta y añadirlo a una variable.
        if "alert" not in args: alert = None
        else:
            if args["alert"] == "success": alert = SUCCESS_ALERT
            elif args["alert"] == "error": alert = ERROR_ALERT
            else: alert = None

        # Verificar y asignar a una variable el parámetro de cantidad.
        try: q = DEFAULT_QUANTITY if "q" not in args or int(args["q"]) <= 0 else int(args["q"])
        except: q = DEFAULT_QUANTITY

        # Verificar y asignar a una variable el parámetro de página.
        try: p = DEFAULT_PAGE if "p" not in args or int(args["p"]) <= 0 else int(args["p"])
        except: p = DEFAULT_PAGE

        # Realizar petición a la API y verificar que fue satisfactoria.
        r = get(f"{API_URL}/poems?page={p}&quantity={q}")
        if r.status_code == BAD_REQUEST_STATUS:
            if p == DEFAULT_PAGE: raise Exception

            return redirect(url_for("index"))
        elif r.status_code != OK_STATUS:
            raise Exception

        # Obtener la información de los poemas y la siguiente página.
        data = r.json()

        return render_template("index.html", alert=alert, page=p, quantity=q, next_page=data["next_page"], poems=data["poems"])
    except:
        return render_template("index.html", alert=alert, page=p, quantity=q, next_page=None, poems=[])

@app.errorhandler(404)
@app.errorhandler(405)
def error_redirect(e):
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=False, port=int(getenv("PORT", 5000)))