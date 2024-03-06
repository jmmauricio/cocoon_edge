#!/usr/bin/env python3
import json
import http.client
import numpy as np

class Gns3:

    def __init__(self) -> None:
        pass

        # gns3 api client
        self.api_ip = 'localhost'
        self.api_port = 3080
        self.api_headers = {'Content-type': 'application/json'}

        self.api_client = http.client.HTTPConnection(self.api_ip, self.api_port)
        self.nodes = []
        self.links = []

    def create_project(self, name):

        to_api_dict = {"name":name}
        to_api_json = json.dumps(to_api_dict)  # Convert dictionary to JSON format
        self.api_client.request('POST', '/v2/projects', to_api_json, self.api_headers)     # Send POST request
        response = self.api_client.getresponse() # Get response from server
        response_dict = json.loads(response.read().decode())
        self.project_id = response_dict['project_id']

    def set_current_project(self,project_id):

        self.project_id = project_id


        

    def add_vpcs_node(self, name, pos_x=0, pos_y=0):
        '''
        {"name": "VPCS 1", "node_type": "vpcs", "compute_id": "local"}        
        '''
    
        to_api_dict = {"name": name, "node_type": "vpcs", "compute_id": "local","x": pos_x, "y": pos_y}
        to_api_json = json.dumps(to_api_dict)  # Convert dictionary to JSON format
        self.api_client.request('POST', f'/v2/projects/{self.project_id}/nodes', to_api_json, self.api_headers)     # Send POST request
        response = self.api_client.getresponse() # Get response from server
        response_dict = json.loads(response.read().decode())

        self.nodes += [{"name":name, "node_id":response_dict['node_id']}]

    def add_switch_node(self, name, pos_x=0, pos_y=0):
        '''
        {"name": "VPCS 1", "node_type": "ethernet_switch", "compute_id": "local"}        
        '''
    
        to_api_dict = {"name": name, "node_type": "ethernet_switch", "compute_id": "local",
                       "x": pos_x, "y": pos_y}
        to_api_json = json.dumps(to_api_dict)  # Convert dictionary to JSON format
        self.api_client.request('POST', f'/v2/projects/{self.project_id}/nodes', to_api_json, self.api_headers)     # Send POST request
        response = self.api_client.getresponse() # Get response from server
        response_dict = json.loads(response.read().decode())

        self.nodes += [{"name":name, "node_id":response_dict['node_id']}]

    def add_template_node(self, name, template_name, pos_x=0, pos_y=0):
        '''
        {"name": "VPCS 1", "node_type": "CIG01", "compute_id": "local"}        
        '''

        self.get_templates()

        for item in self.templates:
            if item["name"] == template_name:
                template_id = item["template_id"]
        
    
        to_api_dict = {"name":name,"x": pos_x, "y": pos_y}
        to_api_json = json.dumps(to_api_dict)  # Convert dictionary to JSON format
        self.api_client.request('POST', f"/v2/projects/{self.project_id}/templates/{template_id}", to_api_json, self.api_headers)     # Send POST request
        response = self.api_client.getresponse() # Get response from server
        response_dict = json.loads(response.read().decode())

        self.nodes += [{"name":name, "node_id":response_dict['node_id']}]

    def add_link(self, name_j, adapter_number_j,port_number_j,name_k, adapter_number_k,port_number_k):
        '''

                '''

        for item in self.nodes:
            if item["name"] == name_j: node_j_id = item["node_id"]
        for item in self.nodes:
            if item["name"] == name_k: node_k_id = item["node_id"]

        to_api_dict = {"nodes": [{"adapter_number": adapter_number_j, "node_id": node_j_id, "port_number":port_number_j}, 
                                 {"adapter_number": adapter_number_k, "node_id": node_k_id, "port_number":port_number_k}]}
        
        to_api_json = json.dumps(to_api_dict)  # Convert dictionary to JSON format
        self.api_client.request('POST', f'/v2/projects/{self.project_id}/links', to_api_json, self.api_headers)     # Send POST request
        response = self.api_client.getresponse() # Get response from server
        response_dict = json.loads(response.read().decode())
        print(response_dict)

        self.links += [{"name_j":name_j, "name_k":name_k, "node_id":response_dict['link_id']}]

    def get_templates(self):

        self.api_client.request("GET", f'/v2/templates') # Send a GET request for the number
        response = self.api_client.getresponse() # Get the response from the server
        response_dict = json.loads(response.read().decode())
        
        self.templates = response_dict

    def add_drawing(self,svg, pos_x=0, pos_y=0):
        '''

        '''
    
        to_api_dict = {"x": pos_x, "y": pos_y, "svg":svg}
        to_api_json = json.dumps(to_api_dict)  # Convert dictionary to JSON format
        self.api_client.request('POST', f"/v2/projects/{self.project_id}/drawings", to_api_json, self.api_headers)     # Send POST request
        response = self.api_client.getresponse() # Get response from server
        response_dict = json.loads(response.read().decode())


