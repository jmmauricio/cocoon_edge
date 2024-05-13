from pydae.bmapu import bmapu_builder
from pydae.build_v2 import build_mkl

import makeconfigs

P_Nom_MW = 1
M = 2
N = 3
F = 50
S_pv_mva = 1
V_kv = 132
S_bess_mva = 1
S_bess_storage_kWh = 250
data = {
    "system":{"name":f"pv_{M}_{N}","S_base":100e6,"K_p_agc":0.0,"K_i_agc":0.0,"K_xif":0.01},
    "buses":[
        {"name":"POI_MV","P_W":0.0,"Q_var":0.0,"U_kV":20.0},
        {"name": "PV", "P_W":0.0,"Q_var": 0.0, "U_kV":20.0},
        {"name":   "POI","P_W":0.0,"Q_var":0.0,"U_kV":V_kv},
        {"name":  "GRID","P_W":0.0,"Q_var":0.0,"U_kV":V_kv},
        {"name":"BESS","P_W":0.0,"Q_var":0.0,"U_kV":0.69},
    ],
    "lines":[
        {"bus_j":"POI","bus_k":"GRID","X_pu":0.1,"R_pu":0.0,"Bs_pu":0.0,"S_mva":S_pv_mva*N*M + 1.2*S_bess_mva, 'sym':True, 'monitor':True},
        {"bus_j":"BESS","bus_k": "POI_MV","X_pu":0.05,"R_pu":0.0,"Bs_pu":0.0,"S_mva":1.2*S_bess_mva, 'sym':True, 'monitor':True},
        {"bus_j":"PV","bus_k": "POI_MV","X_pu":0.05,"R_pu":0.0,"Bs_pu":0.0,"S_mva":S_pv_mva*N*M, 'sym':True, 'monitor':True},
        ],
    "transformers":[{"bus_j":"POI_MV","bus_k": "POI","X_pu":0.05,"R_pu":0.0,"Bs_pu":0.0,"S_mva":S_pv_mva*N*M}],
    "pvs":[],
    "sources":[{"type":"genape","bus":"GRID",
                "S_n":1000e6,"F_n":50.0,"X_v":0.001,"R_v":0.0,
                "K_delta":0.001,"K_alpha":1e-6}],
    "vscs":[{"type":"bess_pq","bus":"BESS","E_kWh":S_bess_storage_kWh,"S_n":S_bess_mva*1e6,
            "soc_ref":0.5,
            "socs":[0.0, 0.1, 0.2, 0.8,0.9,1.0],
            "es":[1, 1.08, 1.13, 1.17, 1.18,1.25]}
        ],
    }


for i_m in range(1,M+1):
    name_j = "PV"
    for i_n in range(1,N+1):
        name = f"{i_m}".zfill(2) + f"{i_n}".zfill(2)
        name_k = 'MV' + name

        data['buses'].append({"name":f"LV{name}","P_W":0.0,"Q_var":0.0,"U_kV":0.4})
        data['buses'].append({"name":f"MV{name}","P_W":0.0,"Q_var":0.0,"U_kV":20.0})

        data['lines'].append({"bus_j":f"LV{name}","bus_k":f"MV{name}","X_pu":0.05,"R_pu":0.01,"Bs_pu":0.0,"S_mva":1.2*S_pv_mva,"monitor":False})
        data['lines'].append({"bus_j":f"{name_k}","bus_k":f"{name_j}","X_pu":0.01,"R_pu":0.01,"Bs_pu":0.0,"S_mva":1.2*S_pv_mva*(N-i_n+1),"monitor":False})
        name_j = name_k
        data['pvs'].append({"bus":f"LV{name}","type":"pv_dq_d","S_n":S_pv_mva*1e6,"U_n":400.0,"F_n":50.0,"X_s":0.1,"R_s":0.0001,"monitor":False,
                            "I_sc":8,"V_oc":42.1,"I_mp":3.56,"V_mp":33.7,"K_vt":-0.160,"K_it":0.065,"N_pv_s":25,"N_pv_p":250})
    

#grid.dae['params_dict'].update({f'{str(T_lp1)}':0.1,f'{str(T_lp2)}':0.1})
#grid.dae['params_dict'].update({f'{str(PRamp)}':2.5,f'{str(QRamp)}':2.5})

grid = bmapu_builder.bmapu(data)

grid.uz_jacs = False
grid.verbose = True
grid.construct(f'pv_{M}_{N}')

build_mkl(grid.sys_dict, platform='Windows')


makeconfigs.simulator(M,N,S_pv_mva,S_bess_mva, V_kv, F,True)
makeconfigs.controller_settings(P_Nom_MW,M,N,S_pv_mva,S_bess_mva, V_kv, F,True)
