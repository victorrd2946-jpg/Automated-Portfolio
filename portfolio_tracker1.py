import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# --- 1. CONFIGURACIÓN DE TU PORTAFOLIO ---
# Ingresa aquí tus acciones y la cantidad que tienes (Shares)
# He actualizado SHOP con 1, cámbialo por tu cantidad real.
mis_acciones = {
    "NVDA": 9.51376, "META": 0.55874, "VOO": 0.52598, 
    "GLDM": 6.71521, "IBIT": 8.25082, "AMZN": 0.97603,
    "SHOP": 1.83032, "DUOL": 3.93319, "SGOV": 5.33698
}

tickers = list(mis_acciones.keys())

print(f"--- Extrayendo datos para {len(tickers)} activos ---")

try:
    # --- 2. EXTRACCIÓN Y CÁLCULO ---
    datos = yf.download(tickers, period="1d")['Close']
    ultimo_precio = datos.iloc[-1]
    
    # Calculamos el valor de cada posición (Precio * Cantidad)
    valor_total = sum(ultimo_precio[t] * mis_acciones[t] for t in tickers)
    fecha_hoy = datetime.now().strftime('%Y-%m-%d %H:%M')

    # --- 3. GUARDADO EN EL HISTORIAL ---
    # Creamos una pequeña tabla con la foto de hoy
    nueva_fila = pd.DataFrame({"Fecha": [fecha_hoy], "Total_Value": [round(valor_total, 2)]})
    
    # Lo guardamos en un archivo CSV. 'a' significa "Append" (añadir al final)
    archivo_historial = "portfolio_history.csv"
    hdr = not os.path.exists(archivo_historial) # Solo pone encabezado la primera vez
    
    nueva_fila.to_csv(archivo_historial, mode='a', index=False, header=hdr)

    print(f"\n¡Éxito! Valor Total: ${round(valor_total, 2)}")
    print(f"Datos guardados en: {archivo_historial}")

except Exception as e:
    print(f"Error al procesar: {e}")