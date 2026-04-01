# -*- coding: utf-8 -*-

from pathlib import Path
import pandas as pd
from pytrends.request import TrendReq
import time

country_terms = {
    "CL": {"kw": "Bolsa de valores", "hl": "es-CL", "tz": -180},
}

timeframe = "2020-11-22 2025-11-09"

def get_trends(keyword, geo, hl, tz, timeframe=timeframe):
    pytrends = TrendReq(hl=hl, tz=tz)
    pytrends.build_payload([keyword], geo=geo, timeframe=timeframe)
    data = pytrends.interest_over_time().reset_index()

    if "isPartial" in data.columns:
        data = data.drop(columns=["isPartial"])

    data = data[["date", keyword]]
    data.columns = ["date", "value"]
    return data

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for geo, info in country_terms.items():
    keyword = info["kw"]
    hl = info["hl"]
    tz = info["tz"]

    print(f"Descargando datos para {geo} — término: {keyword}")
    df = get_trends(keyword, geo, hl, tz)

    today = pd.Timestamp.today().date()
    filename = output_dir / f"DatosGT_{geo}_{today}.xlsx"

    df.to_excel(filename, index=False)

    print(f"Archivo guardado en: {filename}")
    print(f"Existe el archivo: {filename.exists()}")

    time.sleep(20)
