#!/usr/bin/env python3
"""
main.py
Muestra un capítulo aleatorio del Tao Te Ching en la terminal.

Uso:
    python3 main.py              # Capítulo aleatorio
    python3 main.py --numero 8   # Capítulo específico
    python3 main.py --seccion Tao  # Solo de la sección Tao (1-37)
    python3 main.py --lista      # Lista todos los capítulos disponibles
"""

import argparse
import random
import sys
from pathlib import Path

from parser import cargar_tao
from display import mostrar_capitulo


def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Muestra un capítulo del Tao Te Ching en tu terminal.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--numero", "-n", type=int, default=None,
        help="Número de capítulo específico (1-81). Si se omite, es aleatorio."
    )
    p.add_argument(
        "--seccion", "-s", choices=["Tao", "Te", "tao", "te"],
        default=None,
        help="Filtrar solo por una sección (Tao: 1-37, Te: 38-81)."
    )
    p.add_argument(
        "--lista", "-l", action="store_true",
        help="Lista todos los capítulos disponibles y sale."
    )
    p.add_argument(
        "--archivo", "-a", type=Path, default=None,
        help="Ruta alternativa al archivo taoteching.txt."
    )
    return p


def main() -> int:
    args = construir_parser().parse_args()

    try:
        capitulos = cargar_tao(args.archivo)
    except (FileNotFoundError, ValueError) as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1

    # Filtro por sección
    if args.seccion:
        seccion = args.seccion.capitalize()
        capitulos = [c for c in capitulos if c.seccion == seccion]
        if not capitulos:
            print(f"❌ No hay capítulos en la sección '{seccion}'.",
                  file=sys.stderr)
            return 1

    # Modo lista
    if args.lista:
        print(f"\n📜 Capítulos disponibles ({len(capitulos)}):\n")
        for c in capitulos:
            primera_linea = c.texto.splitlines()[0][:50]
            print(f"  [{c.seccion:>3}] {c.numero:>2}  {primera_linea}...")
        print()
        return 0

    # Selección del capítulo
    if args.numero is not None:
        capitulo = next((c for c in capitulos if c.numero == args.numero), None)
        if capitulo is None:
            print(f"❌ No existe el capítulo {args.numero} en la selección.",
                  file=sys.stderr)
            return 1
    else:
        capitulo = random.choice(capitulos)

    mostrar_capitulo(capitulo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
