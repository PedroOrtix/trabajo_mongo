# MEMORIA TRABAJO MONOGODB
# Parte 1: Implementación de Funciones en Python con PyMongo

## Introducción

La empresa Norsewind Studios ha decidido migrar su base de datos relacional a una base de datos no relacional utilizando MongoDB. Este cambio busca mejorar la capacidad de manejo de datos debido al creciente número de jugadores de su videojuego "Jotun’s Lair". La base de datos contiene información sobre los monstruos, el loot del juego, las mazmorras y los comentarios de los usuarios.

## Objetivo

El objetivo principal de esta primera parte del proyecto es implementar las funciones necesarias para interactuar con la base de datos MongoDB desde Python, cubriendo todos los endpoints definidos en la API REST de la empresa. Estas funciones deben ser capaces de realizar operaciones de creación, lectura, actualización y eliminación (CRUD) sobre las colecciones relevantes: `loot`, `monsters`, `rooms`, `users`.

## Estructura de la Base de Datos

Las colecciones principales en la base de datos MongoDB son:
- **Loot**: Contiene información sobre los objetos del juego.
- **Monsters**: Contiene información sobre los monstruos del juego.
- **Rooms**: Contiene información sobre las habitaciones y sus conexiones, monstruos y loot presentes.
- **Users**: Contiene información sobre los usuarios y sus comentarios.

## Funciones Implementadas
Se pueden encontrar en la carpeta `queries_folder`.

### Funciones GET

1. **`get_loot(db)`**:
   - Esta función recupera todos los objetos de loot del juego. Devuelve una lista de diccionarios con los campos `id` y `name`.

2. **`get_loot_by_id(db, loot_id)`**:
   - Recupera un objeto de loot específico identificado por su `loot_id`. Omite el campo `amount` en la información de `in_rooms`.

3. **`get_monster(db)`**:
   - Recupera todos los monstruos del juego, devolviendo una lista de diccionarios con los campos `id`, `name`, `level` y `type`.

4. **`get_monster_by_id(db, monster_id)`**:
   - Recupera un monstruo específico identificado por su `monster_id`. Omite el campo `amount` en la información de `in_rooms`.

5. **`get_dungeons(db)`**:
   - Recupera todas las mazmorras del juego utilizando un pipeline de agregación para agrupar los datos por `dungeon_id` y `dungeon_name`.

6. **`get_dungeon_by_id(db, dungeon_id)`**:
   - Recupera información detallada sobre una mazmorra específica, incluyendo las habitaciones, conexiones entre habitaciones, monstruos y loot presentes, así como la cantidad de comentarios de cada categoría en cada habitación. Utiliza un pipeline de agregación y una función en Python para eliminar duplicados.

7. **`get_room_by_id(db, room_id)`**:
   - Recupera información detallada sobre una habitación específica, incluyendo los monstruos, loot y comentarios asociados.

8. **`get_user(db)`**:
   - Recupera información básica de todos los usuarios, incluyendo `email`, `user_name` y `country`.

9. **`get_user_by_email(db, email)`**:
   - Recupera información detallada sobre un usuario específico, identificado por su `email`.

### Funciones POST

1. **`post_comment(db, user_email, room_id, text, category)`**:
   - Añade un nuevo comentario a una habitación específica y lo asocia a un usuario. Verifica la existencia del usuario y la habitación antes de proceder.

2. **`post_monster(db, name, type, level, place, exp, man_page)`**:
   - Añade un nuevo monstruo al juego con la información proporcionada.

3. **`post_loot(db, name, type1, type2, weight, gold)`**:
   - Añade un nuevo objeto de loot al juego con la información proporcionada.

4. **`post_room(db, dungeon_id, dungeon_name, dungeon_lore, room_name, rooms_connected, inWP=None, outWP=None)`**:
   - Añade una nueva habitación a una mazmorra, actualizando las conexiones con otras habitaciones.

### Funciones PUT

1. **`put_room_monsters(db, room_id, monsters)`**:
   - Actualiza la lista de monstruos en una habitación específica. Verifica la existencia de los monstruos antes de actualizar.

2. **`put_room_loot(db, room_id, loot)`**:
   - Actualiza la lista de objetos de loot en una habitación específica. Verifica la existencia de los objetos de loot antes de actualizar.

3. **`put_room_connections(db, room_id, connections)`**:
   - Actualiza las conexiones de una habitación con otras habitaciones. Verifica la existencia de las habitaciones antes de actualizar.

