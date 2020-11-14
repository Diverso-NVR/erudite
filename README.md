# Equipment Portal

## Использование этого модуля клиентом
Данный модуль включает в себя 11 рутов:

- https://.../equipment
вы отправляете на данный адрес GET запорс, вам возвращается информация обо всем оборудовании из базы данных

- https://.../room
вы отправляете на данный адрес GET запорс, вам возвращается информация обо всех комнатах из базы данных

- https://.../room_equipment/{room_id}
вы отправляете на данный адрес GET запорс, вам возвращается информация обо всем оборудовании из комнаты под id = room_id

- https://.../room/{room_id}
вы отправляете на данный адрес GET запорс, вам возвращается информация о комнате под id = room_id

- https://...//equipment/{equipment_id}
вы отправляете на данный адрес GET запорс, вам возвращается информация об оборудовании под id = equipment_id

    equipment_id: int
    
    room_id: int

### Пример кода для PUT запроса
```
file = open('/home/sergey/Desktop/xaa', 'rb')

a = file.read()

file.close() 

files = {'file_in': ('some_name', a, 'video/mp4')}

r = requests.put(URL,files=files)
```

<p>pip install -r requirements.txt - для скачивания всех нужных библиотек</p>