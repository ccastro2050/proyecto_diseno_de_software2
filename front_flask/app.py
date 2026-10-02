"""
app.py — El ensamblador del FRONT (Flask + Jinja2).

El front no tiene negocio ni base de datos: rutas que muestran HTML y un
cliente HTTP que habla con la API.

EN ESTA VERSION NO HAY SESION, y es a proposito: la puerta —identificarse, el
token, el 401 y el 403— es la VERSION 3. Hoy cualquiera que llegue a la
direccion entra, y eso es exactamente lo que la v3 arregla. Ponerlo antes
seria anticipar, y le quitaria a la v3 su razon de ser.
"""

import os

from flask import Flask, redirect, render_template, url_for

from entidades import ENTIDADES
from rutas_entidades import bp as bp_entidades
# v2 — el usuario CON SUS ROLES: maestro-detalle con casillas,
# que no cabe en el molde de las vistas genericas.
from rutas_usuarios_roles import bp as bp_usuarios_roles
from rutas_facturas import bp as bp_facturas

app = Flask(__name__)
app.secret_key = os.environ.get("CLAVE_SESION", "clave-solo-para-desarrollo")
app.register_blueprint(bp_entidades)
app.register_blueprint(bp_usuarios_roles)
# v2 — la facturacion maestro-detalle: su propio blueprint, porque no
# es un CRUD. Una factura no se edita: se emite y se anula.
app.register_blueprint(bp_facturas)


@app.context_processor
def menu():
    """El menu, con TODAS las entidades de esta version.

    En la v3 este mismo metodo filtrara por permiso. Hoy no hay a quien
    preguntarle: no hay sesion.
    """
    return {"menu_entidades": ENTIDADES, "hay_sesion": False}


@app.route("/")
def inicio():
    return render_template("inicio.html", entidades=ENTIDADES)


if __name__ == "__main__":
    # debug=True recarga al guardar un .py. Es de DESARROLLO: en un servidor
    # real se usa un servidor WSGI (gunicorn, waitress), nunca este.
    app.run(host="0.0.0.0", port=int(os.environ.get("PUERTO", "8067")), debug=True)
