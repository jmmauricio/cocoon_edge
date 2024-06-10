import grpc
from concurrent import futures
import time
import communication_pb2
import communication_pb2_grpc

class CommunicationServicer(communication_pb2_grpc.CommunicationServicer):
    def SendNumbers(self, request_iterator, context):
        for request in request_iterator:
            print("Received numbers from client:", request.number1, request.number2, request.number3, request.number4)
        return communication_pb2.NumbersResponse(message="")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    communication_pb2_grpc.add_CommunicationServicer_to_server(CommunicationServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started. Listening on port 50051...")
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
