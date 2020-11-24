# Equipment Portal

## Использование этого модуля клиентом
Доки UI: https://nvr.miem.hse.ru/api/erudite/docs

- https://nvr.miem.hse.ru/api/erudite/equipment
вы отправляете на данный адрес GET запорс, вам возвращается информация обо всем оборудовании из базы данных

- https://nvr.miem.hse.ru/api/erudite/rooms
вы отправляете на данный адрес GET запорс, вам возвращается информация обо всех комнатах из базы данных

- https://nvr.miem.hse.ru/api/erudite/rooms/{room_id}/equipment
вы отправляете на данный адрес GET запорс, вам возвращается информация обо всем оборудовании из комнаты под id = room_id

- https://nvr.miem.hse.ru/api/erudite/rooms/{room_id}
вы отправляете на данный адрес GET запорс, вам возвращается информация о комнате под id = room_id

- https://nvr.miem.hse.ru/api/erudite//equipment/{equipment_id}
вы отправляете на данный адрес GET запорс, вам возвращается информация об оборудовании под id = equipment_id

- https://nvr.miem.hse.ru/api/erudite/equipment
вы отправляете на данный адрес POST запорс, вставляя в тело запроса информацию об оборудовании в формате словаря, и данное оборудование добавляется в базу данных

- https://nvr.miem.hse.ru/api/erudite/rooms
вы отправляете на данный адрес POST запорс, вставляя в тело запроса информацию о комнате в формате словаря, и данная комната добавляется в базу данных

- https://nvr.miem.hse.ru/api/erudite/rooms/{room_id}
вы отправляете на данный адрес DELETE запорс, и комната под id = room_id удаляется из базы данных

- https://nvr.miem.hse.ru/api/erudite//equipment/{equipment_id}
вы отправляете на данный адрес DELETE запорс, и оборудование под id = equipment_id удаляется из базы данных

- https://nvr.miem.hse.ru/api/erudite/rooms/{room_id}
вы отправляете на данный адрес PUT запорс, вставляя в тело запроса информацию об полях в формате словаря, которые надо ихменить/добавить, и комната под id = room_id изменяется в базе данных

- https://nvr.miem.hse.ru/api/erudite//equipment/{equipment_id}
вы отправляете на данный адрес PUT запорс, вставляя в тело запроса информацию об полях в формате словаря, которые надо ихменить/добавить, и оборудование под id = equipment_id изменяется в базе данных

    equipment_id: int
    
    room_id: int

<p>pip install -r requirements.txt - для скачивания всех нужных библиотек</p>
