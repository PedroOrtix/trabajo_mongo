import json

def get_loot(db):
    # Retrieve basic details of all loot items
    loot_items = list(db.loot.find({}, {'_id': 0, 'id': 1, 'name': 1}))
    return json.dumps(loot_items)

def get_loot_by_id(db, loot_id):
    # Retrieve detailed information about a specific loot item
    # from in_rooms atribute take the room_id and dungeon_id
    loot = db.loot.find_one({'id': loot_id}, {'_id': 0, 'in_rooms': 0})
    if loot:
        rooms = list(db.rooms.find({'loot.id': loot_id}, {'_id': 0, 'room_id': 1, 'room_name': 1, 'dungeon_id': 1, 'dungeon_name': 1}))
        loot['rooms'] = rooms
    return json.dumps(loot)
    

def get_monster(db):
    # Retrieve basic details of all monsters
    monsters = list(db.monsters.find({}, {'_id': 0, 'id': 1, 'name': 1, 'level': 1, 'type': 1}))
    return json.dumps(monsters)

def get_monster_by_id(db, monster_id):
    # Retrieve detailed information about a specific monster
    monster = db.monsters.find_one({'id': monster_id}, {'_id': 0})
    if monster:
        rooms = list(db.rooms.find({'monsters.id': monster_id}, {'_id': 0, 'room_id': 1, 'room_name': 1, 'dungeon_id': 1, 'dungeon_name': 1}))
        monster['rooms'] = rooms
    return json.dumps(monster)

def get_dungeons(db):
    # Aggregate and list unique dungeons from the rooms collection
    pipeline = [
        {
            "$group": {
                "_id": "$dungeon_id",
                "name": {"$first": "$dungeon_name"},
                "dungeon_id": {"$first": "$dungeon_id"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "dungeon_id": 1,
                "name": 1
            }
        }
    ]
    dungeons = list(db.rooms.aggregate(pipeline))
    return json.dumps(dungeons)

def get_dungeon_by_id(db, dungeon_id):
    # Retrieve all rooms associated with a specific dungeon ID
    rooms = list(db.rooms.find({"dungeon_id": dungeon_id}, {'_id': 0}))
    if rooms:
        dungeon = {
            "dungeon_id": dungeon_id,
            "name": rooms[0]['dungeon_name'] if rooms else None,
            "rooms": rooms
        }
    else:
        dungeon = {}
    return json.dumps(dungeon)

def get_room_by_id(db, room_id):
    # Retrieve detailed information about a specific room
    room = db.rooms.find_one({'room_id': room_id}, {'_id': 0})
    return json.dumps(room)

def get_user(db):
    # Retrieve basic details of all users
    users = list(db.users.find({}, {'_id': 0, 'email': 1, 'user_name': 1, 'country': 1}))
    return json.dumps(users)

def get_user_by_email(db, email):
    # Retrieve detailed information about a user by email
    user = db.users.find_one({'email': email}, {'_id': 0})
    return json.dumps(user)
