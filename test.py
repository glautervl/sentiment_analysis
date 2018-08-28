import grpc

# import the generated classes
import service.model.sentiment_analysis_rpc_pb2_grpc as grpc_bt_grpc
import service.model.sentiment_analysis_rpc_pb2 as grpc_bt_pb2

from service import registry

from tests_data import b64_sentences

if __name__ == '__main__':

    try:

        # Service ONE - Sentiment Analysis
        endpoint = 'localhost:{}'.format(registry['sentiment_analysis']['grpc'])
        # Open a gRPC channel
        channel = grpc.insecure_channel('{}'.format(endpoint))


        # ShowMessage() Method Test
        # create a stub (client)
        stub = grpc_bt_grpc.ShowMessageStub(channel)
        # create a valid request message
        test_text = "RODANDO TESTES..."
        message = grpc_bt_pb2.InputMessage(value=test_text)
        # make the call
        response = stub.show(message)
        print("ShowMessage() Method Test Passed => " + response.value)
        print()

        # SentimentIntensityAnalysis() Method Test
        # create a stub (client)
        stub = grpc_bt_grpc.SentimentIntensityAnalysisStub(channel)
        # create a valid request message
        test_data = b64_sentences.senteces()
        message = grpc_bt_pb2.InputMessage(value=test_data)
        # make the call
        response = stub.intensivityAnalysis(message)
        print("SentimentIntensityAnalysis() Method Test Passed => " + response.value)
        print()

        # SentimentComplexAnalysis() Method Test
        # create a stub (client)
        stub = grpc_bt_grpc.SentimentComplexAnalysisStub(channel)
        # create a valid request message
        test_data = b64_sentences.senteces()
        message = grpc_bt_pb2.InputMessage(value=test_data)
        # make the call
        response = stub.complexAnalysis(message)
        print("SentimentComplexAnalysis() Method Test Passed => " + response.value)
        print()

        # # CustomCorpusAnalysis() Method Test
        # # create a stub (client)
        # stub = grpc_bt_grpc.CustomCorpusAnalysisStub(channel)
        # # create a valid request message
        # test_text = "RODANDO TESTES..."
        # message = grpc_bt_pb2.InputMessage(value=test_text)
        # # make the call
        # response = stub.show(message)
        # print("CustomCorpusAnalysis() Method Test Passed => " + response.value)
        # print()

        # # TwitterAnalysis() Method Test
        # # create a stub (client)
        # stub = grpc_bt_grpc.TwitterAnalysisStub(channel)
        # # create a valid request message
        # test_text = "RODANDO TESTES..."
        # message = grpc_bt_pb2.InputMessage(value=test_text)
        # # make the call
        # response = stub.show(message)
        # print("TwitterAnalysis() Method Test Passed => " + response.value)
        # print()

    except Exception as e:
        print(e)
