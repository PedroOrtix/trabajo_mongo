from datetime import datetime

### POST QUERIES ###
def post_comment(db, user_email, room_id, text, category):
    """
    Adds a comment to a specific room and user.

    Args:
        db (Database): The database connection object.
        user_email (str): The email of the user posting the comment.
        room_id (int): The ID of the room to post the comment in.
        text (str): The content of the comment.
        category (str): The category of the comment (e.g., bug, hint, lore, suggestion).

    Returns:
        dict: A status message indicating success or failure.
    """
    user = db.users.find_one({"email": user_email})
    if not user:
        return {"status": "error", "message": "User does not exist"}

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
    """
    Adds a new monster to the database.

    Args:
        db (Database): The database connection object.
        name (str): The name of the monster.
        type (str): The type of the monster.
        level (int): The level of the monster.
        place (str): The place where the monster can be found.
        exp (int): The experience points the monster gives.
        man_page (str): The manual page reference for the monster.

    Returns:
        dict: A status message indicating success.
    """
    monster = {
        'name': name,
        'type': type,
        'level': level,
        'place': place,
        'exp': exp,
        'man_page': man_page
    }
    db.monsters.insert_one(monster)
    return {'status': 'success', 'message': 'Monster added'}

def post_loot(db, name, type1, type2, weight, gold):
    """
    Adds new loot to the database.

    Args:
        db (Database): The database connection object.
        name (str): The name of the loot.
        type1 (str): The primary type of the loot.
        type2 (str): The secondary type of the loot.
        weight (float): The weight of the loot.
        gold (int): The gold value of the loot.

    Returns:
        dict: A status message indicating success.
    """
    loot = {
        'name': name,
        'type1': type1,
        'type2': type2,
        'weight': weight,
        'gold': gold
    }
    db.loot.insert_one(loot)
    return {'status': 'success', 'message': 'Loot added'}

def post_room(db, dungeon_id, dungeon_name, dungeon_lore, room_name, rooms_connected, inWP=None, outWP=None):
    """
    Adds a new room to the database and updates connections with other rooms.

    Args:
        db (Database): The database connection object.
        dungeon_id (int): The ID of the dungeon the room belongs to.
        dungeon_name (str): The name of the dungeon the room belongs to.
        dungeon_lore (str): The lore of the dungeon.
        room_name (str): The name of the room.
        rooms_connected (list): A list of room IDs that are connected to this room.
        inWP (str, optional): The waypoint to enter the room.
        outWP (str, optional): The waypoint to exit the room.

    Returns:
        dict: A status message indicating success.
    """
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
    
    for rid in rooms_connected:
        db.rooms.update_one(
            {'room_id': rid},
            {'$push': {'rooms_connected': {'room_id': room['room_id'], 'room_name': room_name}}}
        )
    
    return {'status': 'success', 'message': 'Room added'}

### PUT QUERIES ###
def put_room_monsters(db, room_id, monsters):
    """
    Updates the list of monsters in a specific room.

    Args:
        db (Database): The database connection object.
        room_id (int): The ID of the room to update.
        monsters (list): A list of monster IDs to add to the room.

    Returns:
        dict: A status message indicating success or failure.
    """
    existing_monsters = db.monsters.find({'id': {'$in': monsters}}, {'_id': 0, 'id': 1})
    existing_monsters_ids = [m['id'] for m in existing_monsters]
    
    if len(existing_monsters_ids) != len(monsters):
        return {'status': 'error', 'message': 'One or more monsters do not exist'}
    
    db.rooms.update_one(
        {'room_id': room_id},
        {'$set': {'monsters': [db.monsters.find_one({'id': mid}, {'_id': 0, 'in_rooms': 0})
                            for mid in monsters]}}
    )

def put_room_loot(db, room_id, loot):
    """
    Updates the list of loot items in a specific room.

    Args:
        db (Database): The database connection object.
        room_id (int): The ID of the room to update.
        loot (list): A list of loot item IDs to add to the room.

    Returns:
        dict: A status message indicating success or failure.
    """
    existing_loot = db.loot.find({'id': {'$in': loot}}, {'_id': 0, 'id': 1})
    existing_loot_ids = [lt['id'] for lt in existing_loot]
    
    if len(existing_loot_ids) != len(loot):
        return {'status': 'error', 'message': 'One or more loot items do not exist'}

    db.rooms.update_one(
        {'room_id': room_id},
        {'$set': {'loot': [db.loot.find_one({'id': lid}, {'_id': 0, 'in_rooms': 0})
                            for lid in loot]}}
    )

def put_room_connections(db, room_id, connections):
    """
    Updates the connections of a specific room with other rooms.

    Args:
        db (Database): The database connection object.
        room_id (int): The ID of the room to update.
        connections (list): A list of room IDs to connect to.

    Returns:
        dict: A status message indicating success or failure.
    """
    existing_rooms = db.rooms.find({'room_id': {'$in': connections}}, {'_id': 0, 'room_id': 1})
    existing_room_ids = [r['room_id'] for r in existing_rooms]
    
    if len(existing_room_ids) != len(connections):
        return {'status': 'error', 'message': 'One or more connected rooms do not exist'}

    db.rooms.update_one(
        {'room_id': room_id},
        {'$set': {'rooms_connected': [db.rooms.find_one({'room_id': rid}, {'_id': 0, 'room_id': 1, 'room_name': 1})
                                    for rid in connections]
                }
            }
        )

### DELETE QUERIES ###
def delete_room(db, room_id):
    """
    Deletes a specific room and removes references to it from monsters and loot.

    Args:
        db (Database): The database connection object.
        room_id (int): The ID of the room to delete.

    Returns:
        dict: A status message indicating success.
    """
    db.rooms.delete_one({'room_id': room_id})
    db.monsters.update_many(
        {'in_rooms.room_id': room_id}, 
        {'$pull': {'in_rooms': {'room_id': room_id}}}
    )
    db.loot.update_many(
        {'in_rooms.room_id': room_id},
        {'$pull': {'in_rooms': {'room_id': room_id}}}
    )
    db.users.update_many(
        {'hints.referemces_room.room_id': room_id},
        {'$pull': {'hints': {'referemces_room.room_id': room_id}}})
    
    return {'status': 'success', 'message': 'Room and related comments deleted'}

def delete_monster(db, monster_id):
    """
    Deletes a specific monster and removes references to it from rooms.

    Args:
        db (Database): The database connection object.
        monster_id (int): The ID of the monster to delete.

    Returns:
        dict: A status message indicating success.
    """
    db.monsters.delete_one({'id': monster_id})
    db.rooms.update_many(
        {'monsters.id': monster_id},
        {'$pull': {'monsters': {'id': monster_id}}}
    )
    return {'status': 'success', 'message': 'Monster deleted'}

def delete_loot(db, loot_id):
    """
    Deletes a specific loot item and removes references to it from rooms.

    Args:
        db (Database): The database connection object.
        loot_id (int): The ID of the loot item to delete.

    Returns:
        dict: A status message indicating success.
    """
    db.loot.delete_one({'id': loot_id})
    db.rooms.update_many(
        {'loot.id': loot_id},
        {'$pull': {'loot': {'id': loot_id}}}
    )
    return {'status': 'success', 'message': 'Loot deleted'}
