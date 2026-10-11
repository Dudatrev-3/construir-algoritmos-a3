import os
import requests
import folium
from dotenv import load_dotenv

#autentificação
load_dotenv(".env")
s = requests.Session()
res = s.post(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}"
)

#procura linhas
linhas = s.get(
    "http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca=Lapa"
)
linhas = linhas.json()

#paradas
codigo_linha = 2451
res = s.get(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={codigo_linha}"
)
paradas = res.json()

#posições
res = s.get(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha={codigo_linha}"
)
pos = res.json()

#mapa
m = folium.Map(
    location=[paradas[0]["py"], paradas[0]["px"]],
    zoom_start=14
)

#ônibus
for onibus in pos["vs"]:
    folium.Marker(
        location=[onibus["py"], onibus["px"]],
        popup=f"Ônibus: {onibus['p']}",
        icon=folium.Icon(color="green")
    ).add_to(m)

#marcador
for parada in paradas:
    folium.Marker(
        location=[parada["py"], parada["px"]],
        popup=parada["np"],
        icon=folium.Icon(color="red")
    ).add_to(m)    

m.save("mapa.html")
