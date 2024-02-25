
* run `\emec_emu\pv_m_n> python emulator.py` at the host PC
* open in GNS3 the file `\com_emu\com_emu.gns3` 
* start all PCs at GNS3
* run the following scripts in the workspace/cocoon_edge folder
    - **poi**: `sudo python3 edge.py POI`
    - **lv0101**: `sudo python3 edge.py LV0101 -autoip enp0s8 -apiip 172.25.192.1`
    - **lv0102**: `sudo python3 edge.py LV0102 -autoip enp0s8 -apiip 172.25.192.1`
    - **lv0103**: `sudo python3 edge.py LV0103 -autoip enp0s8 -apiip 172.25.192.1`
    - **lv0104**: `sudo python3 edge.py LV0104 -autoip enp0s8 -apiip 172.25.192.1`
    - **ppc**: `sudo python3 control_modbus.py`

After working stop each machine with: `sudo poweroff`
