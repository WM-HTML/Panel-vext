import requests
import sys
import re

API_KEY = 'AIzaSyD-EXAMPLE-APIKEY-FOR-TESTING-1234567890'  # API de ejemplo, no válida

def extraer_video_id(url):
    patrones = [
        r'youtu\.be/([^?&]+)',
        r'v=([^?&]+)',
        r'embed/([^?&]+)',
    ]
    for p in patrones:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None

def obtener_info_video(video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={API_KEY}'
    resp = requests.get(url)
    if resp.status_code != 200:
        print("Error en la petición:", resp.status_code)
        return
    data = resp.json()
    if 'items' not in data or len(data['items']) == 0:
        print("Video no encontrado.")
        return

    item = data['items'][0]
    snippet = item['snippet']
    stats = item['statistics']

    titulo = snippet.get('title', 'N/A')
    canal = snippet.get('channelTitle', 'N/A')
    fecha = snippet.get('publishedAt', 'N/A')
    url_video = f"https://youtu.be/{video_id}"
    vistas = stats.get('viewCount', '0')
    likes = stats.get('likeCount', 'No disponible')

    print(f"Título: {titulo}")
    print(f"URL: {url_video}")
    print(f"Canal: {canal}")
    print(f"Fecha de subida: {fecha}")
    print(f"Vistas: {vistas}")
    print(f"Likes: {likes}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        url = input("Pega la URL del video de YouTube: ").strip()
    else:
        url = sys.argv[1]
    video_id = extraer_video_id(url)
    if not video_id:
        print("No se pudo extraer el ID del video de la URL proporcionada.")
    else:
        obtener_info_video(video_id)
