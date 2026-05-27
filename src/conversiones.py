"""
Módulo de conversiones de unidades de calidad de aire
ppb/ppm → μg/m³ con corrección por temperatura
"""

import math


class ConversorCalidadAire:
    """
    Conversor de unidades de contaminantes atmosféricos
    ppb (partes por billón) → μg/m³
    ppm (partes por millón) → μg/m³
    
    Con corrección por temperatura ambiente
    """

    # Pesos moleculares (g/mol)
    PESOS_MOLECULARES = {
        'CO': 28,      # Monóxido de carbono
        'NO2': 46,     # Dióxido de nitrógeno
        'SO2': 64,     # Dióxido de azufre
        'O3': 48,      # Ozono
        'CO2': 44,     # Dióxido de carbono
    }

    # Constante molar a 25°C y 1 atm
    CONSTANTE_MOLAR = 24.45
    
    # Temperatura de referencia (25°C en Kelvin)
    TEMP_REFERENCIA_K = 298.15

    def __init__(self):
        """Inicializa el conversor"""
        pass

    def ppb_a_ug_m3(self, valor_ppb, gas, temperatura_celsius, presion_atm=1.0):
        """
        Convierte ppb a μg/m³ con corrección térmica
        
        Parámetros:
        -----------
        valor_ppb : float
            Valor en partes por billón (ppb)
        gas : str
            Nombre del gas ('CO', 'NO2', 'SO2', 'O3', 'CO2')
        temperatura_celsius : float
            Temperatura ambiente en grados Celsius
        presion_atm : float, opcional
            Presión en atmósferas (default: 1.0)
            
        Retorna:
        --------
        float
            Valor convertido en μg/m³
            
        Fórmula:
        μg/m³ = (ppb × MW / 24.45) × (298.15 K / T_kelvin) × (P / 1 atm)
        """
        
        # Validar gas
        if gas not in self.PESOS_MOLECULARES:
            raise ValueError(f"Gas no soportado: {gas}. Opciones: {list(self.PESOS_MOLECULARES.keys())}")
        
        # Obtener peso molecular
        mw = self.PESOS_MOLECULARES[gas]
        
        # Convertir temperatura a Kelvin
        temp_kelvin = temperatura_celsius + 273.15
        
        # Aplicar fórmula de conversión
        # μg/m³ = (ppb × MW / 24.45) × (298.15 / T) × (P / 1)
        factor_conversion = mw / self.CONSTANTE_MOLAR
        factor_temperatura = self.TEMP_REFERENCIA_K / temp_kelvin
        
        resultado = valor_ppb * factor_conversion * factor_temperatura * presion_atm
        
        return round(resultado, 2)

    def ppm_a_ug_m3(self, valor_ppm, gas, temperatura_celsius, presion_atm=1.0):
        """
        Convierte ppm a μg/m³ con corrección térmica
        
        Parámetros:
        -----------
        valor_ppm : float
            Valor en partes por millón (ppm)
        gas : str
            Nombre del gas ('CO', 'NO2', 'SO2', 'O3', 'CO2')
        temperatura_celsius : float
            Temperatura ambiente en grados Celsius
        presion_atm : float, opcional
            Presión en atmósferas (default: 1.0)
            
        Retorna:
        --------
        float
            Valor convertido en μg/m³
        """
        
        # Convertir ppm a ppb (1 ppm = 1000 ppb)
        valor_ppb = valor_ppm * 1000
        
        # Usar la función ppb_a_ug_m3
        return self.ppb_a_ug_m3(valor_ppb, gas, temperatura_celsius, presion_atm)

    def co_ppb_a_ug_m3(self, valor_ppb, temperatura_celsius):
        """
        Conversión específica para CO (ppb → μg/m³)
        """
        return self.ppb_a_ug_m3(valor_ppb, 'CO', temperatura_celsius)

    def co_ppm_a_ug_m3(self, valor_ppm, temperatura_celsius):
        """
        Conversión específica para CO (ppm → μg/m³)
        """
        return self.ppm_a_ug_m3(valor_ppm, 'CO', temperatura_celsius)

    def no2_ppb_a_ug_m3(self, valor_ppb, temperatura_celsius):
        """
        Conversión específica para NO₂ (ppb → μg/m³)
        """
        return self.ppb_a_ug_m3(valor_ppb, 'NO2', temperatura_celsius)

    def so2_ppb_a_ug_m3(self, valor_ppb, temperatura_celsius):
        """
        Conversión específica para SO₂ (ppb → μg/m³)
        """
        return self.ppb_a_ug_m3(valor_ppb, 'SO2', temperatura_celsius)

    def o3_ppb_a_ug_m3(self, valor_ppb, temperatura_celsius):
        """
        Conversión específica para O₃ (ppb → μg/m³)
        """
        return self.ppb_a_ug_m3(valor_ppb, 'O3', temperatura_celsius)

    def co2_ppm_a_ug_m3(self, valor_ppm, temperatura_celsius):
        """
        Conversión específica para CO₂ (ppm → μg/m³)
        """
        return self.ppm_a_ug_m3(valor_ppm, 'CO2', temperatura_celsius)

    def obtener_peso_molecular(self, gas):
        """
        Obtiene el peso molecular de un gas
        
        Parámetros:
        -----------
        gas : str
            Nombre del gas
            
        Retorna:
        --------
        int
            Peso molecular en g/mol
        """
        if gas not in self.PESOS_MOLECULARES:
            raise ValueError(f"Gas no soportado: {gas}")
        return self.PESOS_MOLECULARES[gas]


if __name__ == "__main__":
    # Ejemplos de uso
    conversor = ConversorCalidadAire()

    print("=" * 60)
    print("CONVERSOR DE CALIDAD DE AIRE - EJEMPLOS")
    print("=" * 60)

    # Ejemplo 1: CO en ppm → μg/m³
    co_ppm = 0.12
    temp = 25
    resultado_co = conversor.co_ppm_a_ug_m3(co_ppm, temp)
    print(f"\nEjemplo 1: CO")
    print(f"  Entrada: {co_ppm} ppm a {temp}°C")
    print(f"  Salida: {resultado_co} μg/m³")

    # Ejemplo 2: NO₂ en ppb → μg/m³
    no2_ppb = 2
    resultado_no2 = conversor.no2_ppb_a_ug_m3(no2_ppb, temp)
    print(f"\nEjemplo 2: NO₂")
    print(f"  Entrada: {no2_ppb} ppb a {temp}°C")
    print(f"  Salida: {resultado_no2} μg/m³")

    # Ejemplo 3: SO₂ en ppb → μg/m³
    so2_ppb = 15
    resultado_so2 = conversor.so2_ppb_a_ug_m3(so2_ppb, temp)
    print(f"\nEjemplo 3: SO₂")
    print(f"  Entrada: {so2_ppb} ppb a {temp}°C")
    print(f"  Salida: {resultado_so2} μg/m³")

    # Ejemplo 4: Variación por temperatura
    print(f"\nEjemplo 4: Efecto de temperatura en NO₂")
    for t in [10, 20, 25, 30, 35]:
        resultado = conversor.no2_ppb_a_ug_m3(2, t)
        print(f"  {t}°C: {resultado} μg/m³")

    print("\n" + "=" * 60)
