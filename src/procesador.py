"""
Módulo para procesamiento de archivos Excel
Lectura, conversión y exportación de datos de calidad de aire
"""

import pandas as pd
import numpy as np
from pathlib import Path
from src.conversiones import ConversorCalidadAire
from src.validacion import ValidadorCalidadAire


class ProcesadorExcel:
    """
    Procesador de archivos Excel con datos de calidad de aire
    Detecta columnas automáticamente, convierte datos y exporta resultados
    """

    # Posibles nombres de columnas (case-insensitive)
    COLUMNAS_CONOCIDAS = {
        'co': ['CO', 'co', 'Co', 'C.O.', 'Carbon Monoxide', 'Monóxido de Carbono'],
        'no2': ['NO2', 'no2', 'No2', 'N.O2', 'Nitrogen Dioxide', 'Dióxido de Nitrógeno'],
        'so2': ['SO2', 'so2', 'So2', 'S.O2', 'Sulfur Dioxide', 'Dióxido de Azufre'],
        'o3': ['O3', 'o3', 'O₃', 'Ozone', 'Ozono'],
        'co2': ['CO2', 'co2', 'Co2', 'C.O2', 'Carbon Dioxide', 'Dióxido de Carbono'],
        'temperatura': ['TmpC', 'Tmp', 'Temperatura', 'temperatura', 'Temp', 'T', 'Degree C', '°C'],
        'humedad': ['RH', 'rh', 'Humedad', 'humedad', 'Humidity', 'HR', 'H.R'],
        'fecha': ['Date', 'date', 'Fecha', 'fecha', 'DATA'],
        'hora': ['Time', 'time', 'Hora', 'hora', 'HORA'],
    }

    def __init__(self):
        """
        Inicializa el procesador
        """
        self.conversor = ConversorCalidadAire()
        self.validador = ValidadorCalidadAire()
        self.df_original = None
        self.df_procesado = None
        self.mapeo_columnas = {}
        self.errores = []
        self.advertencias = []

    def leer_excel(self, ruta_archivo):
        """
        Lee archivo Excel
        
        Parámetros:
        -----------
        ruta_archivo : str
            Ruta del archivo Excel
            
        Retorna:
        --------
        tuple (bool, str, DataFrame o None)
            (éxito, mensaje, dataframe)
        """
        try:
            ruta = Path(ruta_archivo)
            if not ruta.exists():
                return False, f"Archivo no encontrado: {ruta_archivo}", None
            
            self.df_original = pd.read_excel(ruta_archivo)
            
            if self.df_original.empty:
                return False, "El archivo está vacío", None
            
            # Detectar columnas
            self._detectar_columnas()
            
            return True, f"Archivo cargado exitosamente ({len(self.df_original)} filas)", self.df_original
        
        except Exception as e:
            return False, f"Error al leer Excel: {str(e)}", None

    def _detectar_columnas(self):
        """
        Detecta automáticamente las columnas del DataFrame
        """
        self.mapeo_columnas = {}
        
        for tipo_gas, posibles_nombres in self.COLUMNAS_CONOCIDAS.items():
            for col in self.df_original.columns:
                if col in posibles_nombres:
                    self.mapeo_columnas[tipo_gas] = col
                    break

    def obtener_columna(self, tipo_gas):
        """
        Obtiene la columna mapeada para un gas
        
        Parámetros:
        -----------
        tipo_gas : str
            Tipo de gas ('co', 'no2', 'so2', etc.)
            
        Retorna:
        --------
        str o None
            Nombre de la columna, o None si no se encontró
        """
        return self.mapeo_columnas.get(tipo_gas)

    def establecer_columna(self, tipo_gas, nombre_columna):
        """
        Establece manualmente el mapeo de una columna
        
        Parámetros:
        -----------
        tipo_gas : str
            Tipo de gas
        nombre_columna : str
            Nombre de la columna en el DataFrame
        """
        if nombre_columna in self.df_original.columns:
            self.mapeo_columnas[tipo_gas] = nombre_columna
        else:
            raise ValueError(f"Columna '{nombre_columna}' no encontrada en el archivo")

    def convertir_datos(self):
        """
        Realiza conversiones de unidades para todos los gases
        
        Retorna:
        --------
        tuple (bool, str, DataFrame o None)
            (éxito, mensaje, dataframe con resultados)
        """
        if self.df_original is None:
            return False, "No hay datos cargados", None
        
        try:
            # Copiar dataframe original
            self.df_procesado = self.df_original.copy()
            
            # Obtener columnas necesarias
            col_temp = self.obtener_columna('temperatura')
            
            if col_temp is None:
                return False, "Columna de temperatura no encontrada", None
            
            # Procesar cada gas
            self._procesar_gas('co', 'ppm', 'CO_ug_m3')
            self._procesar_gas('no2', 'ppb', 'NO2_ug_m3')
            self._procesar_gas('so2', 'ppb', 'SO2_ug_m3')
            self._procesar_gas('o3', 'ppb', 'O3_ug_m3')
            self._procesar_gas('co2', 'ppm', 'CO2_ug_m3')
            
            return True, "Conversión completada exitosamente", self.df_procesado
        
        except Exception as e:
            return False, f"Error en conversión: {str(e)}", None

    def _procesar_gas(self, tipo_gas, unidad_entrada, nombre_columna_salida):
        """
        Procesa conversión para un gas específico
        
        Parámetros:
        -----------
        tipo_gas : str
            Tipo de gas ('co', 'no2', 'so2', etc.)
        unidad_entrada : str
            Unidad de entrada ('ppm' o 'ppb')
        nombre_columna_salida : str
            Nombre para la columna de salida
        """
        col_gas = self.obtener_columna(tipo_gas)
        col_temp = self.obtener_columna('temperatura')
        
        if col_gas is None or col_temp is None:
            return
        
        if col_gas not in self.df_procesado.columns:
            return
        
        # Determinar función de conversión
        if unidad_entrada == 'ppm':
            func = getattr(self.conversor, f'{tipo_gas}_ppm_a_ug_m3', None)
        else:
            func = getattr(self.conversor, f'{tipo_gas}_ppb_a_ug_m3', None)
        
        if func is None:
            return
        
        # Aplicar conversión
        resultados = []
        for idx, row in self.df_procesado.iterrows():
            try:
                valor = row[col_gas]
                temp = row[col_temp]
                
                # Validar valores
                if pd.isna(valor) or pd.isna(temp):
                    resultados.append(np.nan)
                    continue
                
                valor_float = float(valor)
                temp_float = float(temp)
                
                # Convertir
                resultado = func(valor_float, temp_float)
                resultados.append(resultado)
            
            except (ValueError, TypeError):
                resultados.append(np.nan)
        
        # Agregar columna de salida
        self.df_procesado[nombre_columna_salida] = resultados

    def obtener_estadisticas(self, columna):
        """
        Calcula estadísticas para una columna
        
        Parámetros:
        -----------
        columna : str
            Nombre de la columna
            
        Retorna:
        --------
        dict
            Diccionario con estadísticas
        """
        if self.df_procesado is None or columna not in self.df_procesado.columns:
            return {}
        
        datos = self.df_procesado[columna].dropna()
        
        if len(datos) == 0:
            return {}
        
        return {
            'promedio': round(datos.mean(), 2),
            'minimo': round(datos.min(), 2),
            'maximo': round(datos.max(), 2),
            'mediana': round(datos.median(), 2),
            'desv_estandar': round(datos.std(), 2),
            'cantidad': len(datos),
            'nulos': len(self.df_procesado[columna]) - len(datos),
        }

    def exportar_excel(self, ruta_salida, incluir_estadisticas=True):
        """
        Exporta datos procesados a archivo Excel
        
        Parámetros:
        -----------
        ruta_salida : str
            Ruta del archivo de salida
        incluir_estadisticas : bool
            Si incluir hoja con estadísticas
            
        Retorna:
        --------
        tuple (bool, str)
            (éxito, mensaje)
        """
        if self.df_procesado is None:
            return False, "No hay datos procesados para exportar"
        
        try:
            # Crear directorio si no existe
            ruta = Path(ruta_salida)
            ruta.parent.mkdir(parents=True, exist_ok=True)
            
            # Crear escritor de Excel
            with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
                # Datos principales
                self.df_procesado.to_excel(writer, sheet_name='Datos', index=False)
                
                # Estadísticas
                if incluir_estadisticas:
                    self._exportar_estadisticas(writer)
            
            return True, f"Archivo exportado exitosamente: {ruta_salida}"
        
        except Exception as e:
            return False, f"Error al exportar: {str(e)}"

    def _exportar_estadisticas(self, writer):
        """
        Exporta estadísticas a hoja separada
        
        Parámetros:
        -----------
        writer : ExcelWriter
            Escritor de Excel
        """
        # Recopilar estadísticas de columnas de resultado
        columnas_resultado = [col for col in self.df_procesado.columns if col.endswith('_ug_m3')]
        
        datos_stats = []
        for col in columnas_resultado:
            stats = self.obtener_estadisticas(col)
            if stats:
                stats['Contaminante'] = col.replace('_ug_m3', '').upper()
                stats['Unidad'] = 'μg/m³'
                datos_stats.append(stats)
        
        if datos_stats:
            df_stats = pd.DataFrame(datos_stats)
            # Reordenar columnas
            columnas_ordenadas = ['Contaminante', 'Unidad', 'promedio', 'minimo', 'maximo', 'mediana', 'desv_estandar', 'cantidad', 'nulos']
            df_stats = df_stats[[col for col in columnas_ordenadas if col in df_stats.columns]]
            
            df_stats.to_excel(writer, sheet_name='Estadísticas', index=False)

    def obtener_resumen(self):
        """
        Obtiene resumen de datos procesados
        
        Retorna:
        --------
        str
            Texto con resumen
        """
        if self.df_procesado is None:
            return "No hay datos procesados"
        
        resumen = f"""
        RESUMEN DE DATOS PROCESADOS
        ============================
        Filas: {len(self.df_procesado)}
        Columnas: {len(self.df_procesado.columns)}
        
        COLUMNAS DETECTADAS:
        """
        
        for tipo, columna in self.mapeo_columnas.items():
            if columna:
                resumen += f"\n  {tipo.upper()}: {columna}"
        
        resumen += "\n"
        return resumen


