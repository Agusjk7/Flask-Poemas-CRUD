import requests
from constants import *
from flask import Blueprint, redirect, render_template, request, url_for

views = Blueprint("views", __name__)


@views.route("/create")
def get_create():
    return render_template(
        "create.html", alert=None, values={"author": "", "title": "", "poem": ""}
    )


@views.route("/create", methods=["POST"])
def create():
    try:
        # Obtener valores del formulario y verificar que no estén vacios.
        author, title, poem, secret = request.form.values()
        if "" in [author, title, poem, secret]:
            return render_template(
                "create.html",
                alert=INCOMPLETE_FORM_ALERT,
                values={"author": author, "title": title, "poem": poem},
            )

        # Crear el poema mediante la API y verificar si todo salió bien.
        r = requests.post(
            f"{API_URL}/poem",
            json={
                "author": author,
                "title": title,
                "poem": poem.split("\r\n"),
                "secret": secret,
            },
        )
        if r.status_code == NOT_AUTHORIZED_STATUS:
            return render_template(
                "create.html",
                alert=NOT_AUTHORIZED_ALERT,
                values={"author": author, "title": title, "poem": poem},
            )
        elif r.status_code != CREATED_STATUS:
            raise Exception

        return redirect(url_for("index", alert="success"))
    except:
        return redirect(url_for("index", alert="error"))


@views.route("/<int:id>")
def read(id):
    try:
        # Verificar si el id es válido.
        if id <= 0:
            return redirect(url_for("index"))

        # Verificar si el poema existe.
        r = requests.get(f"{API_URL}/poem/{id}")
        if r.status_code == NOT_FOUND_STATUS:
            return redirect(url_for("index"))
        elif r.status_code != OK_STATUS:
            return redirect(url_for("index", alert="error"))

        # Obtener la información del poema.
        data = r.json()

        return render_template(
            "view.html",
            values={
                "author": data.get("author"),
                "title": data.get("title"),
                "poem": data.get("poem"),
            },
        )
    except:
        return redirect(url_for("index", alert="error"))


@views.route("/<int:id>/edit")
def get_update(id):
    try:
        # Verificar si el id es válido.
        if id <= 0:
            return redirect(url_for("index"))

        # Verificar si el poema existe.
        r = requests.get(f"{API_URL}/poem/{id}")
        if r.status_code == NOT_FOUND_STATUS:
            return redirect(url_for("index"))
        elif r.status_code != OK_STATUS:
            return redirect(url_for("index", alert="error"))

        # Obtener la información del poema.
        data = r.json()

        return render_template(
            "update.html",
            values={"id": id, "author": data.get("author"), "title": data.get("title")},
            poem=data.get("poem"),
        )
    except:
        return redirect(url_for("index", alert="error"))


@views.route("/<int:id>/edit", methods=["POST", "PUT"])
def update(id):
    try:
        # Obtener valores del formulario.
        method, author, title, poem, secret = request.form.values()

        # Verificar que el método sea PUT.
        if request.method == "PUT" or (request.method == "POST" and method == "PUT"):
            # Verificar que los campos no estén vacios.
            if "" in [author, title, poem, secret]:
                return render_template(
                    "update.html",
                    alert=INCOMPLETE_FORM_ALERT,
                    values={
                        "id": id,
                        "author": author,
                        "title": title,
                    },
                    poem=poem.split("\r\n"),
                )

            # Actualizar el poema mediante la API y verificar si todo salió bien.
            r = requests.put(
                f"{API_URL}/poem/{id}",
                json={
                    "author": author,
                    "title": title,
                    "poem": poem.split("\r\n"),
                    "secret": secret,
                },
            )
            if r.status_code == NOT_AUTHORIZED_STATUS:
                return render_template(
                    "update.html",
                    alert=NOT_AUTHORIZED_ALERT,
                    values={
                        "id": id,
                        "author": author,
                        "title": title,
                    },
                    poem=poem.split("\r\n"),
                )
            elif r.status_code != OK_STATUS:
                raise Exception

            return redirect(url_for("index", alert="success"))
        else:
            raise Exception
    except:
        return redirect(url_for("index", alert="error"))


@views.route("/<int:id>/delete")
def get_delete(id):
    try:
        # Verificar si el id es válido.
        if id <= 0:
            return redirect(url_for("index"))

        # Verificar si el poema existe.
        r = requests.get(f"{API_URL}/poem/{id}")
        if r.status_code == NOT_FOUND_STATUS:
            return redirect(url_for("index"))
        elif r.status_code != OK_STATUS:
            return redirect(url_for("index", alert="error"))

        return render_template("delete.html", id=id)
    except:
        return redirect(url_for("index", alert="error"))


@views.route("/<int:id>/delete", methods=["POST", "DELETE"])
def delete_poem(id):
    try:
        # Obtener valores del formulario.
        method, secret = request.form.values()

        # Verificar si el método es DELETE.
        if request.method == "DELETE" or (
            request.method == "POST" and method == "DELETE"
        ):
            # Verificar que la palabra secreta no esté vacía.
            if secret == "":
                return render_template(
                    "delete.html", alert=INCOMPLETE_FORM_ALERT, id=id
                )

            # Eliminar el poema mediante la API y verificar si todo salió bien.
            r = requests.delete(
                f"{API_URL}/poem/{id}", json={"id": id, "secret": secret}
            )
            if r.status_code == NOT_AUTHORIZED_STATUS:
                return render_template("delete.html", alert=NOT_AUTHORIZED_ALERT, id=id)
            elif r.status_code != OK_STATUS:
                raise Exception

            return redirect(url_for("index", alert="success"))
    except:
        return redirect(url_for("index", alert="error"))
