import time
from threading import Thread
import numpy as np
from modbus_client import Modbus_client
# #from ctrl_devices import Device
import numpy as np
import logging
import json
import uvicorn
from fastapi import FastAPI, Response
from fastapi.logger import logger as fastapi_logger
import asyncio

class PPC():

    def __init__(self) -> None:
        self.N_gen = 6
        self.V_POI_ref = 1.0
        self.P_POI_ref = 1.5
        self.Q_POI_ref = 0.0
        self.ctrl_on = False
        self.ctrl_mode = 'PQ'

    def start_ctrl(self):
        self.control_loop_thread = Thread(target = self.control_loop)
        self.control_loop_thread.start()

    def start_api(self):
        app = FastAPI()     
       
        @app.post("/setpoints")
        async def set_setpoints(received: dict):
            self.change_setpoints(received)
            return Response(content= 'Exito', media_type='text/plain')


        @app.post("/start")
        async def start(received: dict):
            if self.ctrl_on == False:
                self.ctrl_on = True
                self.start_ctrl()
            return Response(content= 'Ok!', media_type='text/plain')

        @app.post("/stop")
        async def stop(received: dict):
            if self.ctrl_on == True:
                self.ctrl_on = False
            return Response(content= 'Ok!', media_type='text/plain')

        print('run uvicorn')
        uvicorn.run(app,host="0.0.0.0", port = 8010, log_level='critical')
        print('uvicorn ran')

    def change_setpoints(self, received):

        if 'P_POI_ref' in received:
            self.P_POI_ref = received['P_POI_ref']
        if 'Q_POI_ref' in received:
            self.Q_POI_ref = received['Q_POI_ref']

    def control_pq(self):

        mb_0001 = Modbus_client("10.0.0.3",port=502)
        mb_0101 = Modbus_client("10.0.1.1",port=502)
        mb_0102 = Modbus_client("10.0.1.2",port=502)
        mb_0103 = Modbus_client("10.0.1.3",port=502)
        mb_0201 = Modbus_client("10.0.2.1",port=502)
        mb_0202 = Modbus_client("10.0.2.2",port=502)
        mb_0203 = Modbus_client("10.0.2.3",port=502)

        mb_0001.start()
        mb_0101.start()
        mb_0102.start()
        mb_0103.start()
        mb_0201.start()
        mb_0202.start()
        mb_0203.start()
    
        t_0 = time.time()
        while self.ctrl_on:
            t = t_0 - time.time()    
            print(f't = {t:0.1f}, PPC running, P_POI_ref = {self.P_POI_ref:5.2f}, Q_POI_ref = {self.Q_POI_ref:5.2f}')
            time.sleep(0.5)

            P_POI_ref = self.P_POI_ref * 2e6
            Q_POI_ref = self.Q_POI_ref * 2e6

            for mb in [mb_0101, mb_0102, mb_0103,mb_0201, mb_0202, mb_0203]:
                # reactive powers
                value = int(Q_POI_ref/self.N_gen)
                reg_number = 40426
                mb.write(value, reg_number, 'int32',format = 'CDAB')

                # active powers
                value = int(P_POI_ref/self.N_gen)
                reg_number = 40424
                mb.write(value, reg_number, 'uint32',format = 'CDAB')



    def control_loop(self):      

        if self.ctrl_mode == 'PQ':
            self.control_pq()  



        # p_ref = 1e6
        # q_ref = 0.0e6


        # xi = 0.0
        # Dt = 0.1
        # t_0 = time.time()
        # for it in range(50):
        #     reg_number = 372
        #     value_echo = mb_0001.read(reg_number, 'int16', format = 'CDAB')
        #     V_POI = value_echo/100

        #     epsilon = (V_POI_ref - V_POI)
            
        #     q_ref_pu = 0*epsilon + 1*xi
        #     xi += Dt*epsilon
        #     q_ref = np.clip(q_ref_pu*2e6*N_gen,-0.5e6,0.5e6)*0

        #     for mb in [mb_0101, mb_0102]:



        #     print(f't = {time.time()-t_0:5.2f}, V_POI = {V_POI:5.3f}, q_ref = {q_ref/1e6:5.3f} Mvar')

        #     time.sleep(Dt)



if __name__ == "__main__":
    ppc = PPC()
    ppc.start_ctrl()
    ppc.start_api()





# mb_0001.close()
# mb_0101.close()
# mb_0102.close()


# POI = Device('POI')
# POI.ini_get_v()

# gens = [Device('LV0101'), Device('LV0102')]
# for gen in gens:
#     gen.ini_set_q()

# N_gens = len(gens)
# V_POI_ref = 1.01
# V_POI = POI.get_v()
# K_i = 100
# K_p = 1.0
# xi = 0.0

# t_0 = time.time()
# Dt = 0.1

# for it in range(100):

#     # voltage control
#     V_POI = POI.get_v()
#     epsilon = V_POI_ref - V_POI
#     xi += Dt*epsilon
#     q_ref = K_p*(epsilon) + K_i*xi

#     for gen in gens:
#         gen.set_q(q_ref/N_gens)

#     t = time.time() - t_0
#     print(f"t = {t:6.3f}, q_ref = {q_ref:4.3f}, V_POI = {V_POI:4.3f}")

#     time.sleep(Dt)
