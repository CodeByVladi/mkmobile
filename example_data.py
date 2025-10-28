"""
Script de ejemplo para agregar datos iniciales a la base de datos.
Ejecuta este script después de configurar el token del bot para agregar datos de ejemplo.
"""

from database import init_db, get_session, MKPack, Video

def add_sample_data():
    """Agregar datos de ejemplo a la base de datos"""
    
    # Inicializar la base de datos
    init_db()
    session = get_session()
    
    try:
        # Verificar si ya hay datos
        existing_packs = session.query(MKPack).count()
        if existing_packs > 0:
            print("La base de datos ya contiene packs. No se agregarán datos de ejemplo.")
            return
        
        # Agregar packs de ejemplo
        packs = [
            MKPack(
                name="Diamond Pack",
                price=29.99,
                souls_cost=800,
                description="Pack con personajes diamante de alta rareza"
            ),
            MKPack(
                name="Elite Pack",
                price=19.99,
                souls_cost=450,
                description="Pack con personajes de oro y diamante"
            ),
            MKPack(
                name="Kombat Pack",
                price=14.99,
                souls_cost=300,
                description="Pack con personajes aleatorios de oro"
            ),
            MKPack(
                name="Starter Pack",
                price=4.99,
                souls_cost=150,
                description="Pack para nuevos jugadores con personajes básicos"
            ),
            MKPack(
                name="Souls Pack 1",
                price=9.99,
                souls_cost=550,
                description="Pack de 550 almas para compras en la tienda"
            ),
        ]
        
        for pack in packs:
            session.add(pack)
        
        # Agregar videos de ejemplo
        videos = [
            Video(
                title="Nueva actualización de Mortal Kombat Mobile",
                url="https://youtube.com/watch?v=example1",
                description="Descubre las nuevas características de la última actualización"
            ),
            Video(
                title="Los mejores personajes diamante",
                url="https://youtube.com/watch?v=example2",
                description="Guía completa de los personajes diamante más poderosos"
            ),
            Video(
                title="Cómo conseguir almas gratis",
                url="https://youtube.com/watch?v=example3",
                description="Tips y trucos para obtener almas sin gastar dinero"
            ),
        ]
        
        for video in videos:
            session.add(video)
        
        session.commit()
        print("✅ Datos de ejemplo agregados exitosamente!")
        print(f"   - {len(packs)} packs agregados")
        print(f"   - {len(videos)} videos agregados")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error al agregar datos: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    add_sample_data()
