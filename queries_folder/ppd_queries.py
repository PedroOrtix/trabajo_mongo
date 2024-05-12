import json
from datetime import datetime

### POST QUERIES ###
def post_comment(db, user_email, room_id, text, category):
    # tenemos que verificar que el user_email exista
    user = db.users.find_one({"email": user_email})
    if not user:
        return {"status": "error", "message": "User does not exist"}
    
    # tennemos que verificar que la room_id exista
    room = db.rooms.find_one({"room_id": room_id})
    if not room:
        return {"status": "error", "message": "Room does not exist"}
    
    new_hint = {
        "text": text,
        "category": category,
        "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "referemces_room": {
            "room_id": room_id,
            "room_name": room["room_name"],
            "dungeon_id": room["dungeon_id"],
            "dungeon_name": room["dungeon_name"]
        }
    }
    
    db.users.update_one(
        {"email": user_email},
        {"$push": {"hints": new_hint}}
    )
    
    # ahora tenemos que actualizar la colleciuon de rooms "hints"
    
    db.rooms.update_one(
        {"room_id": room_id},
        {"$push": {"hints": {
            "category": category,
            "hintText": text,
            "publish_by": {
                "email": user_email,
                "country": user["country"],
                "user_name": user["name"],
                "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            }
        },
            "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}}
        )

    return {"status": "success", "message": "Comment added"}
    
def post_monster(db, name, type, level, place, exp, man_page):
    monster = {
        'name': name,
        'type': type,
        'level': level,
        'place': place,
        'exp': exp,
        'man_page': man_page
    }
    db.monsters.insert_one(monster)
    return json.dumps({'status': 'success', 'message': 'Monster added'})

def post_loot(db, name, type1, type2, weight, gold):
    loot = {
        'name': name,
        'type1': type1,
        'type2': type2,
        'weight': weight,
        'gold': gold
    }
    db.loot.insert_one(loot)
    return json.dumps({'status': 'success', 'message': 'Loot added'})

def post_room(db, dungeon_id, dungeon_name, dungeon_lore, room_name, rooms_connected, inWP=None, outWP=None):
    room = {
        'room_id': db.rooms.count_documents({}) + 1,
        'dungeon_id': dungeon_id,
        'dungeon_name': dungeon_name,
        'dungeon_lore': dungeon_lore,
        'room_name': room_name,
        'rooms_connected': [{'room_id': rid,
                            'room_name': db.rooms.find_one({'room_id': rid})['room_name']
                            } for rid in rooms_connected],
        'inWP': inWP,
        'outWP': outWP
    }
    db.rooms.insert_one(room)
    
    # por cada room conectada, tenemos que agregar la referencia a la nueva room
    for rid in rooms_connected:
        db.rooms.update_one(
            {'room_id': rid},
            {'$push': {'rooms_connected': {'room_id': room['room_id'], 'room_name': room_name}}}
        )
    
    return json.dumps({'status': 'success', 'message': 'Room added'})

### PUT QUERIES ###
def put_room_monsters(db, room_id, monsters):
    # verificamos si los monsters existen
    existing_monsters = db.monsters.find({'id': {'$in': monsters}}, {'_id': 0, 'id': 1})
    existing_monsters_ids = [m['id'] for m in existing_monsters]
    
    # si la cantida de monsters que existe es diferente a la cantidad de monsters que se quieren agregar, raise error
    if len(existing_monsters_ids) != len(monsters):
        return json.dumps({'status': 'error', 'message': 'One or more monsters do not exist'})
    
    # Update the room with new monsters
    db.rooms.update_one(
        {'room_id': room_id},
        {'$set': {'monsters': [db.monsters.find_one({'id': mid}, {'_id': 0, 'in_rooms': 0})
                            for mid in monsters]}}
    )

def put_room_loot(db, room_id, loot):
    # verificamos si los loot existen
    existing_loot = db.loot.find({'id': {'$in': loot}}, {'_id': 0, 'id': 1})
    existing_loot_ids = [lt['id'] for lt in existing_loot]
    
    if len(existing_loot_ids) != len(loot):
        return json.dumps({'status': 'error', 'message': 'One or more loot items do not exist'})

    # hacer update de la room con el nuevo loot
    db.rooms.update_one(
        {'room_id': room_id},
        {'$set': {'loot': [db.loot.find_one({'id': lid}, {'_id': 0, 'in_rooms': 0})
                            for lid in loot]}}
    )

def put_room_connections(db, room_id, connections):
    # Verificar que las rooms existan
    existing_rooms = db.rooms.find({'room_id': {'$in': connections}}, {'_id': 0, 'room_id': 1})
    existing_room_ids = [r['room_id'] for r in existing_rooms]
    
    if len(existing_room_ids) != len(connections):
        return json.dumps({'status': 'error', 'message': 'One or more connected rooms do not exist'})

    # hacer update de la room con las nuevas conexiones
    db.rooms.update_one(
        {'room_id': room_id},
        {'$set': {'rooms_connected': [db.rooms.find_one({'room_id': rid}, {'_id': 0, 'room_id': 1, 'room_name': 1})
                                    for rid in connections]
                }
            }
        )

### DELETE QUERIES ###
def delete_room(db, room_id):
    # delete room and remove references from monsters and loot
    db.rooms.delete_one({'room_id': room_id})
    db.monsters.update_many(
        {'in_rooms.room_id': room_id}, 
        {'$pull': {'in_rooms': {'room_id': room_id}}}
    )
    db.loot.update_many(
        {'in_rooms.room_id': room_id},
        {'$pull': {'in_rooms': {'room_id': room_id}}}
    )
    return json.dumps({'status': 'success', 'message': 'Room and related comments deleted'})

def delete_monster(db, monster_id):
    db.monsters.delete_one({'id': monster_id})
    db.rooms.update_many(
        {'monsters.id': monster_id},
        {'$pull': {'monsters': {'id': monster_id}}}
    )
    return json.dumps({'status': 'success', 'message': 'Monster deleted'})

def delete_loot(db, loot_id):
    db.loot.delete_one({'id': loot_id})
    db.rooms.update_many(
        {'loot.id': loot_id},
        {'$pull': {'loot': {'id': loot_id}}}
    )
    return json.dumps({'status': 'success', 'message': 'Loot deleted'})
