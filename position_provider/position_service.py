import eventlet
import pandas
from time import sleep
import itertools
import json
import socketio

sio = socketio.Server(cors_allowed_origins="*", async_mode='eventlet')
app = socketio.WSGIApp(sio)


def iter_from_data_frame(line_data):
    return ({
        'lat': line_data['lat'][i],
        'lon': line_data['lon'][i],
        'heading': line_data['heading'][i]
    } for i in range(len(line_data))
    )


def stream_positions(lines):
    for position in itertools.zip_longest(*lines):
        json_object = json.dumps(
            {'line1': position[0],
             'line2': position[1],
             'line3': position[2]
             }
        )
        print(json_object)
        sio.emit('positions', json_object)
        sio.sleep(1)


lines_data = [pandas.read_csv(f'./lines/line{i}.csv') for i in range(1, 4)]
lines = [iter_from_data_frame(line) for line in lines_data]


@sio.event
def connect(sid, environ):
    print(sid, 'connected')


@sio.event
def disconnect(sid):
    print(sid, 'disconnected')


if __name__ == '__main__':
    sio.start_background_task(stream_positions(lines))
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