if __name__ == "__main__":
    # Ejemplo de uso
    procesador = ProcesadorExcel()
    
    print("=" * 60)
    print("PROCESADOR DE EXCEL - EJEMPLO")
    print("=" * 60)
    
    # Crear archivo de ejemplo
    print("\nCreando archivo de ejemplo...")
    from crear_ejemplo import crear_archivo_ejemplo
    crear_archivo_ejemplo()
    
    # Leer archivo
    print("\nLeyendo archivo...")
    exito, msg, df = procesador.leer_excel('datos/ejemplo.xlsx')
    print(f"  {msg}")
    
    if exito:
        print(procesador.obtener_resumen())
        
        # Convertir datos
        print("\nConvirtiendo datos...")
        exito, msg, df_resultado = procesador.convertir_datos()
        print(f"  {msg}")
        
        if exito:
            # Mostrar primeras filas
            print("\nPrimeras 5 filas de resultados:")
            cols_resultado = [col for col in df_resultado.columns if col.endswith('_ug_m3')]
            print(df_resultado[['Date', 'Time', 'TmpC', 'RH'] + cols_resultado].head())
            
            # Estadísticas
            print("\nEstadísticas:")
            for col in cols_resultado:
                stats = procesador.obtener_estadisticas(col)
                if stats:
                    print(f"\n  {col}:")
                    for k, v in stats.items():
                        print(f"    {k}: {v}")
            
            # Exportar
            print("\nExportando...")
            exito, msg = procesador.exportar_excel('datos/salida/resultados.xlsx')
            print(f"  {msg}")
    
    print("\n" + "=" * 60)
