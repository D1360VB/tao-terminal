#!/usr/bin/env python3
"""
display.py
Funciones de presentación para mostrar capítulos del Tao Te Ching
en la terminal con estilo.
"""

import shutil
import subprocess
import textwrap
import time


from colorama import Fore, Style, init as colorama_init

# Inicializa colorama (necesario sobre todo en Windows)
colorama_init(autoreset=True)

# Paleta de colores por sección
COLORES = {
    "Tao": Fore.CYAN,
    "Te":  Fore.YELLOW,
}

COLOR_TEXTO = Fore.WHITE + Style.BRIGHT
COLOR_BORDE = Fore.BLUE + Style.DIM
COLOR_RESET = Style.RESET_ALL

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


def mostrar_encabezado(capitulo, con_color: bool = True) -> str:
    """Devuelve el encabezado decorado con la sección y el número."""
    titulo = f"{capitulo.seccion} {capitulo.numero}"
    banner = _toilet(titulo, fuente="big")

    color = COLORES.get(capitulo.seccion, Fore.WHITE) if con_color else ""
    reset = COLOR_RESET if con_color else ""

    lineas = banner.splitlines()
    ancho = max((len(l) for l in lineas), default=40)
    linea_sup = "─" * ancho

    return f"\n{color}{linea_sup}\n{banner}\n{linea_sup}{reset}\n"


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


def mostrar_capitulo(capitulo, con_marco: bool = True,
                     con_color: bool = True,
                     modo_cowsay: bool = False,
                     maquina_escribir: bool = False,
                     velocidad: float = 0.015) -> None:
    encabezado = mostrar_encabezado(capitulo, con_color=con_color)

    if maquina_escribir:
        imprimir_maquina_de_escribir(
            encabezado,
            delay=velocidad / 2,
            color=COLORES.get(capitulo.seccion, "") if con_color else "",
        )
    else:
        print(encabezado)

    cuerpo = formatear_texto(capitulo.texto)
    color_texto = COLOR_TEXTO if con_color else ""

    if modo_cowsay:
        mostrar_con_cowsay(cuerpo, color=color_texto)
        return

    if maquina_escribir:
        imprimir_maquina_de_escribir(cuerpo, delay=velocidad, color=color_texto)
    else:
        if con_marco:
            ancho = ANCHO_TEXTO + 4
            borde = "·" * ancho
            for linea in cuerpo.splitlines():
                print(f"{color_texto}  {linea}{COLOR_RESET}")
            color_borde = COLOR_BORDE if con_color else ""
            print(f"\n{color_borde}{borde}{COLOR_RESET}\n")
        else:
            print(cuerpo)
            print()
        
def imprimir_maquina_de_escribir(texto: str, delay: float = 0.015,
                                  color: str = "") -> None:
    """
    Imprime el texto carácter a carácter simulando una máquina de escribir.

    Args:
        texto: Texto a imprimir.
        delay: Segundos entre caracteres. 0 = instantáneo.
        color: Código de color de colorama (opcional).
    """
    if color:
        print(color, end="", flush=True)

    for caracter in texto:
        print(caracter, end="", flush=True)
        # Pausas ligeramente más largas tras signos de puntuación
        if caracter in ".,;:!?":
            time.sleep(delay * 4)
        elif caracter in "\n":
            time.sleep(delay * 6)
        else:
            time.sleep(delay)

    if color:
        print(COLOR_RESET, end="", flush=True)
    print()  # salto final
