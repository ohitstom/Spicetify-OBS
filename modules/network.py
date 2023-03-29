import asyncio
import websockets
import subprocess
import psutil
import json
import os

class startServer():
    def __init__(self):
        print("Thread Started")
        self.port = asyncio.run(self.portFinder())
        asyncio.run(self.initialize())  
  
    def process_pid_running(self, pid):
        try:
            return psutil.pid_exists(pid)
        except Exception:
            return False
          
    async def portFinder(self):
        proc = await asyncio.create_subprocess_exec(
            "powershell",
            "spicetify -e path webnowplaying.js",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW
        ) 
        while self.process_pid_running(proc.pid):
            line = str(await proc.stdout.readline(), encoding="utf-8")
            if line.strip() != "":
                output = line.strip()
        with open(output, 'r') as f:
            for line in f:
                if 'new WebSocket' in line:
                    string = line.strip()
                    port = ''.join(filter(str.isdigit, string))
                    print(f"port: {port} found!")
                    return port

    def jsonExporter(self, raw):
        jsonObject = [x for x in raw.splitlines()]
        jsonObject = dict(map(lambda s : s.split(':',1), jsonObject))
        user = os.path.expanduser("~")
        dir = f"{user}\\.SpicetifyOBS.output"
        if not os.path.isdir(dir):
            os.mkdir(dir)
        for key, value in jsonObject.items():
            print(f"{key}: {value}")
            with open(f"{dir}\\{key}.txt", "w") as f:
                f.write(str(value))
            
    async def handler(self, websocket, path):
        if await websocket.recv():
            print("Spotify is connected")
            try:
                async for message in websocket:
                    self.jsonExporter(message)
            except websockets.exceptions.ConnectionClosedError:
                print("Spotify disconnected, attempting to reconnect.")
                return
            
    async def initialize(self):
        print("Server Ready, waiting for client.")
        async with websockets.serve(self.handler, "localhost", self.port):
            await asyncio.Future()