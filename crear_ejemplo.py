"""
Script para crear archivo de ejemplo con datos de prueba
Similar a los datos que arroja el EPAS600
"""

import pandas as pd
from datetime import datetime, timedelta
import random
import os


def crear_archivo_ejemplo():
    """Crea un archivo Excel de ejemplo para pruebas"""

    # Datos de ejemplo basados en la imagen proporcionada
    fechas = []
    horas = []
    co_ppm = []
    no2_ppb = []
    so2_ppb = []
    temp_c = []
    rh = []

    # Generar datos para un día
    fecha_inicio = datetime(2026, 4, 13)
    hora_inicio = datetime(2026, 4, 13, 8, 0, 0)

    for i in range(24):  # 24 horas de datos
        fecha = fecha_inicio + timedelta(hours=i)
        hora = hora_inicio + timedelta(hours=i)

        fechas.append(fecha.strftime("%d/%m/%Y"))
        horas.append(hora.strftime("%H:%M:%S"))

        # CO: valores típicos 0.1 - 0.5 ppm
        co_ppm.append(round(random.uniform(0.1, 0.5), 2))

        # NO2: valores típicos 2 - 21 ppb
        no2_ppb.append(random.randint(2, 21))

        # SO2: valores típicos 1 - 15 ppb
        so2_ppb.append(random.randint(1, 15))

        # Temperatura: 20 - 35°C (variación diaria típica en Panamá)
        temp = 20 + (i % 12) * 1.2 + random.uniform(-2, 2)
        temp_c.append(round(temp, 1))

        # Humedad relativa: 50 - 80%
        rh.append(random.randint(50, 80))

    # Crear DataFrame
    df = pd.DataFrame({
        'Date': fechas,
        'Time': horas,
        'CO': co_ppm,
        'NO2': no2_ppb,
        'SO2': so2_ppb,
        'TmpC': temp_c,
        'RH': rh,
    })

    # Crear directorio si no existe
    os.makedirs('datos', exist_ok=True)

    # Guardar archivo
    ruta_salida = 'datos/ejemplo.xlsx'
    df.to_excel(ruta_salida, index=False, sheet_name='Datos')

    print(f"✓ Archivo de ejemplo creado: {ruta_salida}")
    print(f"  - {len(df)} filas de datos")
    print(f"  - Columnas: {', '.join(df.columns)}")
    print("\nPrimeras 5 filas:")
    print(df.head())

    return df


if __name__ == "__main__":
    crear_archivo_ejemplo()
