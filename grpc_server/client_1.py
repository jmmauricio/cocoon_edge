import grpc
import communication_pb2
import communication_pb2_grpc
import numpy as np
import time

def main():
    with grpc.insecure_channel('10.0.0.2:50051') as channel:
        stub = communication_pb2_grpc.CommunicationStub(channel)
        t_0 = time.time()
        for it in range(1000):
            numbers = communication_pb2.NumbersRequest(
                number1=time.time()-t_0,
                number2=time.time()-t_0,
                number3=time.time()-t_0,
                number4=time.time()-t_0
            )
            response = stub.SendNumbers(iter([numbers]))
            #print("Response from server:", response.message)

if __name__ == '__main__':
    main()
