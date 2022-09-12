import datetime
from re import X
from tracemalloc import start
from matplotlib.pyplot import connect
import socketio
import logging
import json
import asyncio
import wave
import pyaudio
import os
import shutil
from socketIO_client import SocketIO, BaseNamespace

format = "%(asctime)s - %(process)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

sioAudio = socketio.AsyncClient()
sioConected = socketio.AsyncClient()
config = json.load(open('config.json'))
lista = []
x = None
frames = []
counter = 0
counter2 = 0
counter3 = 0
c = 0
'''parentDir = os.getcwd()
directory = "Audio"
path = os.path.join(parentDir, directory)
if os.path.exists(path):
    shutil.rmtree(path)
if not os.path.exists(path):
    os.makedirs(path)'''

@sioAudio.event(namespace= '/audio')
async def distribution(message):
    global counter
    lista.append(message[0]['active_voice'])
    if (counter == 1):
        await segmentator(lista, message)
    counter = counter + 1

async def segmentator(messageList, message):
    global frames, lista, counter, counter2, counter3, c, lista2, x
    if(messageList[0] == None and messageList[1] != None):
        if(x == None):
            frames.append(message[0]["data"].encode("ISO-8859-1"))
            x = messageList[1]
        if(x == messageList[1] and counter2 > 0):
            frames.append(message[0]["data"].encode("ISO-8859-1"))
        else:
            '''if not os.path.exists(directory + "/" + str(x)):
                os.makedirs(directory + "/" + str(x))
            os.chdir(directory + "/" + str(x))
            c = c+1
            print("AUDIO" + str(c) + " SE GUARDA EN " + str(x) + "")
            waveFile= wave.open("audio"+str(c)+".wav", 'wb')
            waveFile.setnchannels(message[0]['channels'])
            waveFile.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
            waveFile.setframerate(message[0]['rate'])
            waveFile.writeframes(b''.join(frames))
            waveFile.close()'''
            end_time = datetime.datetime.strptime(message[0]['time'], '%Y-%m-%d %H:%M:%S.%f')
            start_time = datetime.datetime.strptime(message[0]['time'], '%Y-%m-%d %H:%M:%S.%f') - datetime.timedelta(seconds=counter2/100)
            speaking_time = end_time - start_time
            ident = await identificator(frames, message, messageList, start_time, end_time, speaking_time)
            await sioConected.emit('report', ident, namespace="/conected")
            frames.clear()
            #os.chdir(parentDir)
            counter2 = 0
            x = messageList[1]
    
    if(messageList[0] == x):
        frames.append(message[0]["data"].encode("ISO-8859-1"))

    if(messageList[0] != x and messageList[0] != None):
        counter3 = counter3 + 1
        if(counter3 == 3):
            '''if not os.path.exists(directory + "/" + str(x)):
                os.makedirs(directory + "/" + str(x))
            os.chdir(directory + "/" + str(x))
            c = c+1
            print("AUDIO" + str(c) + " SE GUARDA EN " + str(x))
            waveFile= wave.open("audio"+str(c)+".wav", 'wb')
            waveFile.setnchannels(message[0]['channels'])
            waveFile.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
            waveFile.setframerate(message[0]['rate'])
            waveFile.writeframes(b''.join(frames))
            waveFile.close()'''
            end_time = datetime.datetime.strptime(message[0]['time'], '%Y-%m-%d %H:%M:%S.%f')
            start_time = datetime.datetime.strptime(message[0]['time'], '%Y-%m-%d %H:%M:%S.%f') - datetime.timedelta(seconds=counter2/100)
            speaking_time = end_time - start_time
            ident = await identificator(frames, message, messageList, start_time, end_time, speaking_time)
            await sioConected.emit('report', ident, namespace="/conected")
            frames.clear()
            #os.chdir(parentDir)
            counter2 = 0
            counter3 = 0
            x = messageList[0]

    if(messageList[0] != None and messageList[1] == None):
        counter2 = counter2 + 1

    if(messageList[0] == None and messageList[1] == None and counter2 >= 1):
        counter2 = counter2 + 1
        if(counter2 <= 25):
            frames.append(message[0]["data"].encode("ISO-8859-1"))
        else:
            '''if not os.path.exists(directory + "/" + str(x)):
                os.makedirs(directory + "/" + str(x))
            os.chdir(directory + "/" + str(x))
            c = c+1
            print("AUDIO" + str(c) + " SE GUARDA EN " + str(x))
            waveFile= wave.open("audio"+str(c)+".wav", 'wb')
            waveFile.setnchannels(message[0]['channels'])
            waveFile.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
            waveFile.setframerate(message[0]['rate'])
            waveFile.writeframes(b''.join(frames))
            waveFile.close()'''
            end_time = datetime.datetime.strptime(message[0]['time'], '%Y-%m-%d %H:%M:%S.%f')
            start_time = datetime.datetime.strptime(message[0]['time'], '%Y-%m-%d %H:%M:%S.%f') - datetime.timedelta(seconds=counter2/100)
            speaking_time = end_time - start_time
            ident = await identificator(frames, message, messageList, start_time, end_time, speaking_time)
            await sioConected.emit('report', ident, namespace="/conected")
            frames.clear()
            #os.chdir(parentDir)
            counter2 = 0

    counter = 0
    del lista[0]


async def identificator(frames, message, messageList, start_time, end_time, speaking_time):
    return({
        "name": message[0]['name'],
        "id_device": f"000000000000000"+message[0]['id_device'],
        "type": "AUDIO",
        "format": message[0]['format'],
        "rate":  message[0]['rate'],
        "channels":  message[0]["channels"],
        "chunk": message[0]["chunk"],
        "active_voice": messageList[1],
        "data": b''.join(frames),
        "start_time": str(start_time),
        "end_time": str(end_time),
        "speaking_time": str(speaking_time),
    })


@sioAudio.event()
async def disconnect():
    await sioAudio.disconnect()

async def main():
    await sioAudio.connect('http://localhost:80', namespaces=["/audio"])
    await sioConected.connect('http://localhost:84', namespaces=["/conected"])
    await sioAudio.wait()
    await sioConected.wait()

if __name__ == '__main__':
    logging.info(f'Running')
    asyncio.run(main())
    