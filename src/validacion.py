"""
Módulo de validación de datos de calidad de aire
Verifica rangos, detecta anomalías y compara contra límites normativos
"""

import warnings


class ValidadorCalidadAire:
    """
    Validador de datos de calidad de aire
    Incluye límites normativos (OMS, EPA) y detección de anomalías
    """

    # Límites OMS 2021 (μg/m³) - 24 horas
    LIMITES_OMS_24H = {
        'CO': 4000,      # mg/m³ (convertir)
        'NO2': 35,       # μg/m³
        'SO2': 40,       # μg/m³
        'O3': 100,       # μg/m³
        'PM10': 50,      # μg/m³
        'PM2.5': 15,     # μg/m³
    }

    # Límites EPA (μg/m³) - 24 horas
    LIMITES_EPA_24H = {
        'CO': 10000,     # μg/m³
        'NO2': 100,      # μg/m³
        'SO2': 350,      # μg/m³
        'O3': 70,        # μg/m³
    }

    # Rangos válidos para variables ambientales
    RANGOS_VALIDOS = {
        'temperatura_celsius': (-50, 60),  # Rango físico posible
        'temperatura_recomendada': (10, 35),  # Típico para Panamá
        'humedad_relativa': (0, 100),
    }

    # Rangos esperados de concentraciones (μg/m³)
    RANGOS_TIPICOS = {
        'CO': (0, 5000),
        'NO2': (0, 200),
        'SO2': (0, 200),
        'O3': (0, 200),
    }

    def __init__(self):
        """Inicializa el validador"""
        self.errores = []
        self.advertencias = []

    def validar_temperatura(self, temperatura_celsius, strict=False):
        """
        Valida si la temperatura está en rango válido
        
        Parámetros:
        -----------
        temperatura_celsius : float
            Temperatura en grados Celsius
        strict : bool
            Si True, usa rango recomendado (10-35°C)
            Si False, usa rango físico posible (-50-60°C)
            
        Retorna:
        --------
        tuple (bool, str)
            (válido, mensaje)
        """
        rango = self.RANGOS_VALIDOS['temperatura_recomendada'] if strict else self.RANGOS_VALIDOS['temperatura_celsius']
        min_t, max_t = rango
        
        if not (min_t <= temperatura_celsius <= max_t):
            msg = f"Temperatura fuera de rango: {temperatura_celsius}°C (esperado {min_t}-{max_t}°C)"
            return False, msg
        
        if strict and not (10 <= temperatura_celsius <= 35):
            msg = f"Advertencia: Temperatura {temperatura_celsius}°C fuera del rango típico (10-35°C)"
            return True, msg
        
        return True, "OK"

    def validar_humedad(self, humedad_relativa):
        """
        Valida si la humedad relativa está en rango válido
        
        Parámetros:
        -----------
        humedad_relativa : float
            Humedad relativa en porcentaje (0-100)
            
        Retorna:
        --------
        tuple (bool, str)
            (válido, mensaje)
        """
        min_h, max_h = self.RANGOS_VALIDOS['humedad_relativa']
        
        if not (min_h <= humedad_relativa <= max_h):
            msg = f"Humedad fuera de rango: {humedad_relativa}% (esperado {min_h}-{max_h}%)"
            return False, msg
        
        return True, "OK"

    def validar_concentracion(self, concentracion_ug_m3, gas):
        """
        Valida si una concentración está en rango típico
        
        Parámetros:
        -----------
        concentracion_ug_m3 : float
            Concentración en μg/m³
        gas : str
            Nombre del gas ('CO', 'NO2', 'SO2', 'O3')
            
        Retorna:
        --------
        tuple (bool, str)
            (válido, mensaje)
        """
        if gas not in self.RANGOS_TIPICOS:
            return True, f"Gas {gas} sin rango definido"
        
        min_c, max_c = self.RANGOS_TIPICOS[gas]
        
        if concentracion_ug_m3 < min_c or concentracion_ug_m3 > max_c:
            msg = f"Concentración {gas} fuera de rango típico: {concentracion_ug_m3} μg/m³ (típico {min_c}-{max_c})"
            return False, msg
        
        return True, "OK"

    def comparar_con_limite_oms(self, concentracion_ug_m3, gas):
        """
        Compara concentración con límite OMS 24h
        
        Parámetros:
        -----------
        concentracion_ug_m3 : float
            Concentración en μg/m³
        gas : str
            Nombre del gas
            
        Retorna:
        --------
        dict
            {'cumple': bool, 'limite': float, 'porcentaje': float, 'estado': str}
        """
        if gas not in self.LIMITES_OMS_24H:
            return {'cumple': True, 'limite': None, 'porcentaje': 0, 'estado': 'Sin límite OMS'}
        
        limite = self.LIMITES_OMS_24H[gas]
        porcentaje = (concentracion_ug_m3 / limite) * 100 if limite > 0 else 0
        cumple = concentracion_ug_m3 <= limite
        
        if cumple:
            estado = "✓ Cumple OMS"
        else:
            estado = f"✗ Excede OMS ({porcentaje:.1f}%)"
        
        return {
            'cumple': cumple,
            'limite': limite,
            'porcentaje': round(porcentaje, 2),
            'estado': estado
        }

    def comparar_con_limite_epa(self, concentracion_ug_m3, gas):
        """
        Compara concentración con límite EPA 24h
        
        Parámetros:
        -----------
        concentracion_ug_m3 : float
            Concentración en μg/m³
        gas : str
            Nombre del gas
            
        Retorna:
        --------
        dict
            {'cumple': bool, 'limite': float, 'porcentaje': float, 'estado': str}
        """
        if gas not in self.LIMITES_EPA_24H:
            return {'cumple': True, 'limite': None, 'porcentaje': 0, 'estado': 'Sin límite EPA'}
        
        limite = self.LIMITES_EPA_24H[gas]
        porcentaje = (concentracion_ug_m3 / limite) * 100 if limite > 0 else 0
        cumple = concentracion_ug_m3 <= limite
        
        if cumple:
            estado = "✓ Cumple EPA"
        else:
            estado = f"✗ Excede EPA ({porcentaje:.1f}%)"
        
        return {
            'cumple': cumple,
            'limite': limite,
            'porcentaje': round(porcentaje, 2),
            'estado': estado
        }

    def detectar_anomalia(self, valor, media, desv_estandar, umbral_sigma=3.0):
        """
        Detecta si un valor es una anomalía usando el método de desviación estándar
        
        Parámetros:
        -----------
        valor : float
            Valor a verificar
        media : float
            Media de la serie
        desv_estandar : float
            Desviación estándar de la serie
        umbral_sigma : float
            Umbral de desviaciones estándar (default: 3.0)
            
        Retorna:
        --------
        tuple (bool, str)
            (es_anomalia, mensaje)
        """
        if desv_estandar == 0:
            return False, "No hay variación en los datos"
        
        z_score = abs((valor - media) / desv_estandar)
        es_anomalia = z_score > umbral_sigma
        
        msg = f"Z-score: {z_score:.2f} - {'ANOMALÍA' if es_anomalia else 'Normal'}"
        
        return es_anomalia, msg

    def validar_datos_completos(self, temperatura, humedad, gas=None):
        """
        Realiza validación completa de datos
        
        Retorna:
        --------
        dict
            Resultado de validaciones
        """
        resultado = {
            'valido': True,
            'temperatura': self.validar_temperatura(temperatura, strict=True),
            'humedad': self.validar_humedad(humedad),
            'errores': [],
            'advertencias': []
        }
        
        # Compilar errores y advertencias
        if not resultado['temperatura'][0]:
            resultado['errores'].append(resultado['temperatura'][1])
            resultado['valido'] = False
        elif 'Advertencia' in resultado['temperatura'][1]:
            resultado['advertencias'].append(resultado['temperatura'][1])
        
        if not resultado['humedad'][0]:
            resultado['errores'].append(resultado['humedad'][1])
            resultado['valido'] = False
        
        return resultado


if __name__ == "__main__":
    # Ejemplos de uso
    validador = ValidadorCalidadAire()

    print("=" * 60)
    print("VALIDADOR DE CALIDAD DE AIRE - EJEMPLOS")
    print("=" * 60)

    # Validar temperatura
    print("\nValidación de temperatura:")
    for t in [5, 15, 25, 35, 45]:
        valido, msg = validador.validar_temperatura(t, strict=True)
        print(f"  {t}°C: {msg}")

    # Validar humedad
    print("\nValidación de humedad:")
    for h in [0, 50, 100, 150]:
        valido, msg = validador.validar_humedad(h)
        print(f"  {h}%: {msg}")

    # Comparar con límites
    print("\nComparación con límites (NO₂):")
    no2_valores = [10, 35, 70, 100]
    for no2 in no2_valores:
        oms = validador.comparar_con_limite_oms(no2, 'NO2')
        epa = validador.comparar_con_limite_epa(no2, 'NO2')
        print(f"  {no2} μg/m³: OMS={oms['estado']}, EPA={epa['estado']}")

    print("\n" + "=" * 60)
