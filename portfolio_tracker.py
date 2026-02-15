import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# --- 1. CONFIGURACIÓN DEL PORTAFOLIO ---
# Aquí sumamos el EFECTIVO (CASH) y todos tus activos.
# He puesto 0.00 en CASH, cámbialo por lo que tengas disponible.
mis_activos = {
    "CASH": 0.00,
    "NVDA": 9.51376,
    "META": 0.55874,
    "VOO": 0.52598,
    "GLDM": 6.71521,
    "IBIT": 8.25082,
    "AMZN": 0.97603,
    "SHOP": 1.83032,
    "DUOL": 3.93319,
    "SGOV": 5.33698
}

# Filtramos solo los tickers que existen en Yahoo Finance (excluimos CASH)
tickers_mercado = [t for t in mis_activos.keys() if t != "CASH"]

print(f"--- Extrayendo precios para {len(tickers_mercado)} activos ---")

try:
    # --- 2. EXTRACCIÓN Y CÁLCULO ---
    datos = yf.download(tickers_mercado, period="1d")['Close']
    ultimo_precio = datos.iloc[-1]
    
    # Calculamos el valor de las acciones (Precio * Cantidad)
    valor_acciones = sum(ultimo_precio[t] * mis_activos[t] for t in tickers_mercado)
    
    # SUMA FINAL: Acciones + Efectivo
    valor_total = valor_acciones + mis_activos["CASH"]
    
    fecha_hoy = datetime.now().strftime('%Y-%m-%d %H:%M')

    # --- 3. GUARDADO EN EL HISTORIAL ---
    nueva_fila = pd.DataFrame({"Fecha": [fecha_hoy], "Total_Value": [round(valor_total, 2)]})
    archivo_historial = "portfolio_history.csv"
    hdr = not os.path.exists(archivo_historial)
    
    nueva_fila.to_csv(archivo_historial, mode='a', index=False, header=hdr)

    print(f"\n--- RESUMEN DE HOY ---")
    print(f"Acciones: ${round(valor_acciones, 2)}")
    print(f"Efectivo: ${mis_activos['CASH']}")
    print(f"TOTAL:    ${round(valor_total, 2)}")
    print(f"----------------------")

except Exception as e:
    print(f"Error al procesar los datos: {e}")

