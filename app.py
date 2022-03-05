import json
from os import getenv

import requests
from flask import redirect, render_template, request, url_for

from constants import *
from website import create_app

app = create_app()


@app.route("/")
def index():
    try:
        # Obtener los parámetros de la petición.
        args = json.loads(json.dumps(request.args))

        # Verificar si existe el parámetro de alerta y añadirlo a una variable.
        alert = None
        if "alert" in args:
            alert_type = args.get("alert")
            if alert_type == "success":
                alert = SUCCESS_ALERT
            elif alert_type == "error":
                alert = ERROR_ALERT

        # Verificar y asignar a una variable el parámetro de cantidad.
        try:
            q = (
                DEFAULT_QUANTITY
                if "q" not in args or int(args.get("q")) <= 0
                else int(args.get("q"))
            )
        except:
            q = DEFAULT_QUANTITY

        # Verificar y asignar a una variable el parámetro de página.
        try:
            p = (
                DEFAULT_PAGE
                if "p" not in args or int(args.get("p")) <= 0
                else int(args.get("p"))
            )
        except:
            p = DEFAULT_PAGE

        # Realizar petición a la API y verificar que fue satisfactoria.
        r = requests.get(f"{API_URL}/poems?page={p}&quantity={q}")
        if r.status_code == BAD_REQUEST_STATUS:
            if p == DEFAULT_PAGE:
                raise Exception

            return redirect(url_for("index"))
        elif r.status_code != OK_STATUS:
            raise Exception

        # Obtener la información de los poemas y la siguiente página.
        data = r.json()

        return render_template(
            "index.html",
            alert=alert,
            page=p,
            quantity=q,
            next_page=data.get("next_page"),
            poems=data.get("poems"),
        )
    except:
        return render_template(
            "index.html",
            alert=None,
            page=DEFAULT_PAGE,
            quantity=DEFAULT_QUANTITY,
            next_page=None,
            poems=[],
        )


@app.errorhandler(404)
@app.errorhandler(405)
def error_redirect(e):
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False, port=int(getenv("PORT", 5000)))
