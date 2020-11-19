from fastapi.testclient import TestClient
import os
import pytest

from db.models import Equipment, Room
from main import app

os.environ["TESTING"] = "True"

client = TestClient(app)


def test_rooms():
    response = client.get("/room")
    assert response.status_code == 200


def test_equipment():
    response = client.get("/equipment")
    assert response.status_code == 200


def test_equipment_in_room():
    room_id = 10
    response = client.get(f"/room_equipment/{room_id}")
    assert response.status_code == 200


def test_room():
    room_id = 13
    response = client.get(f"/room/{room_id}")
    assert response.status_code == 200


def test_one_equipment():
    equipment_id = 150
    response = client.get(f"/equipment/{equipment_id}")
    assert response.status_code == 200


def test_post_equipment():
    newequipment = Equipment(
        _id=150,
        ip="172.18.191.21",
        name="Презентация",
        room_id=1,
        audio="main",
        merge="backup2-left",
        port=80,
        rtsp="rtsp://172.18.191.21/0",
        tracking="backup",
        time_editing="2020-10-27 10:05:07.820582",
        external_id="16682899584",
    )
    response = client.post("/equipment", json=newequipment.dict(by_alias=True))
    assert response.status_code == 200


def test_post_room():
    newroom = Room(
        _id=1,
        name=504,
        drive="https://drive.google.com/drive/u/5/folders/1k-ZqejYgxd3t6BfIprGKCU4wV9LolT9e",
        calendar="c_f1hdjmh3q22jnccfrrola0fun0@group.calendar.google.com",
        tracking_state="f",
        main_source="172.18.191.24",
        screen_source="172.18.191.21",
        sound_source="172.18.191.21",
        tracking_source="172.18.191.23",
        auto_control="f",
        stream_url="",
        ruz_id=3360,
    )
    response = client.post("/room", json=newroom.dict(by_alias=True))
    assert response.status_code == 200


def test_delete_equipment():
    equipment_id = 151
    response = client.delete(f"/equipment/{equipment_id}")
    assert response.status_code == 200


def test_delete_room():
    room_id = 1
    response = client.delete(f"/room/{room_id}")
    assert response.status_code == 200


def test_update_equipment():
    equipment_id = 152
    response = client.put(f"/equipment/{equipment_id}", json={"name": 696})
    assert response.status_code == 200


def test_update_room():
    room_id = 1
    response = client.put(f"/room/{room_id}", json={"name": 696})
    assert response.status_code == 200
