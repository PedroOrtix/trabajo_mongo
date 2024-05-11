import json

def get_loot(db):
    # Retrieve basic details of all loot items
    loot_items = list(db.loot.find({}, {'_id': 0, 'id': 1, 'name': 1}))
    return loot_items

def get_loot_by_id(db, loot_id):
    # Retrieve detailed information about a specific loot item
    # from in_rooms atribute take the room_id and dungeon_id
    loot = db.loot.find_one({'id': loot_id}, {'_id': 0})
    
    # vamos a omitir el atributo amount dentro de in_rooms
    if loot.get('in_rooms') is not None:
        loot['in_rooms'] = [{'room_id': room['room_id'],
                            'room_name': room['room_name'],
                            'dungeon_id': room['dungeon_id'],
                            'dungeon_name': room['dungeon_name'] } for room in loot['in_rooms']]
    
    return loot
    

def get_monster(db):
    monsters = list(db.monsters.find({}, {'_id': 0, 'id': 1, 'name': 1, 'level': 1, 'type': 1}))
    return monsters

def get_monster_by_id(db, monster_id):
    # Retrieve detailed information about a specific monster
    monster = db.monsters.find_one({'id': monster_id}, {'_id': 0})
    # vamos a omitir el atributo amount dentro de in_rooms
    if monster.get('in_rooms') is not None:
        monster['in_rooms'] = [{'room_id': room['room_id'],
                            'room_name': room['room_name'],
                            'dungeon_id': room['dungeon_id'],
                            'dungeon_name': room['dungeon_name'] } for room in monster['in_rooms']]
    return monster

def get_dungeons(db):
    # Aggregate and list unique dungeons from the rooms collection
    pipeline = [
        {
            "$group": {
                "_id": "$dungeon_id", # este id hace referencia a la instaciua dungeon_id de la coleccion rooms
                
                # vamos a tomar el primer valor de dungeon_id y dungeon_name
                "dungeon_id": {"$first": "$dungeon_id"},
                "name": {"$first": "$dungeon_name"},
                
            }
        },
        {
            # estos son los atributos que vamos proyectar
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
    pipeline = [
        # Filtrar documentos por dungeon_id
        {"$match": {"dungeon_id": dungeon_id}},
        
        # Agrupar por dungeon_id para consolidar la información
        {"$group": {
            "_id": "$dungeon_id",
            "name": {"$first": "$dungeon_name"},
            "rooms": {"$push": {
                "room_id": "$room_id",
                "room_name": "$room_name",
                "connected_rooms": "$rooms_connected",
                "monsters": "$monsters",  # Tenemos que sacar aun el id y nombre de los monstruos
                "loots": "$loot",  # Tenemos que sacar aun el id y nombre de los loots
                    "bug": {"$sum": {"$cond": [{"$eq": ["$hints.category", "bug"]}, 1, 0]}},
                    "hint": {"$sum": {"$cond": [{"$eq": ["$hints.category", "hint"]}, 1, 0]}},
                    "lore": {"$sum": {"$cond": [{"$eq": ["$hints.category", "lore"]}, 1, 0]}}
                }
            }}
        },
        
        # Seleccionar los campos a mostrar
        {"$project": {
            "_id": 0,
            "id": "1",
            "name": 1,
            "rooms": 1
        }   
        }
    ]
        
        
    result = list(db.rooms.aggregate(pipeline))
    return result

def get_room_by_id(db, room_id):
    
    pipeline = [
        # Filtrar para obtener solo la habitación con el ID específico
        {"$match": {"room_id": room_id}},
        
        # Unir con la colección de monstruos si es necesario, asumiendo una colección separada
        {"$lookup": {
            "from": "monsters",
            "localField": "monsters",  # Asume un campo que contiene IDs de monstruos en la habitación
            "foreignField": "monster_id",
            "as": "monster_details"
        }},
        
        # Unir con la colección de tesoros si es necesario, asumiendo una colección separada
        {"$lookup": {
            "from": "loots",
            "localField": "loot",  # Asume un campo que contiene IDs de tesoros en la habitación
            "foreignField": "loot_id",
            "as": "loot_details"
        }},
        
        # Proyectar la información necesaria
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

    # Ejecutar el pipeline de agregación
    result = list(db.rooms.aggregate(pipeline))
    return result

def get_user(db):
    # Retrieve basic details of all users
    users = list(db.users.find({}, {'_id': 0, 'email': 1, 'user_name': 1, 'country': 1}))
    return users

def get_user_by_email(db, email):
    # Retrieve detailed information about a user by email
    user = db.users.find_one({'email': email}, {'_id': 0})
    return user
