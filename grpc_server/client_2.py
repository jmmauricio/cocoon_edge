import grpc
import communication_pb2
import communication_pb2_grpc

def main():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = communication_pb2_grpc.CommunicationStub(channel)
        numbers = communication_pb2.NumbersRequest(
            number1=2.1,
            number2=2.2,
            number3=2.3,
            number4=2.4
        )
        response = stub.SendNumbers(iter([numbers]))
    print("Response from server:", response.message)

if __name__ == '__main__':
    main()
