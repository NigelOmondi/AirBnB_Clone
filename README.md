<p align="center">
  <img src="https://github.com/Imukua/AIRBNB_CLONE/blob/master/assets/Hogo.png" alt="Hbnb logo">
</p>

<h1 align="center">HBNB</h1>
<p align="center">An AirBnB clone.</p>


# AirBnB Clone - command interprator🏠

Welcome to the AirBnB Clone project, a simplified system for managing lodging listings!

## File Structure 🗂

```plaintext
├── console.py
├── models
│   ├── amenity.py
│   ├── base_model.py
│   ├── city.py
│   ├── place.py
│   ├── review.py
│   ├── state.py
│   └── user.py
└── file_storage.py
```

## Models / Classes 📁

### BaseModel

- `id` (string)
- `created_at` (datetime)
- `updated_at` (datetime)

Contains methods to initialize, save, convert to a dictionary, and format a string.

### User 👤

Extends BaseModel with:

- `email` (string)
- `password` (string)
- `first_name` (string)
- `last_name` (string)

### Place 🏡

Extends BaseModel with:

- `city_id` (string)
- `user_id` (string)
- `name` (string)
- `description` (string)
- `number_rooms` (int)
- `number_bathrooms` (int)
- `max_guest` (int)
- `price_by_night` (int)
- `latitude` (float)
- `longitude` (float)
- `amenity_ids` (list of strings)

### Review ⭐️

Extends BaseModel with:

- `place_id` (string)
- `user_id` (string)
- `text` (string)

### City 🏙

Extends BaseModel with:

- `state_id` (string)
- `name` (string)

### Amenity 🛀

Extends BaseModel with:

- `name` (string)

### State 🌎

Extends BaseModel with:

- `name` (string)

## Storage 💾

```plaintext
FileStorage
  |
  | serializes
  v
objects dict
  |
  | saved to
  v
file.json
  |
  | reloaded from
  v
objects dict
```

Uses JSON serialization to store data persistently.

## File Storage

Serializes and deserializes data to a file with methods to:

- Get all objects
- Create a new object
- Save to file
- Reload from file

## Usage ▶️

### Run Console

```plaintext
$ ./console.py
```

### Console Commands

```plaintext
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update
```

---
