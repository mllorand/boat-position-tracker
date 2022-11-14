import eventlet
import pandas
from time import sleep
import itertools
import json
import socketio

sio = socketio.Server(cors_allowed_origins="*", async_mode='eventlet')
app = socketio.WSGIApp(sio)    

def ping_in_intervals():
    while True:
        sio.sleep(1)
        sio.emit('message')

@sio.event
def connect(sid, environ):
    print(sid, 'connected')


@sio.event
def disconnect(sid):
    print(sid, 'disconnected')


def iter_from_data_frame(line_data):
    return ({
        'lat': line_data['lat'][i],
        'lon': line_data['lon'][i],
        'heading': line_data['heading'][i]
    } for i in range(len(line_data))
    )


# line1_data = pandas.read_csv("./lines/line1.csv")
# line2_data = pandas.read_csv("./lines/line2.csv")
# line3_data = pandas.read_csv("./lines/line3.csv")

# line1 = iter_from_data_frame(line1_data)
# line2 = iter_from_data_frame(line2_data)
# line3 = iter_from_data_frame(line3_data)

# for position in itertools.zip_longest(line1, line2, line3):
#     json_object = json.dumps(
#         {'line1': position[0],
#         'line2': position[1],
#         'line3': position[2]
#         }
#     )
#     print(json_object)
#     sleep(1)


thread = sio.start_background_task(ping_in_intervals)
eventlet.wsgi.server(eventlet.listen(('', 8000)), app)

