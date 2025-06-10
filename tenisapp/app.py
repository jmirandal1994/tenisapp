from flask import Flask, render_template
from scraper import obtener_partidos_dia, obtener_torneos_proximos

app = Flask(__name__)

@app.route("/")
def index():
    partidos_raw = obtener_partidos_dia()
    partidos = []

    for p in partidos_raw:
        torneos_1 = obtener_torneos_proximos(p['link_1'])
        torneos_2 = obtener_torneos_proximos(p['link_2'])

        partidos.append({
            "jugador_1": p['jugador_1'],
            "jugador_2": p['jugador_2'],
            "link_1": p['link_1'],
            "link_2": p['link_2'],
            "torneos_1": torneos_1,
            "torneos_2": torneos_2
        })

    return render_template("index.html", partidos=partidos)

if __name__ == "__main__":
    app.run(debug=True)
