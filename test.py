import grpc

# import the generated classes
import service.model.sentiment_analysis_rpc_pb2_grpc as grpc_bt_grpc
import service.model.sentiment_analysis_rpc_pb2 as grpc_bt_pb2

from service import registry

if __name__ == '__main__':

    try:

        # Service ONE - Sentiment Analysis
        endpoint = 'localhost:{}'.format(registry['sentiment_analysis']['grpc'])
        # Open a gRPC channel
        channel = grpc.insecure_channel('{}'.format(endpoint))

        # create a stub (client)
        stub = grpc_bt_grpc.ShowMessageStub(channel)
        # create a valid request message
        test_text = "RODANDO TESTES..."
        message = grpc_bt_pb2.InputMessage(value=test_text)
        # make the call
        response = stub.show(message)
        print("TEST METHOD SHOW() PASSED => " + response.value)

    except Exception as e:
        print(e)
