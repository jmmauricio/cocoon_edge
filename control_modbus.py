import time
import numpy as np
from ctrl_devices import Device

POI = Device('POI')
POI.ini_get_v()

gens = [Device('LV0101'), Device('LV0102'), Device('LV0103'), Device('LV0104')]
for gen in gens:
    gen.ini_set_q()

N_gens = len(gens)
V_POI_ref = 1.01
V_POI = POI.get_v()
K_i = 100
K_p = 1.0
xi = 0.0

t_0 = time.time()
Dt = 0.1

for it in range(100):

    # voltage control
    V_POI = POI.get_v()
    epsilon = V_POI_ref - V_POI
    xi += Dt*epsilon
    q_ref = K_p*(epsilon) + K_i*xi

    for gen in gens:
        gen.set_q(q_ref/N_gens)

    t = time.time() - t_0
    print(f"t = {t:6.3f}, q_ref = {q_ref:4.3f}, V_POI = {V_POI:4.3f}")

    time.sleep(Dt)
