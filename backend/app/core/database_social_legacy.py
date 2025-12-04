import requests
import pymysql
import ssl
from datetime import datetime, date
import os
# --- TUS DATOS ---
TOKEN = 'ewe'
IG_USER_ID = '1`'

# --- CONEXIÓN AIVEN ---
db_config = {
    'host': "mysql-senu-jhonnybarrios968.b.aivencloud.com",
    'port': 15797,
    'user': "avnadmin",
    'password': os.environ.get("DB_PASSWORD"),
    'db': "Mysoftware", 
    'cursorclass': pymysql.cursors.DictCursor,
    'ssl': {'fake_flag_to_enable': True}
}

def main():
    print("🚀 SINCRONIZANDO POSTS Y VIEWS...")
    
    try:
        conn = pymysql.connect(**db_config)
        print("✅ Conexión BD exitosa.")
        
        # 1. BUSCAR ID INTERNO
        internal_id = None
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM social_accounts WHERE external_id = %s", (IG_USER_ID,))
            acc = cursor.fetchone()
            if not acc:
                print("🤬 Error: No existe la cuenta en 'social_accounts'.")
                return
            internal_id = acc['id']

        # 2. EJECUTAR
        guardar_posts_con_views(conn, internal_id)

    except Exception as e:
        print(f"🔥 Error General: {e}")
    finally:
        conn.close()
        print("👋 Fin.")

def guardar_posts_con_views(conn, internal_id):
    print("\n📸 Bajando Posts con Views...")
    
    url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media"
    # AQUI PEDIMOS 'impressions' PARA LLENAR TUS 'VIEWS'
    params = {
        'fields': 'id,caption,media_type,permalink,timestamp,like_count,comments_count,insights.metric(reach,saved,impressions)',
        'access_token': TOKEN,
        'limit': 100 
    }
    
    try:
        resp = requests.get(url, params=params).json()
        posts = resp.get('data', [])
        print(f"📊 Procesando {len(posts)} publicaciones.")

        with conn.cursor() as cursor:
            for post in posts:
                permalink = post.get('permalink', '')[:255]
                caption = post.get('caption', '')
                media_type = post.get('media_type')
                ts = post.get('timestamp')
                
                fecha_completa_obj = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z")
                post_datetime = fecha_completa_obj.strftime('%Y-%m-%d %H:%M:%S')
                fecha_publicacion_corta = fecha_completa_obj.date() 

                # Métricas
                likes = post.get('like_count', 0)
                comments = post.get('comments_count', 0)
                reach = 0
                saves = 0
                views = 0 # Esta será tu columna 'views'
                
                if 'insights' in post:
                    for m in post['insights']['data']:
                        if m['name'] == 'reach': reach = m['values'][0]['value']
                        if m['name'] == 'saved': saves = m['values'][0]['value']
                        # Mapeamos impresiones -> views
                        if m['name'] == 'impressions': views = m['values'][0]['value']

                # 1. INSERTAR POST
                cursor.execute("SELECT id FROM social_posts WHERE url = %s", (permalink,))
                existe = cursor.fetchone()
                
                if existe:
                    post_db_id = existe['id']
                else:
                    sql_post = """
                        INSERT INTO social_posts 
                        (social_account_id, post_type, caption, posted_at, url, is_promoted, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, 0, NOW(), NOW())
                    """
                    cursor.execute(sql_post, (internal_id, media_type, caption, post_datetime, permalink))
                    post_db_id = conn.insert_id()

                # 2. INSERTAR MÉTRICAS CON VIEWS
                cursor.execute("SELECT post_id FROM social_post_metrics WHERE post_id=%s AND date=%s", (post_db_id, fecha_publicacion_corta))
                
                if not cursor.fetchone():
                    # AQUI AGREGAMOS LA COLUMNA views
                    sql_met = """
                        INSERT INTO social_post_metrics 
                        (post_id, date, reach, likes, comments, saves, views, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                    """
                    cursor.execute(sql_met, (post_db_id, fecha_publicacion_corta, reach, likes, comments, saves, views))
        
        conn.commit()
        print("🚀 ¡Posts guardados con VIEWS exitosamente!")

    except Exception as e:
        print(f"❌ Error en posts: {e}")

if __name__ == "__main__":
    main()