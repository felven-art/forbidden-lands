from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
# from collections import defaultdict
import random
import json
import os

STICKERS_PATH = r'C:\Users\felven\Desktop\Programming\python\work in progress\forbidden_lands\static\stickers'


app = Flask(__name__)
socketio = SocketIO(app)



def save_data(a):
    print('Saving and clearing data.')
    # add received data to local dictionary
    dict_key = str(a['xy'])

    # print(hex_info)
    # send data to the rest of the clients
    if a['notes'] == 'undefined':
        a['notes'] = ''
    
    # clear every other location, so only one can exist at a time
    if 'partyLocation' in a['html']:
        for k in hex_info.keys():
            if 'partyLocation' in hex_info[k]['html']:
                hex_info[k]['html'] = str(hex_info[k]['html']).replace('partyLocation', '')

    hex_info[dict_key] = {}
    hex_info[dict_key]['html'] = a['html']
    hex_info[dict_key]['notes'] = a['notes']
    # dump this shit to json, so everyone currently joining can access what was already discovered
    print('Saving data to hex_db.json.')
    with open(r'C:\Users\felven\Desktop\Programming\python\work in progress\forbidden_lands\hex_db.json', 'w') as f:
        json.dump(hex_info, f)

# try reading existing data
try:
    with open(r'C:\Users\felven\Desktop\Programming\python\work in progress\forbidden_lands\hex_db.json', 'r') as f:
        hex_info = json.load(f)
except Exception:
    hex_info = {}

@app.route('/')
def index():
    return render_template('index.html')

# actions taken on connect - deploying already explored hexes
@socketio.on('connect')
def deploy_hexes():
    print('connect')
    # print(hex_info)
    emit('deploy_hexes', hex_info, broadcast=False)


# @socketio.on('hex_clicked')
# def hex_click(msg):
#     print('hex_clicked')
#     # print(msg)
#     # add received data to local dictionary
#     dict_key = str(msg['xy'])

#     # print(hex_info)
#     # send data to the rest of the clients
#     if msg['notes'] == 'undefined':
#         msg['notes'] = ''

#     emit('display_hex', {'who': '#container [hex-row=' + str(msg['xy'].split(',')[1]) + '][hex-column='+ str(msg['xy'].split(',')[0]) +']',
#                          'html':msg['html'], 'notes': msg['notes']}, broadcast=True, include_self=False)
    
#     # clear every other location, so only one can exist at a time
#     if 'partyLocation' in msg['html']:
#         for k in hex_info.keys():
#             if 'partyLocation' in hex_info[k]['html']:
#                 hex_info[k]['html'] = str(hex_info[k]['html']).replace('partyLocation', '')

#     hex_info[dict_key] = {}
#     hex_info[dict_key]['html'] = msg['html']
#     hex_info[dict_key]['notes'] = msg['notes']
#     # dump this shit to json, so everyone currently joining can access what was already discovered
#     print('Saving data to hex_db.json.')
#     with open(r'C:\Users\felven\Desktop\Programming\python\work in progress\forbidden_lands\hex_db.json', 'w') as f:
#         json.dump(hex_info, f)



# NEW WAY OF HANDLING EVENTS - multiples instead of single one 
@socketio.on('hex_click')
def hex_click(msg):
    print('hex_click')
    save_data(msg)
    emit('display_hex_click', {'who': '#container [hex-row=' + str(msg['xy'].split(',')[1]) + '][hex-column='+ str(msg['xy'].split(',')[0]) +']', 'html':msg['html'], 'notes': msg['notes']}, broadcast=True, include_self=False)

@socketio.on('hex_party_location')
def hex_click(msg):
    print('hex_party_location')
    save_data(msg)
    emit('display_hex_party_location', {'who': '#container [hex-row=' + str(msg['xy'].split(',')[1]) + '][hex-column='+ str(msg['xy'].split(',')[0]) +']', 'html':msg['html'], 'notes': msg['notes']}, broadcast=True, include_self=False)

@socketio.on('hex_add_note')
def hex_click(msg):
    print('hex_add_note')
    save_data(msg)
    emit('display_hex_add_note', {'who': '#container [hex-row=' + str(msg['xy'].split(',')[1]) + '][hex-column='+ str(msg['xy'].split(',')[0]) +']', 'html':msg['html'], 'notes': msg['notes']}, broadcast=True, include_self=False)

@socketio.on('hex_remove_note')
def hex_click(msg):
    print('hex_remove_note')
    save_data(msg)
    emit('display_hex_remove_note', {'who': '#container [hex-row=' + str(msg['xy'].split(',')[1]) + '][hex-column='+ str(msg['xy'].split(',')[0]) +']', 'html':msg['html'], 'notes': msg['notes']}, broadcast=True, include_self=False)


# graceful shutdown
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

# shutdown using request, just go to http://127.0.0.1:5000/shutdown
@app.route('/shutdown', methods=['GET'])
def shutdown():
    print('Shutting down server.')
    with open(r'C:\Users\felven\Desktop\Programming\python\work in progress\forbidden_lands\hex_db.json', 'w') as f:
        json.dump(hex_info, f)
    shutdown_server()
    return 'Server shutting down...'

# force refresh on all clients
@app.route('/refresh-all', methods=['GET'])
def refresh():
    socketio.emit('refresh', {}, broadcast=False)
    return 'Refreshing...'

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')