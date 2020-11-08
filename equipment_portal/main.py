from fastapi import FastAPI
from db.models import db,Camera


app = FastAPI()


@app.get('/cameras')
def list_cameras():
    cameras = []
    for camera in db.cameras.find():
        cameras.append(Camera(**camera))
    return {'cameras': cameras}


@app.post('/cameras')
def create_camera(camera: Camera):
    if hasattr(camera, 'id'):
        delattr(camera, 'id')
    ret = db.cameras.insert_one(camera.dict(by_alias=True))
    camera.id = ret.inserted_id
    return {'camera': camera}