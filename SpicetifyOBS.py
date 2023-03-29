import obspython as obs
import threading
from modules import network, interface

def script_description():
  return """
  SpicetifyOBS:
      Reads websocket data from the webnowplaying extension.
      This data includes but is not limited to: 
      Title, 
      album, 
      and art.
      This data is then formatted into a graphical source.
  """   

def load():
    interface.initialize()
    thread = threading.Thread(target=network.startServer)
    thread.daemon = True
    thread.start()    

def on_event(event):
    if event == obs.OBS_FRONTEND_EVENT_FINISHED_LOADING:
        print("OBS Ready")
        load()
        
        
def script_load(settings):
    obs.obs_frontend_add_event_callback(on_event)
    