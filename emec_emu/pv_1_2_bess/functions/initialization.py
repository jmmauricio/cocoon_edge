import numpy as np
import json

def get_idx(emulator):
    emulator.p_s_ppc_u_idxs = [  emulator.model.inputs_run_list.index(f'p_s_ppc_{name}') for name in emulator.gen_names_list]
    emulator.q_s_ppc_u_idxs = [  emulator.model.inputs_run_list.index(f'q_s_ppc_{name}') for name in emulator.gen_names_list]
    emulator.p_s_y_idxs = [  emulator.model.y_run_list.index(f'p_s_{name}') for name in emulator.gen_names_list]
    emulator.q_s_y_idxs = [  emulator.model.y_run_list.index(f'q_s_{name}') for name in emulator.gen_names_list]
    emulator.array_p_s_y_idxs = np.array(emulator.p_s_y_idxs)+emulator.model.N_x
    emulator.array_q_s_y_idxs = np.array(emulator.q_s_y_idxs) + emulator.model.N_x
    emulator.V_y_idxs = [  emulator.model.y_run_list.index(f'V_{name}') for name in emulator.gen_names_list]
    emulator.irrad_idxs = [ emulator.model.inputs_run_list.index(f'irrad_{name}') for name in emulator.gen_names_list]
    emulator.array_irrad_idxs = np.array(emulator.irrad_idxs)
    emulator.array_V_y_idxs = np.array(emulator.V_y_idxs)+emulator.model.N_x
    emulator.lvrt_ext_y_idxs = [  emulator.model.inputs_run_list.index(f'lvrt_ext_{name}') for name in emulator.gen_names_list]
    emulator.v_lvrt_idxs = [  emulator.model.params_list.index(f'v_lvrt_{name}') for name in emulator.gen_names_list]
    emulator.t_lp1p_idxs = [emulator.model.params_list.index(f'T_lp1p_{name}') for name in emulator.gen_names_list]
    emulator.t_lp2p_idxs = [emulator.model.params_list.index(f'T_lp2p_{name}') for name in emulator.gen_names_list]
    emulator.t_lp1q_idxs = [emulator.model.params_list.index(f'T_lp1q_{name}') for name in emulator.gen_names_list]
    emulator.t_lp2q_idxs = [emulator.model.params_list.index(f'T_lp2q_{name}') for name in emulator.gen_names_list]
    emulator.pramp_up_idxs = [emulator.model.params_list.index(f'PRampUp_{name}') for name in emulator.gen_names_list]
    emulator.pramp_down_idxs = [emulator.model.params_list.index(f'PRampDown_{name}') for name in emulator.gen_names_list]
    emulator.qramp_up_idxs = [emulator.model.params_list.index(f'QRampUp_{name}') for name in emulator.gen_names_list]
    emulator.qramp_down_idxs = [emulator.model.params_list.index(f'QRampDown_{name}') for name in emulator.gen_names_list]
        
        
def get_names(emulator):
    emulator.p_s_names = [f"p_s_{name}" for name in emulator.gen_names_list]
    emulator.q_s_names = [f"q_s_{name}" for name in emulator.gen_names_list]
    emulator.v_names = [f"V_{name}" for name in emulator.gen_names_list]
    emulator.lvrt_names = [f"LVRT_{name}" for name in emulator.gen_names_list]
    emulator.hvrt_names = [f"HVRT_{name}" for name in emulator.gen_names_list]        
    emulator.irrad_names = [f"irrad_{name}" for name in emulator.gen_names_list] 
    emulator.t_lp1p_names = [f"T_lp1p_{name}" for name in emulator.gen_names_list]
    emulator.t_lp2p_names = [f"T_lp2p_{name}" for name in emulator.gen_names_list]
    emulator.t_lp1q_names = [f"T_lp1q_{name}" for name in emulator.gen_names_list]
    emulator.t_lp2q_names = [f"T_lp2q_{name}" for name in emulator.gen_names_list]
    emulator.pramp_up_names = [f"PRampUp_{name}" for name in emulator.gen_names_list]
    emulator.pramp_down_names = [f"PRampDown_{name}" for name in emulator.gen_names_list]
    emulator.qramp_up_names = [f"QRampUp_{name}" for name in emulator.gen_names_list]
    emulator.qramp_down_names = [f"QRampDown_{name}" for name in emulator.gen_names_list]
    
def get_keys_measures(emulator):
    emulator.keys = np.empty(0)
    emulator.keys = np.append(emulator.keys,'p_line_POI_GRID')
    emulator.keys = np.append(emulator.keys,'q_line_POI_GRID')
    if emulator.has_bess:
        emulator.keys = np.append(emulator.keys, 'p_line_PV_POI_MV')
        emulator.keys = np.append(emulator.keys, 'q_line_PV_POI_MV')
        emulator.keys = np.append(emulator.keys, 'soc_BESS')
        emulator.keys = np.append(emulator.keys, 'p_line_BESS_POI_MV')
        emulator.keys = np.append(emulator.keys, 'q_line_BESS_POI_MV')
    emulator.keys = np.append(emulator.keys, 'V_POI')
    emulator.keys = np.append(emulator.keys, 'omega_coi') #frecuency
    emulator.keys = np.append(emulator.keys, emulator.p_s_names)
    emulator.keys = np.append(emulator.keys, emulator.q_s_names)
    emulator.keys = np.append(emulator.keys, emulator.v_names)
    emulator.keys = np.append(emulator.keys, emulator.lvrt_names)
    #emulator.keys = np.append(emulator.keys, emulator.hvrt_names)
    
def check_configuration(filename):
    try:
        with open(filename, 'r') as archivo:
            config = json.load(archivo)
                        
        if any(key not in config["input"] for key in ["m_gen", "n_gen", "dt_mid", "dt", "pvs"]):
            raise ValueError("[ERROR] Error missing an essential key in input config.json")
        if any(key not in config["input"]["pvs"] for key in ["temp", "irrad", "p_ref_ppc", "inverter_response", "lvrt"]):
            raise ValueError("[ERROR] Error missing an essential key in pvs")
        return config
    except json.JSONDecodeError as e:
        raise ValueError(f"[ERROR] Error in config.json: {str(e)}") 
    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR] Not found file: {filename}")