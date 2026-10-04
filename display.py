#!/usr/bin/env python3
"""
display.py
Funciones de presentación para mostrar capítulos del Tao Te Ching
en la terminal con estilo.
"""

import shutil
import subprocess
import textwrap


# Ancho máximo del texto (para que se vea elegante en la terminal)
ANCHO_TEXTO = 60


def _tiene_comando(nombre: str) -> bool:
    """Verifica si un comando está disponible en el sistema."""
    return shutil.which(nombre) is not None


def _toilet(texto: str, fuente: str = "big", filtro: str | None = None) -> str:
    """
    Genera arte ASCII con toilet. Si toilet no está instalado, devuelve
    el texto con un formato simple de fallback.
    """
    if not _tiene_comando("toilet"):
        # Fallback: decorar con caracteres simples
        return f"╔{'═' * (len(texto) + 4)}╗\n║  {texto}  ║\n╚{'═' * (len(texto) + 4)}╝"

    cmd = ["toilet", "-f", fuente]
    if filtro:
        cmd += ["-F", filtro]
    cmd.append(texto)
    try:
        resultado = subprocess.run(
            cmd, capture_output=True, text=True, check=True
        )
        return resultado.stdout.rstrip("\n")
    except subprocess.CalledProcessError:
        return texto


def mostrar_encabezado(capitulo) -> str:
    """Devuelve el encabezado decorado con la sección y el número."""
    titulo = f"{capitulo.seccion} {capitulo.numero}"
    banner = _toilet(titulo, fuente="big")

    # Marco con algunos símbolos estéticos
    ancho = max(len(linea) for linea in banner.splitlines()) if banner else 40
    linea_sup = "─" * ancho
    return f"\n{linea_sup}\n{banner}\n{linea_sup}\n"


def formatear_texto(texto: str, ancho: int = ANCHO_TEXTO) -> str:
    """
    Envuelve el texto para que no exceda el ancho indicado,
    conservando los saltos de línea originales entre estrofas.
    """
    parrafos = texto.split("\n\n")
    formateados = []
    for parrafo in parrafos:
        # Unir líneas del párrafo en un solo bloque y re-envolver
        lineas = [l.strip() for l in parrafo.splitlines() if l.strip()]
        bloque = " ".join(lineas)
        envuelto = textwrap.fill(bloque, width=ancho)
        formateados.append(envuelto)
    return "\n\n".join(formateados)


def mostrar_capitulo(capitulo, con_marco: bool = True) -> None:
    """Imprime un capítulo completo con estilo en la terminal."""
    encabezado = mostrar_encabezado(capitulo)
    cuerpo = formatear_texto(capitulo.texto)

    if con_marco:
        ancho = ANCHO_TEXTO + 4
        borde = "·" * ancho
        print(encabezado)
        for linea in cuerpo.splitlines():
            print(f"  {linea}")
        print(f"\n{borde}\n")
    else:
        print(encabezado)
        print(cuerpo)
        print()
