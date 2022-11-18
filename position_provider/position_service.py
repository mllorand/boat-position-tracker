import eventlet
import pandas
from time import sleep
import itertools
import json
import socketio
import sys

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
        sio.sleep(1)
        sio.emit('positions', json_object)

lines_data = [pandas.read_csv(f'./lines/line{i}.csv') for i in range(1, 4)]
lines = [iter_from_data_frame(line) for line in lines_data]

# longest = 0
# for line_data in lines_data:
#     longest = max(longest, len(line_data.index))

# for line_data in lines_data:
#     if longest <= len(line_data.index):
#         continue
#     for i in range(longest - len(line_data.index)):
#         line_data.append(line_data.iloc[-1])
    

# # a = json.dumps(lines_data)
# for data in lines_data:
#     print(data)
# sys.exit(0)


@sio.event
def connect(sid, environ):
    print(sid, 'express connected')
    sio.start_background_task(stream_positions, lines)


@sio.event
def disconnect(sid):
    print(sid, 'disconnected')


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
