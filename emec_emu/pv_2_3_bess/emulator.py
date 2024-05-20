import time
from threading import Thread
import importlib
import numpy as np
import logging
import json
import uvicorn
from fastapi import FastAPI, Response
from fastapi.logger import logger as fastapi_logger
from vrt_state import VRTStateMachine
import asyncio
from functions.initialization import *

class Emulator():

    def __init__(self) -> None:
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        try:
            self.config = check_configuration('config.json')
        except (ValueError, FileNotFoundError) as error:
            print(str(error))
            exit()
        
        self.M_gen = self.config["input"]["m_gen"]
        self.N_gen = self.config["input"]["n_gen"]
        name_module = f"pv_{self.M_gen}_{self.N_gen}"
        try: 
            module = importlib.import_module(name_module)
            self.model = module.model()
        except ModuleNotFoundError:
            print(f"Could not load model '{name_module}'")
        
        self.gen_names_list = ['LV' + f'{mm:02}{nn:02}' for mm in range(1, self.M_gen + 1) for nn in range(1, self.N_gen + 1)]

        get_idx(self)
        get_names(self)
        
        #Ramp variables
        self.p_setpoint_bess = 0
        self.q_setpoint_bess = 0
        self.ramp_setpoint_bess = 0
        self.q_setpoint_bess = 0
        self.ramp_setpoint_pvs = 13

        # Config.json 
        self.Dt_mid = self.config["input"]["dt_mid"]
        self.hvrt_alarm = 0
        self.states = []
        lvrt = self.config["input"]["pvs"]["lvrt"]
        self.VRT_invs = [VRTStateMachine(lv_in= lvrt["lv_in"], hv_in=lvrt["hv_in"], lv_out=lvrt["lv_out"], hv_out=lvrt["hv_out"], t_in=lvrt["t_in"], t_out=lvrt["lv_out"], name = name) for name in self.gen_names_list]
        self.has_bess = False
        if "bess" in self.config["input"]:
            self.has_bess = True
        get_keys_measures(self)
        
    def ini(self, initialization):
        self.model.Dt = 0.025
        self.model.ini(initialization,'xy_0.json')
        self.kirrad = self.model.get_value('irrad_LV0101') / self.model.get_value('p_s_LV0101')
        self.model.p[self.v_lvrt_idxs] = 0.0
        self.N_store = 5000
        self.N_z = self.model.z.shape[0]
        print(f'N_z = {self.N_z}')
        self.Z_store = np.zeros((self.N_store,self.N_z))
        self.T_store = np.zeros((self.N_store,))
        np.savez('outputs',outs=self.model.outputs_list)
        
 
    def start(self):
        self.step_loop_thread = Thread(target = self.step_loop)
        self.step_loop_thread.start()
        ### Initialize to max irrad.
        irradians = np.ones(len(self.return_irrad()))
        irra = dict(zip(self.irrad_names,irradians))
        self.change_irrad(irra)
        
        
    def measurement_error(self) -> float:
        random = np.random.normal(1,0.0005,1)
        if random > 1.005:
            random = 1.005
        elif random < 0.995:
            random = 0.995
        return random
        
    def return_measures(self):
        p_s = self.model.xy[self.array_p_s_y_idxs] 
        q_s = self.model.xy[self.array_q_s_y_idxs] 
        v = self.model.xy[self.array_V_y_idxs]
        lvrt = self.model.u_run[self.lvrt_ext_y_idxs]
        measures = np.empty(0)
        p_poi = self.model.get_value('p_line_POI_GRID') * self.measurement_error()
        q_poi = self.model.get_value('q_line_POI_GRID') * self.measurement_error()
        if self.has_bess:    
            p_pv = self.model.get_value('p_line_PV_POI_MV')
            q_pv = self.model.get_value('q_line_PV_POI_MV')
            soc_bess = self.model.get_value('soc_BESS')
            p_bess = self.model.get_value('p_line_BESS_POI_MV')
            q_bess = self.model.get_value('q_line_BESS_POI_MV')
        v_poi = self.model.get_value('V_POI')
        f_poi = self.model.get_value('omega_coi')
        measures = np.append(measures,p_poi)
        measures = np.append(measures,q_poi)
        if self.has_bess:
            measures = np.append(measures, p_pv)
            measures = np.append(measures, q_pv)
            measures = np.append(measures, soc_bess)
            measures = np.append(measures, p_bess)
            measures = np.append(measures, q_bess) 
        measures = np.append(measures, v_poi)
        measures = np.append(measures, f_poi)
        measures = np.append(measures, p_s)
        measures = np.append(measures, q_s)
        measures = np.append(measures, v)
        measures = np.append(measures, lvrt)
        #measures = np.append(measures, self.hvrt_alarm)
        return measures

    def return_irrad(self):
        values = self.model.u_run[self.irrad_idxs]
        irrad = np.empty(0)
        irrad = np.append(irrad, values/self.kirrad)
        return irrad

    def return_response_inverters(self):
        keys = (
            self.t_lp1p_names + 
            self.t_lp2p_names + 
            self.t_lp1q_names + 
            self.t_lp2q_names +
            self.pramp_up_names +
            self.pramp_down_names +
            self.qramp_up_names +
            self.qramp_down_names
        )
        measures = (
            self.model.u_run[self.t_lp1p_idxs] +
            self.model.u_run[self.t_lp2p_idxs] +
            self.model.u_run[self.t_lp1q_idxs] +
            self.model.u_run[self.t_lp2q_idxs] +
            self.model.u_run[self.pramp_up_idxs] +
            self.model.u_run[self.pramp_down_idxs] +
            self.model.u_run[self.qramp_up_idxs] +
            self.model.u_run[self.qramp_down_idxs]
        )        
        return dict(zip(keys,measures))


    def change_response_inverters(self, params):
        for key, value in params.items():
            match = False
            if 'T_lp1p' in key:
                match = True
                self.model.u_run[self.t_lp1p_idxs] = value
            if 'T_lp2p' in key:
                match = True
                self.model.u_run[self.t_lp2p_idxs] = value
            if 'T_lp1q' in key:
                match = True
                self.model.u_run[self.t_lp1q_idxs] = value
            if 'T_lp2q' in key:
                match = True
                self.model.u_run[self.t_lp2q_idxs] = value
            if 'PRampUp' in key:
                match = True
                self.model.u_run[self.pramp_up_idxs] = value
            if 'PRampDown' in key:
                match = True
                self.model.u_run[self.pramp_down_idxs] = value
            if 'QRampUp' in key:
                match = True
                self.model.u_run[self.qramp_up_idxs] = value
            if 'QRampDown' in key:
                match = True
                self.model.u_run[self.qramp_down_idxs] = value
            if match is False:
                print(f'Could not find key: {key}', key)
        return True

    def change_setpoints(self, received):
        if 'p_ref' not in locals():
            self.p_ref = self.model.u_run[self.p_s_ppc_u_idxs]
        if 'q_ref' not in locals():
            self.q_ref = self.model.u_run[self.q_s_ppc_u_idxs]
        mode = self.config["input"]["pvs"]["lvrt"]["mode"]
        #received = json.loads(received)
        for key,value in received.items():
            prefix = key[0]
            sufix_m = key[-4:-2]
            sufix_n = key[-2:]

            if (('p_s_ref_BESS' in key and not self.config["input"]["bess"]["ramp"]) or 'q_s_ref_BESS' in key) and self.has_bess:
                idx = self.model.inputs_run_list.index(key)
                self.model.u_run[idx] = value
            elif 'p_s_ref_BESS' in key:
                self.p_setpoint_bess = value
            elif 'q_s_ref_BESS' in key:
                self.q_setpoint_bess = value
            elif 'ramp_bess' in key:
                self.ramp_setpoint_bess = value
            elif 'p' in prefix:
                if len(self.states) != 0:
                    if (self.states[(int(sufix_m)-1)*self.N_gen+int(sufix_n)-1] != (3 or 2)) or (mode != 1):
                        self.p_ref[(int(sufix_m)-1)*self.N_gen+int(sufix_n)-1] = value  
            elif 'q' in prefix:
                if len(self.states) != 0:
                    if (self.states[(int(sufix_m)-1)*self.N_gen+int(sufix_n)-1] != (3 or 2)) or (mode != 1):
                        self.q_ref[(int(sufix_m)-1)*self.N_gen+int(sufix_n)-1] = value/2
            #if 'v_ref_GRID' in received:
            #    self.model.u_run[self.model.inputs_run_list.index('v_ref_GRID')] = received['v_ref_GRID']
        if not self.config["input"]["pvs"]["ramp_p"]:
            self.model.u_run[self.p_s_ppc_u_idxs] = self.p_ref
        self.model.u_run[self.q_s_ppc_u_idxs] = self.q_ref

        time.sleep(0.001)  

    def change_irrad(self, received):
        if 'irrad_ref' not in locals():
            self.irrad_ref = self.model.u_run[self.irrad_idxs]
        for key,value in received.items():
            sufix_m = key[-4:-2]
            sufix_n = key[-2:]
            self.irrad_ref[(int(sufix_m)-1)*self.N_gen+int(sufix_n)-1] = value * self.kirrad
           
        self.model.u_run[self.irrad_idxs] = self.irrad_ref
    
    
    def start_api(self):
        app = FastAPI()     
       
        @app.post("/response_inverters")
        async def post_response_inverters(params:dict):
            self.change_response_inverters(params)
            return Response(content='Exito', media_type='application/json')
        
        @app.get("/response_inverters")
        async def get_response_inverters():
            measures = self.return_response_inverters()
            return Response(content=json.dumps(measures), media_type="application/json")
        
        
        @app.get("/measures")
        async def get_measures():
            measures = self.return_measures()
            dicc = dict(zip(self.keys,measures))
            
            return Response(content=json.dumps(dicc), media_type='application/json')

        @app.post("/setpoints")
        async def set_setpoints(received: dict):
            self.change_setpoints(received)
            return Response(content= 'Exito', media_type='text/plain')

        @app.post("/irrad")
        async def post_irrad(received:dict):
            self.change_irrad(received)
            return Response(content='Exito', media_type= 'text/plain')   
        
        @app.get("/irrad")
        async def get_irrad():
            irradians = self.return_irrad()
            irra = dict(zip(self.irrad_names,irradians))
            return Response(content=json.dumps(irra), media_type='application/json')
            
        @app.get("/get_value")
        async def get_value(received: dict):
            response = self.model.get_value(received['name'])
            return response
        
        @app.post("/set_value")
        async def set_value(received:dict):
            self.model.set_value(received['name'],received['value'])
            return Response(content='Exito', media_type= 'text/plain')
        
        @app.get("/dimensions")
        async def get_dimensions():
            dimensions = {}
            dimensions['m'] = self.M_gen
            dimensions['n'] = self.N_gen
            return Response(content=json.dumps(dimensions), media_type='application/json')

        @app.post("/save_store")
        async def save_store(received: dict):
            print('Store saving')
            np.savez(received['file_name'],Time=self.T_store,Z=self.Z_store,i_store=self.i_store,N_store=self.N_store)
            return Response(content='Exito', media_type= 'text/plain')
             
        print('run uvicorn')
        uvicorn.run(app,host="0.0.0.0", port = 8000, log_level='critical')
        print('uvicorn ran')


    async def calculate_states(self, V_LV):
        tasks = []
        for machine_state, v in zip(self.VRT_invs, V_LV):
            tasks.append(machine_state.update_state(v))
        self.states = await asyncio.gather(*tasks)
        return
    
    def ramp_bess(self, t):
        next_step = self.ramp_setpoint_bess / (60/(t/1e9)) / self.config["input"]["bess"]["S_bess"] ## 50 ms se llama desde el bucle principal            
        idx = self.model.inputs_run_list.index('p_s_ref_BESS')
        measure_bess = self.model.u_run[idx]
        if measure_bess > self.p_setpoint_bess + next_step:
            self.model.u_run[idx] = measure_bess - next_step
        elif measure_bess < self.p_setpoint_bess - next_step:
            self.model.u_run[idx] = measure_bess + next_step
        else:
            self.model.u_run[idx] = self.p_setpoint_bess
        
        # q_s_ref_BESS
        idx = self.model.inputs_run_list.index('q_s_ref_BESS')
        self.model.u_run[idx] = self.q_setpoint_bess

        
    def ramp_p(self, t):        
        if not hasattr(self, "p_ref"):
            self.p_ref = self.model.u_run[self.p_s_ppc_u_idxs]
        if not hasattr(self, "q_ref"):
            self.q_ref = self.model.u_run[self.q_s_ppc_u_idxs]
        p_measure = self.model.xy[self.array_p_s_y_idxs] 
        next_setpoint = self.model.xy[self.array_p_s_y_idxs].copy()
        for i, p_setpoint in enumerate(self.p_ref):
            next_step = self.ramp_setpoint_pvs / (60/(t/1e9)) / self.config["input"]["pvs"]["p_max"] ## 50 ms se llama desde el bucle principal            
            if p_measure[i] > p_setpoint + next_step:
                next_setpoint[i] = p_measure[i] - next_step
            elif p_measure[i] < p_setpoint - next_step:
                next_setpoint[i] = p_measure[i] + next_step

        self.model.u_run[self.p_s_ppc_u_idxs] = next_setpoint[i]

    def step_loop(self):
        t = 0.0
        self.model.step(t+self.Dt_mid,{})
        self.i_store = 0
        t_0 = time.perf_counter_ns()
        t2 = t_0 ## time for ramps
        count = 0
        self.model.t = 0

        while True:

            if self.i_store < self.N_store-1:
                self.i_store += 1
            else:
                self.i_store = 0

            t = time.perf_counter_ns()-t_0
            prev = time.perf_counter_ns()
            self.model.step(t/1e9+self.Dt_mid,{})
            self.Z_store[self.i_store,:] = self.model.z
            self.T_store[self.i_store] = t

            V_LV = self.model.xy[np.array(self.V_y_idxs)+self.model.N_x]
            asyncio.run(self.calculate_states(V_LV))
            
            t3 = time.perf_counter_ns() -t2

            if self.has_bess and self.config["input"]["bess"]["ramp"]:
                self.ramp_bess(t3)
            if self.config["input"]["pvs"]["ramp_p"]:
                t4 += t3
                count += 1
                if count == 3:
                    self.ramp_p(t4)
                    t4 = 0
                    count = 0
                self.ramp_p(t3)
            t2 = time.perf_counter_ns()
            
            lvrt_ext = np.zeros(self.N_gen * self.M_gen)
            lvrt_ext[np.array(self.states) == 2] = 1.0 # LVRT
            lvrt_ext[np.array(self.states) == 3] = 1.0 # post LVRT

            self.model.u_run[self.lvrt_ext_y_idxs] = lvrt_ext
            #self.model.u_run[self.lvrt_ext_y_idxs] = lvrt_ext
            
            #hvrt_ext = np.zeros(self.N_gen* self.M_gen)
            #hvrt_ext[V_LV >1.1] = 1.0
            #self.hvrt_alarm = hvrt_ext
            
            if ((time.perf_counter_ns()-t_0-t) > self.Dt_mid*1e9):
                logging.warning("The simulation step took longer to execute than the given time.")
            time.sleep(max(0, (self.Dt_mid - (time.perf_counter_ns() - prev)/1e9)))
            # while (time.perf_counter_ns() - t_0) < (t + self.Dt_mid*1e9):
            #     pass
            

