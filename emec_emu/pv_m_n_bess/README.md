# PYDAE-HIL

Hardware in the loop for PPC.

## Ejecución simulador


En primer lugar necesitamos definir la estructura de la planta para después compilar el código.
Dependiendo de si queremos simular con baterías o no, tenemos los ficheros pv_mn_bess_builder.py y pv_mn_builder.py. Ambos contienen variables dentro que podremos modificar como la cantidad M de líneas o la cantidad N de inversores por línea. También podremos modificar la potencia por inversor 'S_pv_mva', la tensión nominal de la planta 'V_kv' y la frecuencia nominal de la planta 'V_kv'. En el fichero de genera la planta con BESS podremos modificar la cantidad de potencia que puede entregar el convertidor y la cantidad de energía de almacenaje que posee dicha batería.

```bash
python3 pv_mn_builder.py
```

Tras esto se nos generaran todos los ficheros necesarios para ejecutar la planta, además también se crearan los ficheros config_simulator.json y config_controller.json. 

El fichero emulator.py recibirá un JSON llamado config.json definido a continuación. 

### Config.json


```json
{
    "input": {
        "m_gen": 4, // n lines
        "n_gen": 5, // m inverter for line
        "dt_mid": 0.05, //time execution loop
        "dt": 0.025, // integration interval in pydae
        "pvs": { 
            "temp": 36, //Don't modify this parameter
            "irrad": 600, //Don't modify this parameter
            "p_ref_ppc": 1, //Don't modify this parameter
            "p_max": 72,
            "ramp_p": true,
            "inverter_response":{ //Adjust with the link below.
                "T_lp1p": 0.05,
                "T_lp2p": 0.05,
                "PRampDown": -10,
                "PRampUp": 10,
                "T_lp1q": 0.1,
                "T_lp2q": 0.1,
                "QRampDown": -10,
                "QRampUp": 10
            },
            "lvrt": {
                "mode": 1, //Set "mode" to 0 to allow the inverter to listen to power setpoints during frozen state 
                           //Set "mode" to 1 to deny the inverter to listen to power setpoints during frozen state.
                "lv_umbral": 0.8,
                "lv_in": 0.85,
                "hv_in":1.15, 
                "lv_out": 0.9,
                "hv_out": 1.1, 
                "t_in": 0.1,
                "t_out": 10,
                "i_ref": 0.5 // Q_ref while inverter is in LVRT
            },
            "bess": { //only if there is bess
                "soc_ref_bess": 0.5, //initialization state of charge
                "ramp": true, // 
                "S_bess": 50 // POWER of converter
           }
        }
    }
}
```
[Pincha aquí para ajustar la respuesta de los inversores](https://colab.research.google.com/drive/1rrgkMgOo9Pv838t5k7tac90IvtCiij2A?usp=sharing)


```bash
python3 emulator.py
```

## Consultas.http

En este fichero nos tenemos distintas peticiones que podemos hacer al simulador, son ejemplos de la API de emulator.py . Estas nos permitirán por ejemplo, cambiar la irradiancia que reciben los inversores. Enviar consignas a los inversores o leer datos de estos.
Además podremos cambiar cualquier parametro interno de pydae a través de él.



## To-do and questions

- Traducir al inglés (exito, etc.)
- Why 10.0.0.10:8000?
- agregar q_s_ref_BESS
- ¿Por qué a todo se le aplica ramp?
- ¿Por qué         #Ramp variables?
- ¿Cómo se definen las respuestas a /measures?
- ¿Cómo es lo de MODBUS?
- Se debería hacer una consulta con get_values


