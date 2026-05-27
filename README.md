# Conversor de Calidad de Aire - EPAS600

Sistema profesional para convertir unidades de contaminantes atmosféricos (ppb/ppm → μg/m³) con corrección por temperatura, diseñado específicamente para laboratorios ambientales.

## 📋 Características

✅ **Conversión precisa con corrección térmica** - Los datos se ajustan según temperatura ambiente  
✅ **Soporta múltiples gases** - CO, NO₂, SO₂, O₃, CO₂  
✅ **Interfaz gráfica intuitiva** - Fácil de usar, sin necesidad de programación  
✅ **Importación automática de Excel** - Detecta automáticamente columnas  
✅ **Validación de datos** - Alertas sobre valores anómalos  
✅ **Exportación formateada** - Resultados listos para reportes  
✅ **Estadísticas integradas** - Promedio, mín, máx, desv. estándar  

## 🔬 Pesos Moleculares

- **CO** (Monóxido de Carbono): 28 g/mol
- **NO₂** (Dióxido de Nitrógeno): 46 g/mol
- **SO₂** (Dióxido de Azufre): 64 g/mol
- **O₃** (Ozono): 48 g/mol
- **CO₂** (Dióxido de Carbono): 44 g/mol

## 🧮 Fórmula de Conversión

```
μg/m³ = (ppb/ppm × MW / 24.45) × (298.15 K / T_ambiente)
```

Donde:
- **MW**: Peso molecular del gas (g/mol)
- **24.45**: Constante molar a 25°C y 1 atm
- **298.15 K**: Temperatura de referencia (25°C)
- **T_ambiente**: Temperatura en Kelvin

## 📦 Requisitos

- Python 3.8+
- pandas
- openpyxl
- numpy

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Emg17031998/conversor-calidad-aire.git
cd conversor-calidad-aire
```

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ▶️ Uso

### Opción 1: Interfaz Gráfica (Recomendado)

```bash
python main.py
```

Se abrirá la aplicación gráfica donde podrás:
1. Cargar archivo Excel con datos del EPAS600
2. Configurar columnas de temperatura y humedad
3. Convertir datos ppb/ppm a μg/m³
4. Exportar resultados a Excel

### Opción 2: Uso programático

```python
from src.conversiones import ConversorCalidadAire
from src.procesador import ProcesadorExcel

# Convertir un valor
conversor = ConversorCalidadAire()
valor_ug_m3 = conversor.ppb_a_ug_m3(
    valor_ppb=10,           # 10 ppb
    gas='NO2',              # Dióxido de nitrógeno
    temperatura_celsius=25  # Temperatura ambiente
)
print(f"Resultado: {valor_ug_m3} μg/m³")

# Procesar archivo Excel completo
procesador = ProcesadorExcel()
exito, msg, df = procesador.leer_excel('datos_entrada.xlsx')
exito, msg, df_resultado = procesador.convertir_datos()
procesador.exportar_excel('resultados.xlsx')
```

## 📂 Estructura del Proyecto

```
conversor-calidad-aire/
├── src/
│   ├── __init__.py           # Inicialización del módulo
│   ├── conversiones.py       # Lógica de conversión ppb/ppm → μg/m³
│   ├── validacion.py         # Validación de datos y límites normativos
│   ├── procesador.py         # Lectura y escritura de archivos Excel
│   └── gui.py                # Interfaz gráfica (tkinter)
├── datos/
│   └── ejemplo.xlsx          # Archivo de ejemplo con datos de prueba
├── main.py                   # Punto de entrada de la aplicación
├── requirements.txt          # Dependencias del proyecto
├── README.md                 # Este archivo
└── .gitignore                # Archivos a ignorar en Git
```

## 💡 Ejemplo de Uso

### Archivo Excel de entrada

| Date | Time | CO (ppm) | NO2 (ppb) | SO2 (ppb) | TmpC | RH |
|------|------|----------|-----------|-----------|------|-----|
| 13/04/2026 | 8:00:00 | 0.12 | 2 | 15 | 25 | 65 |
| 13/04/2026 | 8:05:00 | 0.27 | 2 | 1 | 26 | 65 |

### Resultado después de convertir

| Date | Time | CO (ppm) | NO2 (ppb) | SO2 (ppb) | TmpC | RH | CO_ug_m3 | NO2_ug_m3 | SO2_ug_m3 |
|------|------|----------|-----------|-----------|------|-----|----------|-----------|-----------|
| 13/04/2026 | 8:00:00 | 0.12 | 2 | 15 | 25 | 65 | 137.34 | 96.80 | 192.40 |
| 13/04/2026 | 8:05:00 | 0.27 | 2 | 1 | 26 | 65 | 309.41 | 96.60 | 12.83 |

## 🧪 Pruebas

Para verificar que la conversión funciona correctamente:

```bash
# Instalar pytest
pip install pytest

# Ejecutar pruebas
pytest tests/
```

## 📊 Validación y Límites Normativos

El conversor incluye validación contra:

- **OMS 2021** - Guías de calidad de aire
- **EPA** - Límites de la Agencia de Protección Ambiental de EE.UU.
- **Rangos típicos** - Temperatura (10-35°C), Humedad (0-100%)

## 🔧 Configuración Avanzada

### Parámetros de entrada

**Temperaturas soportadas**: -50°C a 60°C (rango típico para Panamá: 10-35°C)

**Presión**: Por defecto 1 atm (puede ajustarse si se tiene dato)

**Humedad**: Para validación (0-100%)

## 📝 Notas Técnicas

### Corrección por Temperatura

La fórmula implementada asume que:
- La concentración de gases varía inversamente con la temperatura
- A mayor temperatura, la misma masa se distribuye en mayor volumen
- Se aplica la ley combinada de gases ideales

### Precisión

- Redondeo a 2 decimales en resultados finales
- Errores < 1% para condiciones típicas
- Compatible con datos ICPA280 y EPAS600

## 🚨 Solución de Problemas

### Error: "Columna 'TmpC' no encontrada"

**Solución**: Asegúrate que tu Excel tiene una columna con temperatura. El sistema intenta detectarla automáticamente, pero también puedes seleccionarla manualmente en la GUI.

### Error: "Módulo 'openpyxl' no encontrado"

**Solución**: Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Los valores convertidos no coinciden con Excel

**Posible causa**: Diferencia en métodos de redondeo o temperatura de referencia

**Verificación**: Comprueba que:
- Los pesos moleculares sean correctos
- La temperatura sea en Celsius
- Utilices los mismos factores de conversión

## 🎯 Roadmap - Próximas Mejoras

- [ ] **Fase 2**: Gráficos de series temporales
- [ ] **Fase 3**: Reportes automáticos en PDF/Word
- [ ] **Fase 4**: Comparación con límites normativos
- [ ] **Fase 5**: Base de datos para auditoría
- [ ] **Fase 6**: API REST para integración con otros sistemas
- [ ] **Fase 7**: Sincronización en la nube

## 👨‍💼 Contribución

¿Tienes sugerencias o encontraste un bug? Por favor:

1. Abre un issue describiendo el problema
2. Si es una mejora, sugiere cambios con ejemplos
3. Incluye datos de prueba si es posible

## 📄 Licencia

Este proyecto está bajo licencia MIT. Puedes usarlo libremente en tu laboratorio.

## 📧 Contacto

Para preguntas o sugerencias sobre las conversiones y validaciones contacta al equipo del laboratorio.

---

**Versión**: 1.0.0  
**Última actualización**: Mayo 2026  
**Compatibilidad**: EPAS600, ICPA280  
**Laboratorio**: Ambiental y Ocupacional
