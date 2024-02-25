import json 
import dict_modbus

def simulator( M,N,S_pv, S_bess, V_kV, F, bess: bool):
    list_names = ["poi"]
    config = {}
    port = 2000
    
    if bess:
        list_names.append("bess")
    for i in range (1, M*N+1):
        list_names.append(f"g{i}")
    
    for device_name in list_names:
        data = {}
        data["server"] = "modbus"
        data["port"] = f"{port}"

        if device_name == "poi":
            data["freq"] = F
            data["v"] = int(V_kV * 1e3)
            data["p_max"] = int(M * N * S_pv * 1e6)
            data["q_max"] = int((M * N * S_pv)/2 * 1e6)
            data["meas"] = dict_modbus.measures_poi()
        elif device_name == "bess":
            data["p_max"] = int(S_bess * 1e6)
            data["q_max"] = int(S_bess * 1e6)
            data["meas"] = dict_modbus.measures_bess()
            data["setpoints"] = dict_modbus.setpoints_bess()
        else:
            data["p_max"] = int(S_pv * 1e6)
            data["q_max"] = int(S_pv/2 * 1e6)
            data["meas"] = dict_modbus.measures_inverter(device_name)
            data["setpoints"] = dict_modbus.setpoints_inverter(device_name)
        
        port += 1
        config[device_name] = data
        
    with open("config_simulator.json", 'w') as archivo_json:
        # Escribir los datos en el archivo JSON
        json.dump(config, archivo_json, indent=4)
        
    
def controller_settings(P_Nom_MW,M,N,S_pv, S_bess, V_kV, F, bess: bool):
    controller_settings = {}
    api = {
        "scheme": "http",
        "host": "0.0.0.0",
        "port": 5000,
        "cert": "server.crt",
        "key": "server.key"
    }
    configuration = {}
    collector = {      
      "scheme": "http",
      "host": "collector",
      "port": 5050,
    }
    config = {}
    collector["config"] = config
    collector["config"]["adapters"] = dict_modbus.adapters()
    collector["config"]["devices"] = dict_modbus.devices(M,N,bess)
    plant = {
        "id":"PYDAE",
        "p": int(P_Nom_MW*1e6),
        "f": F,
        "v": int(V_kV * 1e3)
    }
    configuration["collector"] = collector
    configuration["plant"] = plant
    configuration["license"] = dict_modbus.license()
    configuration["initialization"] = dict_modbus.initialization()
    inverters = []
    for i in range(1, M*N+1):
        inverter = {}
        inverter["id"] = f"inv{i}"
        inverter["enabled"] = True
        inverter["sbase"] = int(S_pv * 1e6)
        inverter["pmax"] = int(S_pv * 1e6)
        inverter["qmax"] = int(S_pv / 2 * 1e6)
        inverter["qmin"] = int(-S_pv / 2 * 1e6)
        inverter["vbase"] = 630  ## no estoy seguro si es bueno hardcodearla
        inverters.append(inverter)
    
    controller_settings["api"] = api
    controller_settings["configuration"] = configuration
    controller_settings["inverters"] = inverters
        
    with open("config_controller.json", 'w') as archivo_json:
        # Escribir los datos en el archivo JSON
        json.dump(controller_settings, archivo_json, indent=4)
    print(collector)
        