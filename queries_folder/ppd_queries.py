import json

### POST QUERIES ###
def post_comment(db, user_email, room_id, text, category):
    comment = {
        'user_email': user_email,
        'room_id': room_id,
        'text': text,
        'category': category
    }
    db.comments.insert_one(comment)
    return json.dumps({'status': 'success', 'message': 'Comment added'})

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
        'dungeon_id': dungeon_id,
        'dungeon_name': dungeon_name,
        'dungeon_lore': dungeon_lore,
        'room_name': room_name,
        'rooms_connected': [{'room_id': rid} for rid in rooms_connected],
        'inWP': inWP,
        'outWP': outWP
    }
    db.rooms.insert_one(room)
    return json.dumps({'status': 'success', 'message': 'Room added'})

### PUT QUERIES ###
def put_room_monsters(db, room_id, monsters):
    # Verify monsters exist
    existing_monsters = db.monsters.find({'id': {'$in': monsters}}, {'_id': 0, 'id': 1})
    existing_monsters_ids = [m['id'] for m in existing_monsters]
    if len(existing_monsters_ids) != len(monsters):
        return json.dumps({'status': 'error', 'message': 'One or more monsters do not exist'})

    # Update the room with new monsters
    db.rooms.update_one(
        {'room_id': room_id},
        {'$set': {'monsters': [{'id': mid} for mid in monsters]}}
    )
    return json.dumps({'status': 'success', 'message': 'Monsters updated in room'})

def put_room_loot(db, room_id, loot):
    # Verify loot items exist
    existing_loot = db.loot.find({'id': {'$in': loot}}, {'_id': 0, 'id': 1})
    existing_loot_ids = [lt['id'] for lt in existing_loot]
    if len(existing_loot_ids) != len(loot):
        return json.dumps({'status': 'error', 'message': 'One or more loot items do not exist'})

    # Update the room with new loot
    db.rooms.update_one(
        {'room_id': room_id},
        {'$set': {'loot': [{'id': lid} for lid in loot]}}
    )
    return json.dumps({'status': 'success', 'message': 'Loot updated in room'})

def put_room_connections(db, room_id, connections):
    # Verify room connections exist
    existing_rooms = db.rooms.find({'room_id': {'$in': connections}}, {'_id': 0, 'room_id': 1})
    existing_room_ids = [r['room_id'] for r in existing_rooms]
    if len(existing_room_ids) != len(connections):
        return json.dumps({'status': 'error', 'message': 'One or more connected rooms do not exist'})

    # Update the room with new connections
    db.rooms.update_one(
        {'room_id': room_id},
        {'$set': {'rooms_connected': [{'room_id': rid} for rid in connections]}}
    )
    return json.dumps({'status': 'success', 'message': 'Room connections updated'})

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
