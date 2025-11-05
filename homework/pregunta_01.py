"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    '../files/input/clusters_report.txt'. Los requerimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minúsculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    import pandas as pd
    import re

    # === 1. Leer el archivo completo ===
    with open('files/input/clusters_report.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    # === 2. Limpiar texto y dividir por bloques ===

    text = re.sub(r'-{5,}', '', text) # Eliminar líneas con guiones y separar cada bloque por el número de cluster -{5,}
    bloques = re.split(r'\n\s*(?=\d+\s)', text.strip()) # se usa un lookahead para no perder el número del cluster \n\s*(?=\d+\s)

    data = []

    # === 3. Procesar cada bloque ===
    for bloque in bloques:
        lineas = bloque.strip().split('\n')
        if not lineas:
            continue

        # Extraer datos básicos de la primera línea
        match = re.match(r'\s*(\d+)\s+(\d+)\s+([\d,]+ ?%)\s*(.*)', lineas[0]) 
        if not match:
            continue

        cluster = int(match.group(1))
        cantidad = int(match.group(2))
        porcentaje = match.group(3).replace(',', '.')
        palabras = match.group(4)

        # Si hay más líneas, se unen al texto de palabras clave
        if len(lineas) > 1:
            palabras += ' ' + ' '.join(lineas[1:])

        # Limpieza de espacios y formato de comas
        palabras = re.sub(r'\s+', ' ', palabras).strip()
        palabras = re.sub(r'\s*,\s*', ', ', palabras)  # una coma y un espacio exactos
        palabras = palabras.rstrip('.')

        data.append([cluster, cantidad, porcentaje, palabras])

    # === 4. Crear el DataFrame ===
    df = pd.DataFrame(data, columns=[
        'cluster',
        'cantidad_de_palabras_clave',
        'porcentaje_de_palabras_clave',
        'principales_palabras_clave'
    ])

    # === 5. Ajustar tipos de datos ===
    df['porcentaje_de_palabras_clave'] = (
        df['porcentaje_de_palabras_clave']
        .str.replace('%', '', regex=False)
        .astype(float)
    )

    return df