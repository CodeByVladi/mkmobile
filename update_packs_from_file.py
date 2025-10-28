"""
Script para actualizar la base de datos con los packs proporcionados por el usuario
"""

from database import init_db, get_session, MKPack

def parse_pack_line(line):
    """Parsear una línea del formato: 'Pack de Desafío — 50 almas'"""
    if '—' not in line:
        return None
    
    parts = line.split('—')
    if len(parts) != 2:
        return None
    
    name = parts[0].strip()
    cost_part = parts[1].strip()
    
    # Determinar si es almas o cristales
    if 'alma' in cost_part.lower():
        cost = int(cost_part.split()[0])
        return {'name': name, 'souls': cost, 'crystals': 0}
    elif 'cristal' in cost_part.lower():
        cost = int(cost_part.split()[0])
        return {'name': name, 'souls': 0, 'crystals': cost}
    
    return None

def load_packs_from_file():
    """Cargar packs desde el archivo"""
    
    # Inicializar base de datos
    init_db()
    
    # Leer archivo
    file_path = 'attached_assets/Pasted-Pack-de-Desaf-o-50-almas-Pack-de-Oro-150-almas-Pack-Guardi-n-de-Diamante-450-almas-Pack-Tienda-1761673919568_1761673919568.txt'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Parsear packs
    packs_data = []
    for line in lines:
        pack_info = parse_pack_line(line)
        if pack_info:
            packs_data.append(pack_info)
    
    # Limpiar base de datos
    session = get_session()
    try:
        session.query(MKPack).delete()
        session.commit()
        print("✅ Packs anteriores eliminados")
    except Exception as e:
        session.rollback()
        print(f"⚠️  No se pudieron eliminar packs anteriores: {e}")
    finally:
        session.close()
    
    # Agregar nuevos packs
    session = get_session()
    try:
        for pack_data in packs_data:
            pack = MKPack(
                name=pack_data['name'],
                price=0.0,
                souls_cost=pack_data['souls'],
                crystals_cost=pack_data['crystals'],
                available=True
            )
            session.add(pack)
        
        session.commit()
        
        # Contar packs por tipo
        souls_packs = sum(1 for p in packs_data if p['souls'] > 0)
        crystals_packs = sum(1 for p in packs_data if p['crystals'] > 0)
        
        print("\n" + "="*70)
        print("✅ PACKS ACTUALIZADOS EXITOSAMENTE")
        print("="*70)
        print(f"\n📊 Resumen:")
        print(f"   • Packs con Almas: {souls_packs}")
        print(f"   • Packs con Cristales: {crystals_packs}")
        print(f"   • TOTAL: {len(packs_data)} packs")
        print("\n" + "="*70)
        print("\n💡 Los packs están listos para consultarse en el bot")
        print("   Usa /packs para ver todos los packs")
        print("="*70 + "\n")
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ Error al agregar packs: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    load_packs_from_file()
