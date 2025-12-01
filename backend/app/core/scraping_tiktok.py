import csv
import time
import random
from playwright.sync_api import sync_playwright

# --- CONFIGURACIÓN ---
USUARIO = "senu.software"
URL_PERFIL = f"https://www.tiktok.com/@{USUARIO}"
ARCHIVO_CSV = "datos_tiktok_completo.csv"
CANTIDAD_A_ESCANEAR = 10  # Ajusta esto a cuántos videos quieres traer

def limpiar_texto(elemento):
    """Limpia saltos de linea y espacios extra"""
    if elemento:
        return elemento.inner_text().strip().replace('\n', ' ')
    return "0"

def run():
    with sync_playwright() as p:
        # Lanzamos navegador visible
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print(f"--- 1. Entrando al perfil: {URL_PERFIL} ---")
        page.goto(URL_PERFIL)

        # ==========================================
        # PAUSA PARA CAPTCHA Y LOGIN (CRUCIAL)
        # ==========================================
        print("\n" + "="*60)
        print(">>> PAUSA DE SEGURIDAD <<<")
        print("1. Resuelve el CAPTCHA manual en el navegador.")
        print("2. IMPORTANTE: Inicia Sesión (Login) para poder ver los 'Guardados'.")
        print("   (Si no te logueas, TikTok oculta la cantidad de Saves).")
        print("3. Cuando veas tu perfil cargado correctamente, vuelve aquí.")
        input("PRESIONA [ENTER] PARA COMENZAR LA EXTRACCIÓN...")
        print("="*60 + "\n")

        # Scroll para cargar videos en el grid
        print("Escaneando perfil...")
        for _ in range(3):
            page.mouse.wheel(0, 1000)
            time.sleep(1)

        # Seleccionar videos del grid
        videos_grid = page.locator('[data-e2e="user-post-item"]')
        count = videos_grid.count()
        print(f"--> Videos detectados: {count}")

        items_a_procesar = []
        limit = min(count, CANTIDAD_A_ESCANEAR)

        # Primera pasada: Sacar URL y Views desde el perfil (es más exacto)
        for i in range(limit):
            elemento = videos_grid.nth(i)
            link = elemento.locator('a').get_attribute('href')
            try:
                views = elemento.locator('[data-e2e="video-views"]').inner_text()
            except:
                views = "0"
            items_a_procesar.append({"url": link, "views": views})

        # Preparar CSV con TODOS los encabezados que pediste
        encabezados = [
            'fecha_subida', 
            'views', 
            'likes', 
            'comments', 
            'shares', 
            'saves', 
            'tipo_contenido', 
            'caption_titulo', 
            'url_video'
        ]

        with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=encabezados)
            writer.writeheader()

            print(f"--> Iniciando extracción detallada de {limit} videos...")

            for idx, item in enumerate(items_a_procesar):
                url = item['url']
                print(f"[{idx+1}/{limit}] Procesando...", end=" ")

                try:
                    # Navegación rápida (sin esperar carga completa de multimedia)
                    page.goto(url, wait_until='domcontentloaded', timeout=20000)
                    
                    # Pequeña espera para asegurar que el DOM dinámico de React cargó
                    # Esperamos a que aparezca al menos el botón de likes o timeout de 2s
                    try:
                        page.wait_for_selector('[data-e2e="like-count"]', timeout=3000)
                    except:
                        pass 

                    # --- EXTRACCIÓN DE DATOS ---

                    # 1. Caption (Título)
                    try: 
                        caption = limpiar_texto(page.locator('[data-e2e="browse-video-desc"]'))
                    except: caption = "Sin titulo"

                    # 2. Fecha
                    try:
                        fecha = limpiar_texto(page.locator('[data-e2e="browser-video-desc-date"]'))
                    except: fecha = "No encontrada"

                    # 3. Likes
                    try:
                        likes = limpiar_texto(page.locator('[data-e2e="like-count"]'))
                    except: likes = "0"

                    # 4. Comments
                    try:
                        comments = limpiar_texto(page.locator('[data-e2e="comment-count"]'))
                    except: comments = "0"
                    elif "photo" in page.url: # A veces la URL lo dice
                        tipo = "Foto"
                    else:
                        tipo = "Video"

                    # Guardar fila
                    writer.writerow({
                        'fecha_subida': fecha,
                        'views': item['views'], # Usamos la view del grid original
                        'likes': likes,
                        'comments': comments,
                        'shares': shares,
                        'saves': saves,
                        'tipo_contenido': tipo,
                        'caption_titulo': caption,
                        'url_video': url
                    })
                    print("✅ OK")

                except Exception as e:
                    print(f"❌ Error: {e}")
                    # Guardamos al menos lo básico para no perder el rastro
                    writer.writerow({
                        'fecha_subida': 'ERROR',
                        'views': item['views'],
                        'url_video': url,
                        'caption_titulo': 'Error al leer video'
                    })

        browser.close()
        print(f"\n¡TERMINADO! Revisa el archivo: {ARCHIVO_CSV}")

if __name__ == "__main__":
    run()