"""
Script para llenar la base de datos con todos los packs de Mortal Kombat Mobile
Basado en información del Wiki oficial: https://mortalkombat-mobile.fandom.com/wiki/Packs
"""

from database import init_db, get_session, MKPack

def clear_existing_packs():
    """Eliminar packs existentes"""
    session = get_session()
    try:
        session.query(MKPack).delete()
        session.commit()
        print("✅ Packs anteriores eliminados")
    except Exception as e:
        session.rollback()
        print(f"❌ Error al eliminar packs: {e}")
    finally:
        session.close()

def add_mk_mobile_packs():
    """Agregar todos los packs de MK Mobile del wiki"""
    
    init_db()
    clear_existing_packs()
    session = get_session()
    
    try:
        # ================== PACKS DE ALMAS (SOUL BOOSTERS) ==================
        soul_packs = [
            MKPack(
                name="Pack de Almas - Pequeño",
                price=4.99,
                souls_cost=0,
                description="150 almas para comprar personajes y packs especiales"
            ),
            MKPack(
                name="Pack de Almas - Mediano",
                price=9.99,
                souls_cost=0,
                description="450 almas para comprar personajes y packs especiales"
            ),
            MKPack(
                name="Pack de Almas - Grande",
                price=19.99,
                souls_cost=0,
                description="1,100 almas para comprar personajes y packs especiales"
            ),
            MKPack(
                name="Pack de Almas - Enorme",
                price=49.99,
                souls_cost=0,
                description="3,600 almas para comprar personajes y packs especiales"
            ),
            MKPack(
                name="Pack de Almas - Masivo",
                price=99.99,
                souls_cost=0,
                description="8,000 almas para comprar personajes y packs especiales"
            ),
        ]
        
        # ================== PACKS DE PERSONAJES PERMANENTES ==================
        character_packs = [
            MKPack(
                name="Bronze Pack",
                price=0.0,
                souls_cost=15,
                description="Pack básico con personajes de bronce. Ideal para empezar tu colección."
            ),
            MKPack(
                name="Silver Pack",
                price=0.0,
                souls_cost=30,
                description="Pack con personajes de plata de mayor rareza y poder."
            ),
            MKPack(
                name="Gold Pack",
                price=0.0,
                souls_cost=150,
                description="Pack con personajes de oro de alta rareza. Mayor poder y habilidades."
            ),
            MKPack(
                name="Challenge Pack",
                price=0.0,
                souls_cost=350,
                description="Pack especial con personajes de desafío y equipo. Posibilidad de obtener personajes únicos."
            ),
            MKPack(
                name="MK11 Kombat Pack",
                price=0.0,
                souls_cost=400,
                description="Pack con personajes de MK11. 90% Oro, posibilidad de MK11 Scorpion, Sub-Zero, Raiden, Jade y Kabal."
            ),
            MKPack(
                name="Klassic Kombat Pack",
                price=0.0,
                souls_cost=400,
                description="Pack con personajes Klassic. Posibilidad de obtener Klassic Goro diamante y personajes clásicos de oro."
            ),
            MKPack(
                name="Equipment Pack",
                price=0.0,
                souls_cost=80,
                description="Pack con equipo aleatorio para mejorar a tus luchadores."
            ),
        ]
        
        # ================== PACKS ESPECIALES / STARTER ==================
        special_packs = [
            MKPack(
                name="Silver Sword Starter Pack",
                price=2.99,
                souls_cost=0,
                description="Pack de inicio único con personaje de plata y recursos. Solo se puede comprar una vez."
            ),
            MKPack(
                name="Gold Fire Starter Pack",
                price=9.99,
                souls_cost=0,
                description="Pack de inicio único con personaje de oro de tipo fuego. Solo se puede comprar una vez."
            ),
            MKPack(
                name="Gold Ice Starter Pack",
                price=9.99,
                souls_cost=0,
                description="Pack de inicio único con personaje de oro de tipo hielo. Solo se puede comprar una vez."
            ),
            MKPack(
                name="Anniversary Pack",
                price=0.0,
                souls_cost=0,
                description="Pack gratuito de aniversario (solo en Mayo). Contiene almas, koins, cartas de apoyo y equipo."
            ),
        ]
        
        # ================== PACKS HISTÓRICOS / DESCONTINUADOS ==================
        discontinued_packs = [
            MKPack(
                name="Elite Pack",
                price=0.0,
                souls_cost=390,
                available=False,
                description="[DESCONTINUADO] Challenge Pack mejorado con 8% de probabilidad de diamante. Ya no disponible desde Update 2.0."
            ),
            MKPack(
                name="Netherrealm Pack",
                price=0.0,
                souls_cost=350,
                available=False,
                description="[DESCONTINUADO] Pack especial con personajes del Netherrealm. Ya no disponible."
            ),
            MKPack(
                name="Horror Team Pack",
                price=0.0,
                souls_cost=400,
                available=False,
                description="[DESCONTINUADO] Pack temporal con personajes de terror como Jason Voorhees y Freddy Krueger."
            ),
            MKPack(
                name="Spec Ops Scorpion Kombat Pack",
                price=0.0,
                souls_cost=300,
                available=False,
                description="[DESCONTINUADO] Pack temporal exclusivo de Spec Ops Scorpion."
            ),
        ]
        
        # Agregar todos los packs
        all_packs = soul_packs + character_packs + special_packs + discontinued_packs
        
        for pack in all_packs:
            session.add(pack)
        
        session.commit()
        
        print("\n" + "="*70)
        print("✅ PACKS DE MK MOBILE AGREGADOS EXITOSAMENTE")
        print("="*70)
        print(f"\n📊 Resumen:")
        print(f"   • Packs de Almas: {len(soul_packs)}")
        print(f"   • Packs de Personajes: {len(character_packs)}")
        print(f"   • Packs Especiales/Starter: {len(special_packs)}")
        print(f"   • Packs Descontinuados: {len(discontinued_packs)}")
        print(f"   • TOTAL: {len(all_packs)} packs")
        print("\n" + "="*70)
        print("\n💡 Los packs están listos para consultarse en el bot de Telegram")
        print("   Usa /packs para ver todos los packs disponibles")
        print("="*70 + "\n")
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ Error al agregar packs: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    add_mk_mobile_packs()
