import re

from backend.utils import (
    BAD_REQUEST_CODE,
    BAD_REQUEST_CODE_MESSAGE,
    FASES_VALIDAS,
    crear_error,
)


def validar_email(email):
    if not email:
        return ""

    return email


def validar_nombre(nombre):
    if not nombre:
        return ""

    return nombre


def validar_equipo(equipo):
    if not equipo:
        return ""

    return equipo


def validar_fecha(fecha):
    if not fecha:
        return ""

    errores = []
    formato_acceptado = re.compile(r"\d\d\d\d-\d\d-\d\d")
    if not formato_acceptado.fullmatch(fecha):
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                BAD_REQUEST_CODE_MESSAGE,
                f"La fecha: {fecha} no respeta el formato YYYY-MM-DD",
            )
        )
    anio, mes, dia = list(map(int, fecha.split("-")))
    if dia <= 0 or dia > 31:
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                BAD_REQUEST_CODE_MESSAGE,
                f"El dia: {dia} no esta entre 1 y 31",
            )
        )
    if mes > 12 or mes < 1:
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                BAD_REQUEST_CODE_MESSAGE,
                f"El mes: {mes} no esta entre 1 y 12",
            )
        )
    if anio > 9999 or anio < 1000:
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                BAD_REQUEST_CODE_MESSAGE,
                f"El año: {anio} no esta entre 1000 y 9999",
            )
        )

    if len(errores) > 0:
        raise RuntimeError(errores)

    return fecha


def validar_fase(fase_cruda):
    if not fase_cruda:
        return ""

    fase = fase_cruda.lower()

    errores = []
    if fase not in FASES_VALIDAS:
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                BAD_REQUEST_CODE_MESSAGE,
                f"La fase: {fase} no esta entre {FASES_VALIDAS}",
            )
        )

    if len(errores) > 0:
        raise RuntimeError(errores)

    return fase


def validar_limit(limit_crudo):
    if not limit_crudo:
        return 10

    limit = int(limit_crudo)

    errores = []
    if limit <= 0:
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                BAD_REQUEST_CODE_MESSAGE,
                f"El limit: {limit} no es mayor a 0",
            )
        )

    if len(errores) > 0:
        raise RuntimeError(errores)

    return limit


def validar_offset(offset_crudo):
    if not offset_crudo:
        return 0

    offset = int(offset_crudo)

    errores = []
    if offset < 0:
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                BAD_REQUEST_CODE_MESSAGE,
                f"El offset: {offset} es menor a 0",
            )
        )

    if len(errores) > 0:
        raise RuntimeError(errores)

    return offset


def validar_partido(partido):
    errores = []
    if not validar_equipo(partido.get("equipo_local")):
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                BAD_REQUEST_CODE_MESSAGE,
                "equipo_local no puede estar vacio",
            )
        )
    if not validar_equipo(partido.get("equipo_visitante")):
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                BAD_REQUEST_CODE_MESSAGE,
                "equipo_visitante no puede estar vacio",
            )
        )
    fecha = partido.get("fecha")
    if not validar_fecha(fecha):
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                BAD_REQUEST_CODE_MESSAGE,
                "fecha no puede estar vacio",
            )
        )
    fase = partido.get("fase")
    if not validar_fase(fase):
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                BAD_REQUEST_CODE_MESSAGE,
                "fase no puede estar vacio",
            )
        )

    if len(errores) > 0:
        raise RuntimeError(errores)

    return partido


def validar_usuario(usuario):
    errores = []
    if not validar_email(usuario.get("email")):
        errores.append(
            crear_error(
                BAD_REQUEST_CODE, BAD_REQUEST_CODE_MESSAGE, "email no puede estar vacío"
            )
        )
    if not validar_nombre(usuario.get("nombre")):
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                BAD_REQUEST_CODE_MESSAGE,
                "nombre no puede estar vacio",
            )
        )

    if len(errores) > 0:
        raise RuntimeError(errores)

    return usuario


def validar_goles_equipo_local(goles_equipo_local_crudo):
    if not goles_equipo_local_crudo:
        return ""

    goles_equipo_local = int(goles_equipo_local_crudo)

    if goles_equipo_local < 0:
        raise RuntimeError(
            [
                crear_error(
                    BAD_REQUEST_CODE,
                    BAD_REQUEST_CODE_MESSAGE,
                    f"goles_equipo_local: {goles_equipo_local} es menor a 0",
                )
            ]
        )

    return goles_equipo_local


def validar_goles_equipo_visitante(goles_equipo_visitante_crudo):
    if not goles_equipo_visitante_crudo:
        return ""

    goles_equipo_visitante = int(goles_equipo_visitante_crudo)

    if goles_equipo_visitante < 0:
        raise RuntimeError(
            [
                crear_error(
                    BAD_REQUEST_CODE,
                    BAD_REQUEST_CODE_MESSAGE,
                    f"goles_equipo_visitante: {goles_equipo_visitante} es menor a 0",
                )
            ]
        )

    return goles_equipo_visitante


def validar_resultado(resultado):
    errores = []
    if not validar_goles_equipo_local(resultado.get("local")):
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                BAD_REQUEST_CODE_MESSAGE,
                "local no puede estar vacío",
            )
        )
    if not validar_goles_equipo_visitante(resultado.get("visitante")):
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                BAD_REQUEST_CODE_MESSAGE,
                "visitante no puede estar vacío",
            )
        )

    if len(errores) > 0:
        raise RuntimeError(errores)

    return resultado


def validar_id(id_crudo):
    if not id_crudo:
        raise RuntimeError(
            [
                crear_error(
                    BAD_REQUEST_CODE,
                    BAD_REQUEST_CODE_MESSAGE,
                    f"El id: {id_crudo} no es valido",
                )
            ]
        )

    id = int(id_crudo)

    if id <= 0:
        raise RuntimeError(
            [
                crear_error(
                    BAD_REQUEST_CODE,
                    BAD_REQUEST_CODE_MESSAGE,
                    f"El id: {id} es menor a 0",
                )
            ]
        )

    return id
