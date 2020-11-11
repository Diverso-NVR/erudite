from fastapi import FastAPI
from db.models import db,Equipment


app = FastAPI()


@app.get('/equipment')
def list_equipment():
    equipmentss = []
    for equipment in db.equipments.find():
        equipmentss.append(Equipment(**equipment))
    return {'equipment': equipmentss}

#newcam = Camera(name = "camera2", login = "log2", password = "pass2", mac = "mac2")

#@app.post('/cameras')
#def create_camera(camera: Camera):
    #if hasattr(camera, 'id'):
        #delattr(camera, 'id')
    #ret = db.cameras.insert_one(camera.dict(by_alias=True))
    #camera.id = ret.inserted_id
    #return {'camera': camera}


#create_camera(newcam)