### Funciones DELETE

1. **`delete_room(db, room_id)`**:
   - Elimina una habitación específica y remueve las referencias a ella de los monstruos y objetos de loot.

2. **`delete_monster(db, monster_id)`**:
   - Elimina un monstruo específico y remueve las referencias a él de las habitaciones.

3. **`delete_loot(db, loot_id)`**:
   - Elimina un objeto de loot específico y remueve las referencias a él de las habitaciones.


<br>
<br>
<br>

# Parte 2: COMPASS
## ej-1
### ej-1A. Haz una consulta que obtengan los datos necesarios para la colección y exporta el resultado a un fichero .json. Debajo puedes encontrar la estructura de la colección.
```
db.rooms.aggregate([
    {
        $unwind: "$hints" 
    },
    {
        $project: {
            _id: 0,
            Creation_date: "$hints.creation_date",
            HintText: "$hints.hintText",
            Category: "$hints.category",
            References_room: { 
                IdR: "$room_id", 
                Name: "$room_name",
                IdD: "$dungeon_id", 
                Dungeon: "$dungeon_name"
            },
            Publish_by: { 
                Email: "$hints.publish_by.email",
                User_name: "$hints.publish_by.user_name",
                CreationDate: "$hints.publish_by.creation_date",
                Country: "$hints.publish_by.country"
            }
        }
    },
    {
        $out: "Hints" 
    }
])
```
Si bien no estamos primero creando un json y luego subiendo ese json a la coleccion nueva, estamos creando directamente la colección en el script, desde donde ya se puede descargar el json. Esto es debido a que la única manera que hemos encontrado de generar el json primero era guardando el script en un fichero a parte y ejecutarlo, pero como tenemos la base de datos dentro de un contenedor es mucho lio.

<img src="https://lh7-us.googleusercontent.com/iMidEV1I_yk1osPrRLV461aJnvIPjcwXwW0jnk8PDwYrXGM3DSpwpS6S4og6AKKuefMPdOKj0ayQyQXXV09fLNzUBzhdYIl7CNMiX4UcjVRGTsvi0cC0tt7k_dfM7asUjttrXfgdwjn-6_CqRltWZb0" width="250"/>


<img src="https://lh7-us.googleusercontent.com/_Cxaqmw7Ndub6cDp_rRuV-y82nKcW0zOmxnPLk-BWLKDpaRE7K2yhMCf9yfh8VPFFLOKWgBCaUpKYwj3t7DLfSLplQjg4n2QccNTWozuLGR1PiNhtZYQuCY_9pG8Y7S7l5VmLuDQqXhf7-T2NZ2XsXI" width="300"/>


### ej-1B. A continuación, crea una nueva colección llamada Hints y usa el fichero .json para poblarla. Además, elimina el campo hints de las colecciones Rooms y User.
```
db.rooms.updateMany(
    {},  // Filtro vacío para pillar todos los documentos
    {
        $unset: { "hints": "" }  // Operación para eliminar el campo
    }
)

db.users.updateMany(
    {},
    {
        $unset: { "hints": "" }
    }
)
```

### ej-1C. Por último, actualiza las funciones de los endpoints: POST /comment, GET /dungeon/{dungeon_id} , GET /room/{room_id} y GET /user/{email}. ¿Como se ven afectados estos endpoints?
Ver el archivo ej-1c.py
<br>
<br>
<br>
## ej-2
### ej-2A. El número de cuentas de usuario que se crearon cada año agrupadas por país.
```
db.users.aggregate([
    {
        $group: {
            _id: { 
                year: { $substr: ["$creation_date", 0, 4] },
                country: "$country"
            },
            count: { $sum: 1 }
        }
    },
    {
        $group: {
            _id: "$_id.year",
            countries: {
                $push: {
                    country: "$_id.country",
                    count: "$count"
                }
            }
        }
    },
    {
        $project: {
            _id: 0,
            year: "$_id",
            countries: "$countries"
        }
    }
])
```
<img src="https://lh7-us.googleusercontent.com/UCtvWg4Iti_PnOGkxB4LRZJhzzOkD5jTqEZFnBHRFbE7eu_4HDMSIhylhOWW3Tff7gd6Zp7OYh92IksDxumWWhfqUP0W7HL5XzJt2sD-zW8C0CB1UMi_Fzc7MWKVtgspBgwoRWw9igbcHf4pZDmT9EM" alt="drawing" width="350"/>


