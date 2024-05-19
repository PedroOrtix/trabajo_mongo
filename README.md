# Memoria de la Parte 1: Implementación de Funciones en Python con PyMongo

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