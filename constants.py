from os import getenv

API_URL = getenv("API_URL")
DEFAULT_QUANTITY = int(getenv("DEFAULT_QUANTITY"))
DEFAULT_PAGE = int(getenv("DEFAULT_PAGE"))
OK_STATUS = 200
CREATED_STATUS = 204
BAD_REQUEST_STATUS = 400
NOT_FOUND_STATUS = 404
NOT_AUTHORIZED_STATUS = 403
SUCCESS_ALERT = {
    "icon": "success",
    "message": "Operación completada satisfactoriamente.",
}
ERROR_ALERT = {"icon": "question", "message": "Ha ocurrido un error desconocido..."}
INCOMPLETE_FORM_ALERT = {
    "icon": "warning",
    "message": "Debes completar todos los campos para continuar...",
}
NOT_AUTHORIZED_ALERT = {
    "icon": "error",
    "message": "Usted no está autorizado a realizar esta acción.",
}
