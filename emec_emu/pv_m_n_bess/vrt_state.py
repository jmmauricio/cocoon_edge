import asyncio
import time

class VRTStateMachine:
    def __init__(self, lv_in, hv_in, lv_out, hv_out, t_in, t_out, name):
        self.VRTState = 0
        self.LastVRT = None
        self.lv_in = lv_in
        self.lv_out = lv_out
        self.hv_in = hv_in
        self.hv_out = hv_out
        self.t_in = t_in
        self.t_out = t_out
        self.name = name
        
    async def update_state(self, v):
        if self.VRTState == 0:  # Reposo
            if v < self.lv_in:
                self.LastVRT = time.time()
                self.VRTState = 1
            if v > self.hv_in:
                self.LastVRT = time.time()
                self.VRTState = 4

        elif self.VRTState == 1:  # Pre LVRT
            if v > self.lv_out:
                self.VRTState = 0
            elif time.time() - self.LastVRT > self.t_in:
                self.VRTState = 2

        elif self.VRTState == 2:  # LVRT
            if v > self.lv_out:
                self.VRTState = 3
                self.LastVRT = time.time()

        elif self.VRTState == 3:  # Post LVRT
            if v < self.lv_out:
                self.VRTState = 2
            elif time.time() - self.LastVRT > self.t_out:
                self.VRTState = 0

        elif self.VRTState == 4:  # Pre HVRT
            if v < self.hv_out:
                self.VRTState = 0
            elif time.time() - self.LastVRT > self.t_in:
                self.VRTState = 5

        elif self.VRTState == 5:  # HVRT
            if v < self.hv_out:
                self.VRTState = 6
                self.LastVRT = time.time()

        elif self.VRTState == 6:  # Post HVRT
            if v > self.hv_out:
                self.VRTState = 5
            elif time.time() - self.LastVRT > self.t_out:
                self.VRTState = 0
        return self.VRTState