if __name__ == "__main__":

    api = Gns3()
    api.create_project('Test74')
    api.get_templates()


    
    # api.add_vpcs_node('PC2')

    data = {
        "switches":[
            {"name":"SwPOI", "pos_x":0,"pos_y":0},
            {"name":"Sw0101","pos_x":-200,"pos_y":0},
            {"name":"Sw0102","pos_x":-350,"pos_y":0},
            {"name":"Sw0103","pos_x":-500,"pos_y":0},
            {"name":"Sw0104","pos_x":-650,"pos_y":0},
            {"name":"Sw0105","pos_x":-800,"pos_y":0}
        ],
        "end_nodes":[
            {"name":   "POI","modbus_ip":"10.0.0.2", "modbus_port":502, "type":"vm", "vm_name":"POI","pos_x": 110,"pos_y":-7},
            {"name":   "PPC","modbus_ip":"10.0.0.3", "modbus_port":502, "type":"vm", "vm_name":"ppc","pos_x": -50,"pos_y":-100},
            {"name":"LV0101","modbus_ip":"10.0.0.10","modbus_port":502, "type":"vm", "vm_name":"CIG01","adapter_number":1,"pos_x": -200,"pos_y":-150},
            {"name":"LV0102","modbus_ip":"10.0.0.11","modbus_port":502, "type":"vm", "vm_name":"CIG02","adapter_number":1,"pos_x": -350,"pos_y":-150},
            {"name":"LV0103","modbus_ip":"10.0.0.12","modbus_port":502, "type":"vm", "vm_name":"CIG03","adapter_number":1,"pos_x": -500,"pos_y":-150},
            {"name":"LV0104","modbus_ip":"10.0.0.13","modbus_port":502, "type":"vm", "vm_name":"CIG04","adapter_number":1,"pos_x": -650,"pos_y":-150},
            {"name":"LV0105","modbus_ip":"10.0.0.14","modbus_port":502, "type":"vm", "vm_name":"CIG05","adapter_number":1,"pos_x": -800,"pos_y":-150},
            {"name":"Probe", "ip":"10.0.0.4", "type":"vpcs","pos_x":0,"pos_y":200},
        ],
        "links":[
            {"node_j":"POI",   "adapter_number_j":1,"port_number_j":0,"node_k": "SwPOI","adapter_number_k":0,"port_number_k":0},
            {"node_j":"PPC",   "adapter_number_j":1,"port_number_j":0,"node_k": "SwPOI","adapter_number_k":0,"port_number_k":1},
            {"node_j":"LV0101","adapter_number_j":1,"port_number_j":0,"node_k":"Sw0101","adapter_number_k":0,"port_number_k":0},
            {"node_j":"LV0102","adapter_number_j":1,"port_number_j":0,"node_k":"Sw0102","adapter_number_k":0,"port_number_k":0},
            {"node_j":"LV0103","adapter_number_j":1,"port_number_j":0,"node_k":"Sw0103","adapter_number_k":0,"port_number_k":0},
            {"node_j":"LV0104","adapter_number_j":1,"port_number_j":0,"node_k":"Sw0104","adapter_number_k":0,"port_number_k":0},
            {"node_j":"LV0105","adapter_number_j":1,"port_number_j":0,"node_k":"Sw0105","adapter_number_k":0,"port_number_k":0},
            {"node_j":"SwPOI", "adapter_number_j":0,"port_number_j":2,"node_k":"Sw0101","adapter_number_k":0,"port_number_k":1},
            {"node_j":"Sw0101","adapter_number_j":0,"port_number_j":2,"node_k":"Sw0102","adapter_number_k":0,"port_number_k":1},
            {"node_j":"Sw0102","adapter_number_j":0,"port_number_j":2,"node_k":"Sw0103","adapter_number_k":0,"port_number_k":1},
            {"node_j":"Sw0103","adapter_number_j":0,"port_number_j":2,"node_k":"Sw0104","adapter_number_k":0,"port_number_k":1},
            {"node_j":"Sw0104","adapter_number_j":0,"port_number_j":2,"node_k":"Sw0105","adapter_number_k":0,"port_number_k":1},
            {"node_j":"Probe", "adapter_number_j":0,"port_number_j":0,"node_k": "SwPOI","adapter_number_k":0,"port_number_k":3}
        ],
        "vms":[
            {"name":"CIG01", "ssh_ip":"127.0.0.11", "ssh_port":2011},
            {"name":"CIG02", "ssh_ip":"127.0.0.12", "ssh_port":2012},
            {"name":"CIG03", "ssh_ip":"127.0.0.13", "ssh_port":2013},
            {"name":"CIG04", "ssh_ip":"127.0.0.14", "ssh_port":2014},
            {"name":"CIG05", "ssh_ip":"127.0.0.15", "ssh_port":2015}        
        ]
    }

    if "switches" in data:
        for item in data["switches"]:
            api.add_switch_node(item['name'], pos_x=item['pos_x'], pos_y=item["pos_y"])

    if "end_nodes" in data:
        for item in data["end_nodes"]:
            if item['type'] == 'vpcs':
                api.add_vpcs_node(item['name'], pos_x=item['pos_x'], pos_y=item["pos_y"])
            if item['type'] == 'vm':
                api.add_template_node(item['name'], item['vm_name'], pos_x=item['pos_x'], pos_y=item["pos_y"])
                modbus_ip = item['modbus_ip']
                svg = f'<svg width="69" height="24"><text>{modbus_ip}</text></svg>'
                api.add_drawing(svg, pos_x=item['pos_x']-40, pos_y=item["pos_y"]+80)

    if "links" in data:
        for item in data["links"]:
            node_j = item['node_j']
            adapter_number_j = item['adapter_number_j']
            port_number_j = item['port_number_j']
            node_k = item['node_k']
            adapter_number_k = item['adapter_number_k']
            port_number_k = item['port_number_k']

            api.add_link(node_j,adapter_number_j,port_number_j,node_k,adapter_number_k,port_number_k)