if __name__ == "__main__":
    emu = Emulator()
    
    pvs = emu.config["input"]["pvs"]
    inv_resp = pvs["inverter_response"]
    params_ini = {}
    for m in range(1,1+emu.M_gen):
        for n in range(1,1+emu.N_gen): 
            name = f'{m}'.zfill(2) + f'{n}'.zfill(2)
            #La planta tiene que arrancar deslimitada para el buen calculo de la irradiancia.
            params_ini.update({f'irrad_LV{name}': pvs["irrad"],f'p_s_ppc_LV{name}':pvs["p_ref_ppc"],f'temp_deg_LV{name}': pvs["temp"]})
            params_ini.update({f'T_lp1p_LV{name}': inv_resp["T_lp1p"], 
                               f'T_lp2p_LV{name}': inv_resp["T_lp2p"], 
                               f'T_lp1q_LV{name}': inv_resp["T_lp1q"], 
                               f'T_lp2q_LV{name}': inv_resp["T_lp2q"], 
                               f'i_sr_ref_LV{name}': pvs["lvrt"]["i_ref"],
                               f'PRampDown_LV{name}': inv_resp["PRampDown"],
                               f'PRampUp_LV{name}': inv_resp["PRampUp"],
                               f'QRampDown_LV{name}': inv_resp["QRampDown"],
                               f'QRampUp_LV{name}': inv_resp["QRampUp"]})
    print('run ini')

    emu.ini(params_ini)
    emu.start()
    print('run start_api')

    emu.start_api()
    
