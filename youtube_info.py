import requests
import sys
import re
import isodate

API_KEY = 'AIzaSyD3ciowjk5mWhO3xhXPIaPIL-I6BFIUdZk'

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

def obtener_suscriptores_canal(channel_id):
    url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={API_KEY}'
    resp = requests.get(url)
    if resp.status_code != 200:
        return "No disponible"
    data = resp.json()
    if 'items' not in data or len(data['items']) == 0:
        return "No disponible"
    subs = data['items'][0]['statistics'].get('subscriberCount', 'No disponible')
    return subs

def formatear_duracion(duration_iso):
    try:
        duracion = isodate.parse_duration(duration_iso)
        minutos, segundos = divmod(duracion.total_seconds(), 60)
        horas, minutos = divmod(minutos, 60)
        if horas > 0:
            return f"{int(horas)}:{int(minutos):02d}:{int(segundos):02d}"
        else:
            return f"{int(minutos)}:{int(segundos):02d}"
    except Exception:
        return duration_iso

def print_rojo(texto):
    print(f"\033[91m{texto}\033[0m")

def obtener_info_video(video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails,status&id={video_id}&key={API_KEY}'
    resp = requests.get(url)
    if resp.status_code != 200:
        print_rojo(f"Error en la petición: {resp.status_code}")
        return
    data = resp.json()
    if 'items' not in data or len(data['items']) == 0:
        print_rojo("Video no encontrado.")
        return

    item = data['items'][0]
    snippet = item.get('snippet', {})
    stats = item.get('statistics', {})
    contentDetails = item.get('contentDetails', {})
    status = item.get('status', {})

    titulo = snippet.get('title', 'N/A')
    canal = snippet.get('channelTitle', 'N/A')
    canal_id = snippet.get('channelId', None)
    fecha = snippet.get('publishedAt', 'N/A')
    vistas = stats.get('viewCount', '0')
    likes = stats.get('likeCount', 'No disponible')
    comentarios = stats.get('commentCount', 'No disponible')
    privacidad = status.get('privacyStatus', 'N/A')
    estado_subida = status.get('uploadStatus', 'N/A')

    duracion_iso = contentDetails.get('duration', 'N/A')
    duracion_legible = formatear_duracion(duracion_iso)

    tipo_contenido = contentDetails.get('definition', 'N/A')  # ej: hd o sd

    subs = obtener_suscriptores_canal(canal_id) if canal_id else "No disponible"

    print_rojo(f"Título: {titulo}")
    print_rojo(f"URL: https://youtu.be/{video_id}")
    print_rojo(f"Canal: {canal} (ID: {canal_id})")
    print_rojo(f"Suscriptores del canal: {subs}")
    print_rojo(f"Fecha de subida: {fecha}")
    print_rojo(f"Vistas: {vistas}")
    print_rojo(f"Likes: {likes}")
    print_rojo(f"Comentarios: {comentarios}")
    print_rojo(f"Duración: {duracion_legible}")
    print_rojo(f"Tipo de contenido (definición): {tipo_contenido}")
    print_rojo(f"Privacidad: {privacidad}")
    print_rojo(f"Estado de subida: {estado_subida}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        url = input("\033[91mPega la URL del video de YouTube: \033[0m").strip()
    else:
        url = sys.argv[1]
    video_id = extraer_video_id(url)
    if not video_id:
        print("\033[91mNo se pudo extraer el ID del video de la URL proporcionada.\033[0m")
    else:
        obtener_info_video(video_id)
