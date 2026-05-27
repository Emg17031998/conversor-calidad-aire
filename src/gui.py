"""
Interfaz Gráfica (GUI) con Tkinter
Aplicación para conversión de unidades de calidad de aire
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from pathlib import Path
import pandas as pd
import os
from src.procesador import ProcesadorExcel
from src.conversiones import ConversorCalidadAire


class AplicacionConversor:
    """
    Aplicación GUI para conversión de calidad de aire
    """

    def __init__(self, ventana_principal):
        """
        Inicializa la aplicación
        """
        self.ventana = ventana_principal
        self.ventana.title("Conversor de Calidad de Aire - EPAS600")
        self.ventana.geometry("900x700")
        self.ventana.resizable(True, True)
        
        # Crear icono de estilo (emoji)
        self.ventana.iconphoto(False)
        
        # Inicializar procesadores
        self.procesador = ProcesadorExcel()
        self.conversor = ConversorCalidadAire()
        
        # Variables de control
        self.archivo_cargado = tk.StringVar(value="Ninguno")
        self.filas_procesadas = tk.IntVar(value=0)
        
        # Crear interfaz
        self._crear_interfaz()

    def _crear_interfaz(self):
        """
        Crea la interfaz gráfica completa
        """
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame superior - Carga de archivo
        frame_carga = ttk.LabelFrame(self.ventana, text="1. Cargar Archivo Excel", padding=10)
        frame_carga.pack(fill=tk.X, padx=10, pady=5)
        
        btn_cargar = ttk.Button(frame_carga, text="Seleccionar archivo...", command=self._cargar_archivo)
        btn_cargar.pack(side=tk.LEFT, padx=5)
        
        self.label_archivo = ttk.Label(frame_carga, textvariable=self.archivo_cargado, foreground="blue")
        self.label_archivo.pack(side=tk.LEFT, padx=10)
        
        # Frame de vista previa
        frame_preview = ttk.LabelFrame(self.ventana, text="2. Vista Previa de Datos", padding=10)
        frame_preview.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tabla de vista previa
        self.tree = ttk.Treeview(frame_preview, height=8, columns=('Col1', 'Col2', 'Col3', 'Col4', 'Col5'), show='headings')
        scrollbar = ttk.Scrollbar(frame_preview, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame de configuración de columnas
        frame_config = ttk.LabelFrame(self.ventana, text="3. Configurar Columnas (Detectadas automáticamente)", padding=10)
        frame_config.pack(fill=tk.X, padx=10, pady=5)
        
        self.labels_config = {}
        gases = ['CO', 'NO2', 'SO2', 'O3', 'Temperatura', 'Humedad']
        for i, gas in enumerate(gases):
            label = ttk.Label(frame_config, text=f"{gas}: -")
            label.grid(row=i//3, column=i%3, padx=5, pady=5, sticky=tk.W)
            self.labels_config[gas.lower().replace('ó', 'o').replace('n', 'n')] = label
        
        # Frame de acciones
        frame_acciones = ttk.LabelFrame(self.ventana, text="4. Procesar y Exportar", padding=10)
        frame_acciones.pack(fill=tk.X, padx=10, pady=5)
        
        btn_convertir = ttk.Button(frame_acciones, text="Convertir Datos", command=self._convertir_datos)
        btn_convertir.pack(side=tk.LEFT, padx=5)
        
        btn_exportar = ttk.Button(frame_acciones, text="Exportar a Excel", command=self._exportar_excel)
        btn_exportar.pack(side=tk.LEFT, padx=5)
        
        btn_estadisticas = ttk.Button(frame_acciones, text="Ver Estadísticas", command=self._ver_estadisticas)
        btn_estadisticas.pack(side=tk.LEFT, padx=5)
        
        btn_limpiar = ttk.Button(frame_acciones, text="Limpiar", command=self._limpiar)
        btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        # Barra de estado
        self.label_estado = ttk.Label(self.ventana, text="Estado: Listo", relief=tk.SUNKEN)
        self.label_estado.pack(fill=tk.X, padx=10, pady=5)
        self.label_filas = ttk.Label(self.ventana, text="Filas procesadas: 0")
        self.label_filas.pack(fill=tk.X, padx=10, pady=2)

    def _cargar_archivo(self):
        """
        Carga un archivo Excel
        """
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls"), ("Todos", "*.*")]
        )
        
        if not ruta:
            return
        
        # Leer archivo
        exito, msg, df = self.procesador.leer_excel(ruta)
        
        if not exito:
            messagebox.showerror("Error", msg)
            return
        
        # Actualizar UI
        self.archivo_cargado.set(Path(ruta).name)
        self.label_estado.config(text=f"Estado: {msg}")
        
        # Mostrar vista previa
        self._actualizar_preview(df)
        
        # Actualizar configuración de columnas
        self._actualizar_config_columnas()

    def _actualizar_preview(self, df):
        """
        Actualiza la tabla de vista previa
        """
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Configurar columnas
        columnas = list(df.columns[:5])  # Mostrar máximo 5 columnas
        self.tree['columns'] = columnas
        self.tree['show'] = 'headings'
        
        for col in columnas:
            self.tree.column(col, width=100)
            self.tree.heading(col, text=col)
        
        # Agregar datos (máximo 10 filas)
        for idx, row in df.head(10).iterrows():
            valores = [str(row[col])[:20] for col in columnas]
            self.tree.insert('', tk.END, values=valores)

    def _actualizar_config_columnas(self):
        """
        Actualiza etiquetas de configuración de columnas
        """
        mapeos = {
            'co': 'CO',
            'no2': 'NO2',
            'so2': 'SO2',
            'o3': 'O3',
            'temperatura': 'Temperatura',
            'humedad': 'Humedad',
        }
        
        for tipo, label_key in mapeos.items():
            columna = self.procesador.obtener_columna(tipo)
            if label_key.lower() in self.labels_config:
                if columna:
                    self.labels_config[label_key.lower()] = ttk.Label(
                        self.ventana,
                        text=f"{label_key}: {columna}",
                        foreground="green"
                    )
                else:
                    self.labels_config[label_key.lower()] = ttk.Label(
                        self.ventana,
                        text=f"{label_key}: -",
                        foreground="red"
                    )

    def _convertir_datos(self):
        """
        Convierte los datos
        """
        if self.procesador.df_original is None:
            messagebox.showwarning("Advertencia", "Por favor carga un archivo primero")
            return
        
        self.label_estado.config(text="Estado: Convirtiendo datos...")
        self.ventana.update()
        
        exito, msg, df = self.procesador.convertir_datos()
        
        if not exito:
            messagebox.showerror("Error", msg)
            self.label_estado.config(text="Estado: Error en conversión")
            return
        
        self.filas_procesadas.set(len(df))
        self.label_filas.config(text=f"Filas procesadas: {len(df)}")
        self.label_estado.config(text=f"Estado: {msg}")
        messagebox.showinfo("Éxito", msg)

    def _exportar_excel(self):
        """
        Exporta datos a archivo Excel
        """
        if self.procesador.df_procesado is None:
            messagebox.showwarning("Advertencia", "Por favor convierte datos primero")
            return
        
        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("Todos", "*.*")],
            initialfile="resultados.xlsx"
        )
        
        if not ruta:
            return
        
        self.label_estado.config(text="Estado: Exportando...")
        self.ventana.update()
        
        exito, msg = self.procesador.exportar_excel(ruta, incluir_estadisticas=True)
        
        if not exito:
            messagebox.showerror("Error", msg)
            return
        
        self.label_estado.config(text=f"Estado: {msg}")
        messagebox.showinfo("Éxito", f"Archivo exportado: {ruta}")

    def _ver_estadisticas(self):
        """
        Muestra estadísticas de los datos
        """
        if self.procesador.df_procesado is None:
            messagebox.showwarning("Advertencia", "Por favor convierte datos primero")
            return
        
        # Crear ventana de estadísticas
        ventana_stats = tk.Toplevel(self.ventana)
        ventana_stats.title("Estadísticas")
        ventana_stats.geometry("600x400")
        
        # Area de texto
        texto = scrolledtext.ScrolledText(ventana_stats, wrap=tk.WORD, width=70, height=20)
        texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Recopilar estadísticas
        columnas_resultado = [col for col in self.procesador.df_procesado.columns if col.endswith('_ug_m3')]
        
        contenido = "ESTADÍSTICAS DE DATOS PROCESADOS\n"
        contenido += "=" * 50 + "\n\n"
        
        for col in columnas_resultado:
            stats = self.procesador.obtener_estadisticas(col)
            if stats:
                contenido += f"{col}:\n"
                contenido += f"  Promedio: {stats['promedio']} μg/m³\n"
                contenido += f"  Mínimo: {stats['minimo']} μg/m³\n"
                contenido += f"  Máximo: {stats['maximo']} μg/m³\n"
                contenido += f"  Mediana: {stats['mediana']} μg/m³\n"
                contenido += f"  Desv. Est.: {stats['desv_estandar']} μg/m³\n"
                contenido += f"  Cantidad: {stats['cantidad']}\n"
                contenido += f"  Nulos: {stats['nulos']}\n\n"
        
        texto.insert(tk.END, contenido)
        texto.config(state=tk.DISABLED)

    def _limpiar(self):
        """
        Limpia la aplicación
        """
        if messagebox.askyesno("Confirmar", "¿Deseas limpiar todos los datos?"):
            self.procesador = ProcesadorExcel()
            self.archivo_cargado.set("Ninguno")
            self.filas_procesadas.set(0)
            self.label_estado.config(text="Estado: Listo")
            self.label_filas.config(text="Filas procesadas: 0")
            
            # Limpiar preview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            messagebox.showinfo("Info", "Datos limpios")


def main():
    """
    Función principal para ejecutar la aplicación
    """
    ventana = tk.Tk()
    app = AplicacionConversor(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
