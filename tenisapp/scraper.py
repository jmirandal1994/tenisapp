import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://www.tennisexplorer.com"

# ----------------------------
# FUNCIÓN 1: Obtener partidos del día
# ----------------------------
def obtener_partidos_dia():
    url = f"{BASE_URL}/matches/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    partidos = []
    filas = soup.select("tr[data-id]")

    for fila in filas:
        columnas = fila.find_all("td")
        if len(columnas) < 3:
            continue

        jugador_1_tag = columnas[1].find("a")
        jugador_2_tag = columnas[2].find("a")

        if not jugador_1_tag or not jugador_2_tag:
            continue

        jugador_1 = jugador_1_tag.text.strip()
        jugador_2 = jugador_2_tag.text.strip()
        link_1 = BASE_URL + jugador_1_tag.get("href")
        link_2 = BASE_URL + jugador_2_tag.get("href")

        partidos.append({
            "jugador_1": jugador_1,
            "jugador_2": jugador_2,
            "link_1": link_1,
            "link_2": link_2
        })

    return partidos

# ----------------------------
# FUNCIÓN 2: Obtener torneos próximos para un jugador
# ----------------------------
def obtener_torneos_proximos(link_jugador):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(link_jugador, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    torneos = []

    seccion = soup.find("div", id="nextmatches")
    if not seccion:
        return torneos

    filas = seccion.select("table tr")
    for fila in filas[1:]:  # Saltar encabezado
        columnas = fila.find_all("td")
        if len(columnas) < 2:
            continue

        torneo = columnas[0].text.strip()
        fecha = columnas[1].text.strip()
        torneo_lower = torneo.lower()
        es_importante = any(p in torneo_lower for p in ["atp", "qual", "challenger", "q"])

        torneos.append({
            "torneo": torneo,
            "fecha": fecha,
            "es_importante": es_importante
        })

    return torneos

# ----------------------------
# TESTEO
# ----------------------------
if __name__ == "__main__":
    partidos = obtener_partidos_dia()
    for p in partidos[:3]:  # solo mostramos 3 por ahora
        print(f"{p['jugador_1']} vs {p['jugador_2']}")
        t1 = obtener_torneos_proximos(p['link_1'])
        t2 = obtener_torneos_proximos(p['link_2'])

        print(f"  Próximos de {p['jugador_1']}:")
        for t in t1:
            print(f"    {'✅' if t['es_importante'] else '•'} {t['fecha']} - {t['torneo']}")

        print(f"  Próximos de {p['jugador_2']}:")
        for t in t2:
            print(f"    {'✅' if t['es_importante'] else '•'} {t['fecha']} - {t['torneo']}")
        
        print("\n" + "-"*40 + "\n")

