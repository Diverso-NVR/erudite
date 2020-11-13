from fastapi import FastAPI
from pymongo import MongoClient
from db.models import Equipment,Room


DATABASE_URI = "mongodb://host1.miem.vmnet.top:20005"

#Для подключения к внешней БД:
client = MongoClient(DATABASE_URI)

#Доступ к БД через pymongo
db = client['Equipment']


app = FastAPI()

@app.get('/equipment')
async def list_equipments():
    equipmentss = []
    for equipment in db.equipment.find():
        equipmentss.append(Equipment(**equipment))
    return {'equipment': equipmentss}

@app.get('/room')
async def list_rooms():
    rooms_list = [] 
    for room in db.rooms.find():
        rooms_list.append(room)
    print(rooms_list)
    return (rooms_list)

@app.get('/room/{room_id}')
async def list_room_equipments(room_id):
    equipments_list = []
    for equipment in db.equipment.find({ 'room_id': int(room_id) }):
        equipments_list.append(Equipment(**equipment))
    print(equipments_list)
    return (equipments_list)

@app.post('/equipment')
async def create_equipment(equipment: Equipment):
    if hasattr(equipment, 'id_'):
        delattr(equipment, 'id_')
    ret = db.equipment.insert_one(equipment.dict(by_alias=True))
    equipment.id_ = ret.inserted_id
    print("This equipment already exists in the equipments collection")
    return {'equipment': equipment}

"""
Проверка функции create_equipment:
    newequipment = Equipment(id = 150, ip = "172.18.191.21", name = "Презентация", room_id = 1, audio = "main", merge = 'backup2-left', port = 80, rtsp = "rtsp://172.18.191.21/0", tracking = "backup", time_editing = "2020-10-27 10:05:07.820582", external_id = "16682899584")
    create_equipment(newequipment)
"""

@app.post('/room')
async def create_room(room: dict):
    try:
        ret = db.rooms.insert_one(room)
    except:
        print("This room already exists in the rooms collection")
    return {'room': room}

"""
Проверка функции create_room:
    newroom = Room(_id = 1, name = 504, drive = "https://drive.google.com/drive/u/5/folders/1k-ZqejYgxd3t6BfIprGKCU4wV9LolT9e", calendar = "c_f1hdjmh3q22jnccfrrola0fun0@group.calendar.google.com", tracking_state = 'f', main_source = '172.18.191.24', screen_source = "172.18.191.21", sound_source = "172.18.191.21", tracking_source = "172.18.191.23", auto_control = "f", stream_url = '', ruz_id = 3360)
    newroom_dict = newroom.dict()
    newroom_dict.update(_id=1)
    print(newroom_dict)
    create_room(newroom_dict)
"""

@app.delete('/room/{room_id}')
async def delete_room(room_id:int):
    db.rooms.remove( {'_id': room_id})

"""
Проверка функции delete_room:
    delete_room(1)
"""

@app.delete('/equipment/{equipment_id}')
async def delete_equipment(equipment_id:int):
    db.equipment.remove( {'id': equipment_id})

"""
Проверка функции delete_equipment:
    delete_equipment(150)
"""

@app.put('/room/{room_id}')
async def update_room(room_id:int,new_values_dict:dict):
    db.rooms.update_one( {'_id': room_id},{'$set': new_values_dict  } )

"""
Проверка функции update_room:
    new_name = { "name": 696 }
    update_room(1,new_name)
"""

@app.put('/equipment/{equipment_id}')
async def update_equipment(equipment_id:int,new_values_dict:dict):
    db.equipment.update_one( {'id': equipment_id},{'$set': new_values_dict  } )

"""
Проверка функции update_equipment:
    new_name = { "name": 696 }
    update_equipment(150,new_name)
"""