### ej-2B. Los 20 países cuyos usuarios han realizado el mayor número de posts de tipo Lore en los últimos 5 años. Los países deben aparecen ordenados de mayor a menor número de posts.
```
db.Hints.aggregate([
    {
        $addFields: {
            year: { $substr: ["$Creation_date", 0, 4] }
        }
    },
    {
        $set: {
            year: { $toInt: "$year" }
        }
    },
    {
        $match: {
            Category: { $eq: "lore" },
            year: { $gte: 2018 }
        }
    },
    {
        $group: {
            _id: "$Publish_by.Country",
            count: { $sum: 1 }
        }
    },
    {
        $sort: { count: -1 }
    },
    { 
        $limit: 20 
    },
    {
        $project: {
            _id: 0,
            country: "$_id",
            lore_posts: "$count"
        }
    }
])
```
<img src="https://lh7-us.googleusercontent.com/pTp6Vtt0GHb8go0y-N9UBeChXBan0Jnn9bPPRIE7CiMmNah8RiQdPb0YB7h8jQM0VdvgRlyTZaBSmmQg_EADRYbCVFAlvM6cQbCDYYBkRjAPa_fXHB3W2yuOl3228YELt1JdBq6M6MhfI7hHw1sZFJY" alt="drawing" width="180"/>

### ej-2C. Los 5 usuarios que más bugs han reportado en 2022. Deben aparecer ordenados de mayor a menor.
```
db.Hints.aggregate([
    {
        $match: {
            Category: { $eq: "bug" },
            Creation_date: { $regex: "^2022" }
        }
    },
    {
        $group: {
            _id: "$Publish_by.User_name",
            count: { $sum: 1 }
        }
    },
    {
        $sort: { count: -1 }
    },
    {
        $limit: 5
    },
    {
        $project: {
            _id: 0,
            user_name: "$_id",
            bugs_reported: "$count"
        }
    }
])
```
<img src="https://lh7-us.googleusercontent.com/v9ikb-n46l4E_7KJKyrtBo3K70mNQEjBJ5FNEYV0MeULKCcYvLkqgCQqJoarpkdwqx0v3SfuQC-Ayk2MAbSfalPbODKx0YNIkXLeDCWRrk18FEfFQpT2QlKp8Ip9VUmF72i8MLFLKA8TTPjcXrA9NT0" alt="drawing" width="200"/>

Como hemos visto que los resultados más altos son personas con 2 mensajes, hemos comprobado cuantas personas en total, por separado, hay que han hecho comentarios de bugs en 2022 y luego cuantas personas nos ha salido del aggregate: que han sido 226 y 223 respectivamente y, efectivamente, cuando hacemos el aggregate solo hay 3 personas con más de 1 comentario sobre bugs.

### ej-2D. La mazmorra que más sugerencias ha recibido desglosada en países.
En este caso la solución se basa en hacer el maximo de cada uno de los paises por separado. En un script se incluiría este y se cambiaria en "Publish_by.Country": {$eq: "es_ES"} la etiqueta de país por la del que corresponda.
```
db.Hints.aggregate([
    {
        $match: {
            Category: { $eq: "suggestion" },
            "Publish_by.Country": { $eq: "es_ES" }
        }
    },
    {
        $group: {
            _id: "$References_room.Dungeon",
            count: { $sum: 1 }
        }
    },
    {
        $group: {
            _id: null,
            max_sugs: { $max: "$count" },
            max_sugs_dung: {
                $push: {
                    dungeon: "$_id",
                    count: "$count"
                }
            }
        }
    },
    { $unwind: "$max_sugs_dung" },
    {
        $project: {
            _id: 0,
            dungeon_name: "$max_sugs_dung.dungeon",
            is_max: { $eq: ["$max_sugs_dung.count", "$max_sugs"] }
        }
    },
    {
        $match: {
            is_max: { $eq: true }
        }
    }
])
```
<img src="https://lh7-us.googleusercontent.com/t0xeHnwSK8zsiqzKyc3Ds9o75AnaORVidpdqZaUqWrbliCPIeI6DuKEcQU41O2ApvwkcJrO-wrY7yUjYsGL4QLP6rcovR3Dp_WcCpD0MLq4yhExeS5-nrS3W73GDD-oeeae6ff4-R_3WkjUua5CZIIc" alt="drawing" width="500"/>