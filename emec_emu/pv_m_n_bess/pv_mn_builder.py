from pydae.bmapu import bmapu_builder
from pydae.build_v2 import builder
import makeconfigs

P_Nom_MW = 4.0
M = 1
N = 4
F = 50
S_pv_mva = 2.0
V_kv = 132

data = {
    "system":{"name":f"pv_{M}_{N}","S_base":100e6,"K_p_agc":0.0,"K_i_agc":0.0,"K_xif":0.01},
    "buses":[
        {"name":"POI_MV","P_W":0.0,"Q_var":0.0,"U_kV":20.0},
        {"name":   "POI","P_W":0.0,"Q_var":0.0,"U_kV":V_kv},
        {"name":  "GRID","P_W":0.0,"Q_var":0.0,"U_kV":V_kv}
    ],
    "lines":[
        {"bus_j":"POI_MV","bus_k": "POI","X_pu":0.05,"R_pu":0.0,"Bs_pu":0.0,"S_mva":S_pv_mva*N*M, 'sym':True, 'monitor':True},
        {"bus_j":   "POI","bus_k":"GRID","X_pu":0.02,"R_pu":0.0,"Bs_pu":0.0,"S_mva":S_pv_mva*N*M, 'sym':True, 'monitor':True}
        ],
    "pvs":[],
    "sources":[{"type":"genape","bus":"GRID",
                "S_n":1000e6,"F_n":F,"X_v":0.001,"R_v":0.0,
                "K_delta":0.001,"K_alpha":1e-6}]
    }

for i_m in range(1,M+1):
    name_j = "POI_MV"
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

b = builder(grid.sys_dict,verbose=True)
b.sparse = True
b.mkl = True
b.platform = 'linux'
b.dict2system()
b.functions()
b.jacobians()
b.cwrite()
b.template()
b.compile_mkl()

makeconfigs.simulator(M,N,S_pv_mva,0, V_kv, F,False)
makeconfigs.controller_settings(P_Nom_MW,M,N,S_pv_mva,0, V_kv, F,False)

 
#b.compilemkl()