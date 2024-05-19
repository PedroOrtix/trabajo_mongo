import json

def get_loot(db):
    """
    Retrieves all loot items from the database.

    Args:
        db (Database): The database connection object.

    Returns:
        list: A list of dictionaries, each containing the 'id' and 'name' of a loot item.
    """
    loot_items = list(db.loot.find({}, {'_id': 0, 'id': 1, 'name': 1}))
    return loot_items


def get_loot_by_id(db, loot_id):
    """
    Retrieves a specific loot item by its ID from the database.

    Args:
        db (Database): The database connection object.
        loot_id (int): The ID of the loot item to retrieve.

    Returns:
        dict: A dictionary containing the details of the loot item, with 'amount' omitted from 'in_rooms'.
    """
    loot = db.loot.find_one({'id': loot_id}, {'_id': 0})

    if loot.get('in_rooms') is not None:
        loot['in_rooms'] = [{'room_id': room['room_id'],
                            'room_name': room['room_name'],
                            'dungeon_id': room['dungeon_id'],
                            'dungeon_name': room['dungeon_name']} for room in loot['in_rooms']]

    return loot


def get_monster(db):
    """
    Retrieves all monsters from the database.

    Args:
        db (Database): The database connection object.

    Returns:
        list: A list of dictionaries, each containing the 'id', 'name', 'level', and 'type' of a monster.
    """
    monsters = list(db.monsters.find({}, {'_id': 0, 'id': 1, 'name': 1, 'level': 1, 'type': 1}))
    return monsters


def get_monster_by_id(db, monster_id):
    """
    Retrieves a specific monster by its ID from the database.

    Args:
        db (Database): The database connection object.
        monster_id (int): The ID of the monster to retrieve.

    Returns:
        dict: A dictionary containing the details of the monster, with 'amount' omitted from 'in_rooms'.
    """
    monster = db.monsters.find_one({'id': monster_id}, {'_id': 0})

    if monster.get('in_rooms') is not None:
        monster['in_rooms'] = [{'room_id': room['room_id'],
                                'room_name': room['room_name'],
                                'dungeon_id': room['dungeon_id'],
                                'dungeon_name': room['dungeon_name']} for room in monster['in_rooms']]
    return monster


def get_dungeons(db):
    """
    Retrieves a list of all dungeons from the database.

    Args:
        db (Database): The database connection object.

    Returns:
        str: A JSON string representing a list of dictionaries, each containing 'dungeon_id' and 'name'.
    """
    pipeline = [
        {
            "$group": {
                "_id": "$dungeon_id",
                "dungeon_id": {"$first": "$dungeon_id"},
                "name": {"$first": "$dungeon_name"},
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
    """
    Retrieves detailed information about a specific dungeon by its ID.

    Args:
        db (Database): The database connection object.
        dungeon_id (int): The ID of the dungeon to retrieve.

    Returns:
        list: A list containing a single dictionary with detailed information about the dungeon and its rooms.
    """
    pipeline = [
        {"$match": {"dungeon_id": dungeon_id}},
        {"$group": {
            "_id": "$dungeon_id",
            "name": {"$first": "$dungeon_name"},
            "rooms": {"$push": {
                "room_id": "$room_id",
                "room_name": "$room_name",
                "connected_rooms": "$rooms_connected",
                "monsters": {
                    "$map": {
                        "input": "$monsters",
                        "as": "monster",
                        "in": {
                            "id": "$$monster.id",
                            "name": "$$monster.name"
                        }
                    }
                },
                "loots": {
                    "$map": {
                        "input": "$loot",
                        "as": "loot",
                        "in": {
                            "id": "$$loot.id",
                            "name": "$$loot.name"
                        }
                    }
                },
                "bug": {"$sum": {"$cond": [{"$eq": ["$hints.category", "bug"]}, 1, 0]}},
                "hint": {"$sum": {"$cond": [{"$eq": ["$hints.category", "hint"]}, 1, 0]}},
                "lore": {"$sum": {"$cond": [{"$eq": ["$hints.category", "lore"]}, 1, 0]}},
                "suggestion": {"$sum": {"$cond": [{"$eq": ["$hints.category", "suggestion"]}, 1, 0]}},
            }}
        }},
        {"$project": {
            "_id": 0,
            "id": "1",
            "name": 1,
            "rooms": 1
        }}
    ]

    result = list(db.rooms.aggregate(pipeline))

    def remove_duplicates(rooms):
        for room in rooms:
            if 'monsters' in room and isinstance(room['monsters'], list):
                unique_monsters = {}
                for monster in room['monsters']:
                    if 'id' in monster:
                        unique_monsters[monster['id']] = monster
                room['monsters'] = list(unique_monsters.values())

            if 'loots' in room and isinstance(room['loots'], list):
                unique_loots = {}
                for loot in room['loots']:
                    if 'id' in loot:
                        unique_loots[loot['id']] = loot
                room['loots'] = list(unique_loots.values())

        return rooms

    for dungeon in result:
        dungeon['rooms'] = remove_duplicates(dungeon['rooms'])

    return result


def get_room_by_id(db, room_id):
    """
    Retrieves detailed information about a specific room by its ID.

    Args:
        db (Database): The database connection object.
        room_id (int): The ID of the room to retrieve.

    Returns:
        list: A list containing a single dictionary with detailed information about the room, its monsters, loots, and hints.
    """
    pipeline = [
        {"$match": {"room_id": room_id}},
        {"$lookup": {
            "from": "monsters",
            "localField": "monsters",
            "foreignField": "monster_id",
            "as": "monster_details"
        }},
        {"$lookup": {
            "from": "loots",
            "localField": "loot",
            "foreignField": "loot_id",
            "as": "loot_details"
        }},
        {"$project": {
            "_id": 0,
            "idR": "$room_id",
            "name": "$room_name",
            "inWP": "$in_waypoint",
            "outWP": "$out_waypoint",
            "monsters": {
                "$map": {
                    "input": "$monster_details",
                    "as": "monster",
                    "in": {
                        "idM": "$$monster.monster_id",
                        "name": "$$monster.name",
                        "type": "$$monster.type",
                        "level": "$$monster.level",
                        "place": "$$monster.place",
                        "exp": "$$monster.exp",
                        "manPage": "$$monster.manPage"
                    }
                }
            },
            "loots": {
                "$map": {
                    "input": "$loot_details",
                    "as": "loot",
                    "in": {
                        "idL": "$$loot.loot_id",
                        "name": "$$loot.name",
                        "type1": "$$loot.type1",
                        "type2": "$$loot.type2",
                        "weight": "$$loot.weight",
                        "gold": "$$loot.gold"
                    }
                }
            },
            "hints": "$hints"
        }}
    ]

    result = list(db.rooms.aggregate(pipeline))
    return result


def get_user(db):
    """
    Retrieves all users from the database.

    Args:
        db (Database): The database connection object.

    Returns:
        list: A list of dictionaries, each containing 'email', 'user_name', and 'country' of a user.
    """
    users = list(db.users.find({}, {'_id': 0, 'email': 1, 'user_name': 1, 'country': 1}))
    return users


def get_user_by_email(db, email):
    """
    Retrieves a specific user by their email from the database.

    Args:
        db (Database): The database connection object.
        email (str): The email of the user to retrieve.

    Returns:
        dict: A dictionary containing the details of the user.
    """
    user = db.users.find_one({'email': email}, {'_id': 0})
    return user
