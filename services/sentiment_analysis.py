import sys
import base64
import logging
import grpc
import concurrent.futures as futures
import services.common
from nltk.sentiment import SentimentIntensityAnalyzer
from services.modules import complex_mod
from services.modules import twitter_mod


# Importing the generated codes from buildproto.sh
import services.model.sentiment_analysis_rpc_pb2_grpc as grpc_bt_grpc
from services.model.sentiment_analysis_rpc_pb2 import OutputMessage

logging.basicConfig(
    level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger('sentiment_analysis')


'''
Simple arithmetic services to test the Snet Daemon (gRPC), dApp and/or Snet-CLI.
The user must provide the method (arithmetic operation) and
two numeric inputs: "a" and "b".

e.g:
With dApp:  'method': mul
            'params': {"a": 12.0, "b": 77.0}
Resulting:  response:
                value: 924.0


Full snet-cli cmd:
$ snet client call mul '{"a":12.0, "b":77.0}'

Result:
(Transaction info)
Signing job...

Read call params from cmdline...

Calling services...

    response:
        value: 924.0
'''


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class ShowMessageServicer(grpc_bt_grpc.ShowMessageServicer):

    def __init__(self):
        # Just for debugging purpose.
        log.debug("ShowMessageServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def show(self, request, context):
        # In our case, request is a InputMessage() object (from .proto file)
        self.value = request.value

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()

        self.result.value = "Processed => " + self.value
        # log.debug('add({},{})={}'.format(self.a, self.b, self.result.value))
        return self.result


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class SentimentIntensityAnalysisServicer(grpc_bt_grpc.SentimentIntensityAnalysisServicer):

    def __init__(self):
        # Just for debugging purpose.
        log.debug("SentimentIntensityAnalysisServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def intensivityAnalysis(self, request, context):

        # In our case, request is a InputMessage() object (from .proto file)
        self.value = request.value

        analizer = SentimentIntensityAnalyzer()

        text = base64.b64decode(self.value)
        # Decode do string
        temp = text.decode('utf-8')
        # Convert in array
        tempArray = temp.split("\n")
        # Result of sentences
        stringResult = ''

        # Generating result
        for line in tempArray:
            if line is not None:
                if len(line) > 1:
                    stringResult += line
                    stringResult += '\n'
                    stringResult += str(analizer.polarity_scores(line))
                    stringResult += '\n\n'

        # Encoding result
        resultBase64 = base64.b64encode(str(stringResult).encode('utf-8'))

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()
        self.result.value = resultBase64
        # log.debug('add({},{})={}'.format(self.a, self.b, self.result.value))
        return self.result


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class SentimentComplexAnalysisServicer(grpc_bt_grpc.SentimentComplexAnalysisServicer):

    def __init__(self):
        # Just for debugging purpose.
        log.debug("SentimentComplexAnalysisServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def complexAnalysis(self, request, context):
        # In our case, request is a InputMessage() object (from .proto file)
        self.value = request.value

        text = base64.b64decode(self.value)
        # Decode do string
        temp = text.decode('utf-8')
        # Convert in array
        tempArray = temp.split("\n")
        # Result of sentences
        stringResult = ''

        # Generating result
        for line in tempArray:
            if line is not None:
                if len(line) > 1:
                    stringResult += line
                    stringResult += '\n'
                    stringResult += str(complex_mod.sentiment(line))
                    stringResult += '\n\n'

        # Encoding result
        resultBase64 = base64.b64encode(str(stringResult).encode('utf-8'))

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()
        self.result.value = resultBase64
        # log.debug('add({},{})={}'.format(self.a, self.b, self.result.value))
        return self.result


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class CustomCorpusAnalysisServicer(grpc_bt_grpc.ShowMessageServicer):

    def __init__(self):
        # Just for debugging purpose.
        log.debug("CustomCorpusAnalysisServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def customCorpusAnalysis(self, request, context):
        # In our case, request is a InputMessage() object (from .proto file)
        self.value = request.value

        # Read parameter "data"
        inputData = request.value

        text = base64.b64decode(inputData)

        # Decode do string
        temp = text.decode('utf-8')

        # Convert in array
        tempArray = temp.split("\n")

        # Declare new array of sentences
        tempDatabase = []

        # Generating temp database
        for line in tempArray:
            if line is not None:
                if len(line) > 1:
                    tempDatabase.append(line)

        # Generate output file
        file = open("./output/output.txt", "w")

        for line in tempDatabase:
            if line is not None:
                if len(line) > 1:
                    file.write(line)
                    file.write("\n")
                    # print(str(sent_mod.sentiment(line)))
                    file.write(str(complex_mod.sentiment(line)))
                    file.write("\n\n")

        file.close()

        # Reading file
        fo = open("./output/output.txt", "r")
        resultBase64 = base64.b64encode(str(fo.read()).encode('utf-8'))
        fo.close()

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()
        self.result.value = resultBase64
        # log.debug('add({},{})={}'.format(self.a, self.b, self.result.value))
        return self.result


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class TwitterAnalysisServicer(grpc_bt_grpc.TwitterAnalysisServicer):

    def __init__(self):
        # Just for debugging purpose.
        log.debug("TwitterAnalysisServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def twitterAnalysis(self, request, context):
        # In our case, request is a InputMessage() object (from .proto file)
        self.languages = request.languages
        self.sentences = request.sentences

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()

        self.result.value = twitter_mod.analyze(self.languages, self.sentences)

        # log.debug('add({},{})={}'.format(self.a, self.b, self.result.value))
        return self.result


# The gRPC serve function.
#
# Params:
# max_workers: pool of threads to execute calls asynchronously
# port: gRPC server port
#
# Add all your classes to the server here.
# (from generated .py files by protobuf compiler)
def serve(max_workers=10, port=7777):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    grpc_bt_grpc.add_ShowMessageServicer_to_server(ShowMessageServicer(), server)
    grpc_bt_grpc.add_SentimentIntensityAnalysisServicer_to_server(SentimentIntensityAnalysisServicer(), server)
    grpc_bt_grpc.add_SentimentComplexAnalysisServicer_to_server(SentimentComplexAnalysisServicer(), server)
    grpc_bt_grpc.add_CustomCorpusAnalysisServicer_to_server(CustomCorpusAnalysisServicer(), server)
    grpc_bt_grpc.add_TwitterAnalysisServicer_to_server(TwitterAnalysisServicer(), server)
    server.add_insecure_port('[::]:{}'.format(port))
    return server


if __name__ == '__main__':
    '''
    Runs the gRPC server to communicate with the Snet Daemon.
    '''
    parser = services.common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    services.common.main_loop(serve, args)
