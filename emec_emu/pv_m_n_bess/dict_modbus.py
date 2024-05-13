def measures_poi():
  measures = [
                {
                  "variable": "poi.p",
                  "address": "4x370",
                  "type": "int32",
                  "format": "CDAB",
                  "scale": 1
                },
                {
                  "variable": "poi.q",
                  "address": "4x374",
                  "type": "int32",
                  "format": "CDAB",
                  "scale": 1
                },
                {
                  "variable": "poi.v",
                  "address": "4x372",
                  "type": "uint16",
                  "format": "AB",
                  "scale": 100
                },
                {
                  "variable": "poi.f",
                  "address": "4x900",
                  "type": "uint16",
                  "format": "AB",
                  "scale": 1
                }
              ]
  return measures
  
def measures_bess():
  measures = [
                {
                  "variable": "bess.p",
                  "address": "4x12",
                  "type": "int32",
                  "format": "CDAB",
                  "scale": 1
                },
                {
                  "variable": "bess.q",
                  "address": "4x14",
                  "type": "int32",
                  "format": "CDAB",
                  "scale": 1
                },
                {
                  "variable": "bess.soc",
                  "address": "4x6",
                  "type": "int32",
                  "format": "CDAB",
                  "scale": 0.000001
                }
              ]
  return measures

def setpoints_bess():
    setpoints =  [
      {
        "variable": "bess.p",
        "address": "4x2",
        "type": "int32",
        "format": "CDAB",
        "scale": 1
      },
      {
        "variable": "bess.q",
        "address": "4x4",
        "type": "int32",
        "format": "CDAB",
        "scale": 1
      }
    ]
    return setpoints
  
def measures_inverter(device_name):
  measures = [
    {
      "variable": f"{device_name}.p",
      "address": "4x40525",
      "type": "int32",
      "format": "CDAB",
      "scale": 1
    },
    {
      "variable": f"{device_name}.q",
      "address": "4x40544",
      "type": "int32",
      "format": "CDAB",
      "scale": 1
    },
    {
      "variable": f"{device_name}.v",
      "address": "4x40546",
      "type": "int32",
      "format": "CDAB",
      "scale": 0.001
    },
    {
      "variable": f"{device_name}.lvrt",
      "address": "4x40548",
      "type": "int32",
      "format": "CDAB",
      "scale": 1
    },
    {
      "variable": f"{device_name}.hvrt",
      "address": "4x40550",
      "type": "int32",
      "format": "CDAB",
      "scale": 1
    }
  ]
  
  return measures
  
  
def setpoints_inverter(device_name):
  setpoints = [
      {
        "variable": f"{device_name}.p",
        "address": "4x40424",
        "type": "uint32",
        "format": "CDAB",
        "scale": 1
      },
      {
        "variable": f"{device_name}.q",
        "address": "4x40426",
        "type": "int32",
        "format": "CDAB",
        "scale": 1
      }
    ]
  return setpoints

def adapters():
  adapters = []
  poi =  {
      "id": "poi",
      "type": "modbus-gen",
      "interval": 200,
      "config": {
          "ActivePower": {
              "address": 370,
              "reg_type": "holding",
              "slaveID": 1,
              "type": "int32",
              "size": 4,
              "format": "CDAB",
              "scale": 1,
              "read_individual": False
          },
          "ReactivePower": {
              "address": 374,
              "reg_type": "holding",
              "slaveID": 1,
              "type": "int32",
              "size": 4,
              "format": "CDAB",
              "scale": 1,
              "read_individual": False
          },
          "VoltageAVG": {
              "address": 372,
              "reg_type": "holding",
              "slaveID": 1,
              "type": "int16",
              "size": 2,
              "format": "AB",
              "scale": 100,
              "read_individual": False
          },
          "Frequency": {
              "address": 900,
              "reg_type": "holding",
              "slaveID": 1,
              "type": "uint16",
              "size": 2,
              "format": "AB",
              "scale": 1,
              "read_individual": False
          }
      }
  }
  
  inv =  {
      "id": "inv",
      "type": "modbus-gen",
      "interval": 200,
      "config": {
          "ActivePower": {
              "address": 40525,
              "reg_type": "holding",
              "slaveID": 1,
              "type": "int32",
              "size": 4,
              "format": "CDAB",
              "scale": 1
          },
          "ReactivePower": {
              "address": 40544,
              "reg_type": "holding",
              "slaveID": 1,
              "type": "int32",
              "size": 4,
              "format": "CDAB",
              "scale": 1
          },
          "VoltageAVG": {
              "address": 40546,
              "reg_type": "holding",
              "slaveID": 1,
              "type": "int32",
              "size": 4,
              "format": "CDAB",
              "scale": 0.001
          },
          "SetActivePower": {
              "address": 40424,
              "reg_type": "holding",
              "slaveID": 1,
              "type": "uint32",
              "size": 4,
              "format": "CDAB",
              "scale": 1
          },
          "SetReactivePower": {
              "address": 40426,
              "reg_type": "holding",
              "slaveID": 1,
              "type": "int32",
              "size": 4,
              "format": "CDAB",
              "scale": 1
          }
      }
  }
  adapters.append(poi)
  adapters.append(inv)
  
  return adapters
  

def devices(M,N, bess: bool):
  devices = [
    {
        "id": "poi",
        "adapterID": "poi",
        "info": {
            "host": "simulator",
            "port": 2000
        }
    }
  ]
  j = 1 
  r = 1
  if bess:
    r = 2
  for i in range (1, M*N+r):
    if bess and i == 1:
      #bess = {}
      #bess["id"] = "bess"
      #bess["adapterID"] = "bess"
      #info = {}
      #info["host"] = "simulator"
      #info["port"] = 2000 + i
      #bess["info"] = info
      #devices.append(bess)
      continue
    inv = {}
    inv["id"] = f"inv{j}"
    inv["adapterID"] = "inv"
    info = {}
    info["host"] = "simulator"
    info["port"] = 2000 + i
    inv["info"] = info
    devices.append(inv)
    j += 1   
  
  return devices

def license():
  licenses= {
      "ppc.enabled": True,
      "p.enabled": True,
      "curt.enabled": True,
      "ramp.p.enabled": True,
      "ramp.q.enabled": True,
      "pfr.enabled": True,
      "q.enabled": True,
      "pf.enabled": True,
      "vrs.enabled": True,
      "qlimit.enabled": True,
      "redundancy.enabled": False,
      "qv.enabled": True,
      "tap.enabled": False,
      "opf.enabled": False,
      "agc.enabled": True,
      "ear.enabled": False,
      "plimit.enabled": True,
      "equilibrator.enabled": True
  }
  
  return licenses

def initialization():
  initializations = {
    "fugue.enabled": False,
    "fugue.p": False,
    "fugue.q": False
  }
  return initializations