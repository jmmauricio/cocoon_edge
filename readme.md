
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


cocoon_edge.service:

[Unit]
Description=My Custom Service

[Service]
Type=simple
ExecStart= /usr/local/bin/cocoon_edge_script.sh

[Install]
WantedBy=multi-user.target

sudo mv cocoon_edge.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/cocoon_edge.service
sudo chmod +x /etc/systemd/system/cocoon_edge.service

sudo mv cocoon_edge_script.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/cocoon_edge_script.sh

Reload systemd:
sudo systemctl daemon-reload


Start the Service:
sudo systemctl start cocoon_edge

Enable the Service at Boot:
sudo systemctl enable cocoon_edge


sudo nano /usr/local/bin/cocoon_edge_script.sh

sudo nano /etc/systemd/system/cocoon_edge.service


#/bin/bash
cd /
python3 edge.py