import edge
from multiprocessing import Process
import time
from edge import edge_run


if __name__ == "__main__":

    for name in ['POI','LV0101','LV0102','LV0103','LV0104']:

        #edge_config = edge.api_config(name,"192.168.1.100")
        Process(target=edge_run, args=(name,)).start()
                    
        #time.sleep(0.5)

        #Process(target=edge.edge_run, args=(edge_config,)).start()
    

