#!/usr/bin/env python3
"""
parser.py
Lee y parsea el archivo taoteching.txt del Tao Te Ching.
Devuelve una lista de capítulos con su número y sección.
"""

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Capitulo:
    """Representa un capítulo del Tao Te Ching."""
    numero: int
    seccion: str  # "Tao" o "Te"
    texto: str

    def __str__(self) -> str:
        return f"[{self.seccion} {self.numero}]\n{self.texto}"


# Patrón que matchea una línea que es SOLO un número (el número del capítulo)
PATRON_NUMERO = re.compile(r'^\s*(\d+)\s*$')
# Patrón que matchea una línea que es SOLO "Section: X"
PATRON_SECCION = re.compile(r'^\s*Section:\s*(\w+)\s*$', re.IGNORECASE)


def parsear_archivo(ruta: Path) -> list[Capitulo]:
    """
    Lee el archivo y devuelve una lista de objetos Capitulo.

    Args:
        ruta: Path al archivo taoteching.txt

    Returns:
        Lista de Capitulo ordenada por número.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el formato del archivo es inválido.
    """
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    contenido = ruta.read_text(encoding='utf-8')
    lineas = contenido.splitlines()

    capitulos: list[Capitulo] = []
    seccion_actual = "Tao"  # Por defecto, aunque el archivo la declare
    numero_actual: int | None = None
    buffer_texto: list[str] = []

    def cerrar_capitulo():
        """Guarda el capítulo en curso si existe."""
        if numero_actual is not None:
            texto = "\n".join(buffer_texto).strip()
            if texto:  # Solo agregamos si tiene contenido
                capitulos.append(Capitulo(
                    numero=numero_actual,
                    seccion=seccion_actual,
                    texto=texto,
                ))

    for linea in lineas:
        # ¿Es una línea de sección?
        match_seccion = PATRON_SECCION.match(linea)
        if match_seccion:
            cerrar_capitulo()
            seccion_actual = match_seccion.group(1).capitalize()
            numero_actual = None
            buffer_texto = []
            continue

        # ¿Es una línea con solo un número?
        match_numero = PATRON_NUMERO.match(linea)
        if match_numero:
            cerrar_capitulo()
            numero_actual = int(match_numero.group(1))
            buffer_texto = []
            continue

        # Línea normal: acumular si estamos dentro de un capítulo
        if numero_actual is not None:
            buffer_texto.append(linea)

    # No olvidar cerrar el último capítulo
    cerrar_capitulo()

    if not capitulos:
        raise ValueError("El archivo no contiene capítulos válidos.")

    return capitulos


def cargar_tao(ruta: Path | None = None) -> list[Capitulo]:
    if ruta is None:
        # El archivo vive ahora dentro del paquete en data/
        ruta = Path(__file__).parent / "data" / "taoteching.txt"
    return parsear_archivo(ruta)


# Prueba rápida si ejecutas parser.py directamente
if __name__ == "__main__":
    capitulos = cargar_tao()
    print(f"✅ Se cargaron {len(capitulos)} capítulos.\n")
    print(f"Primero: sección={capitulos[0].seccion}, "
          f"número={capitulos[0].numero}")
    print(f"Último:  sección={capitulos[-1].seccion}, "
          f"número={capitulos[-1].numero}")

    # Verifica que la sección cambie correctamente en el 38
    c38 = next((c for c in capitulos if c.numero == 38), None)
    if c38:
        print(f"Capítulo 38 pertenece a la sección: {c38.seccion}")
