import json
import uvicorn
from fastapi import FastAPI, Response
from fastapi.logger import logger as fastapi_logger
import asyncio

class EdgeApi():

    def __init__(self) -> None:
        pass

    def start_api(self):
        app = FastAPI()     
       
        # @app.post("/config_gen")
        # async def post_response_inverters(params:dict):
        #     self.change_response_inverters(params)
        #     return Response(content='Exito', media_type='application/json')
        

        @app.get("/config_edge")
        async def get_config_edge(received: dict):
            
            print(received)

            # read configuration file 
            with open('config_devices.json','r') as fobj:
                config_devices = json.loads(fobj.read())


            name = received['name']
            # find current device in configuration
            for item in config_devices['devices']:
                if item['id'] ==  name:
                    edge_config = item
            
            edge_config.update({"emu_api_ip":config_devices['api']['host'],"emu_api_port":config_devices['api']['port'],})
            print(edge_config)

            return Response(content=json.dumps(edge_config), media_type="application/json")

        
        uvicorn.run(app,host="0.0.0.0", port = 8001, log_level='critical')

if __name__ == "__main__":
    api = EdgeApi()
    api.start_api()        