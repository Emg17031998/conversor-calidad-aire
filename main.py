#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Aplicación principal: Conversor de Calidad de Aire

Uso:
    python main.py

Lanza la interfaz gráfica para convertir unidades de calidad de aire
ppb/ppm → μg/m³ con corrección por temperatura
"""

from src.gui import main

if __name__ == "__main__":
    main()
