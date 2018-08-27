import sys
import os
import base64
import logging
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from aiohttp import web
from jsonrpcserver.aio import methods
from jsonrpcserver.exceptions import InvalidParams

from JSON_RPC import sentiment_mod as sent_mod

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger('Log: sentiment_analysis')


#
# simple sentiment analysis
# usgin Vade Classifier
#
@methods.add
async def sentiment_intensity_analyzer(**kwargs):

    analizer = SentimentIntensityAnalyzer()

    # Read parameter "data"
    inputData = kwargs.get("data", None)

    text = base64.b64decode(inputData)
    # log.debug(f"add({inputData})")

    # Decode do string
    temp = text.decode('utf-8')

    # Convert in array
    tempArray = temp.split("\n")

    # Declare new array of sentences
    tempDatabase = []

    #Generating temp database
    for line in tempArray:
        if line is not None:
            if len(line) > 1:
                tempDatabase.append(line)

    if inputData is None:
        raise InvalidParams('"inputData" is required')

    # Generate output file
    file = open("./output/output.txt", "w")

    for line in tempDatabase:
        if line is not None:
            if len(line) > 1:
                file.write(line)
                file.write("\n")
                print(str(analizer.polarity_scores(line)))
                file.write(str(analizer.polarity_scores(line)))
                file.write("\n\n")

    file.close()

    # Reading file
    fo = open("./output/output.txt", "r")
    tempStr = base64.b64encode(str(fo.read()).encode('utf-8'))
    fo.close()

    return {'result': str(tempStr)}


#
# complex sentiment analysis
# usgin Vade Classifier
#
@methods.add
async def complex_analysis(**kwargs):

    # Read parameter "data"
    inputData = kwargs.get("data", None)

    if inputData is None:
        raise InvalidParams('"data" is required')

    text = base64.b64decode(inputData)
    # log.debug(f"add({inputData})")

    # Decode do string
    temp = text.decode('utf-8')

    # Convert in array
    tempArray = temp.split("\n")

    # Declare new array of sentences
    tempDatabase = []

    #Generating temp database
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
                file.write(str(sent_mod.sentiment(line)))
                file.write("\n\n")

    file.close()

    # Reading file
    fo = open("./output/output.txt", "r")
    tempStr = base64.b64encode(str(fo.read()).encode('utf-8'))
    fo.close()

    return {'result': str(tempStr)}


#
# custom_corpus_sentiment_analysis
# usgin Vade Classifier
#
@methods.add
async def custom_corpus_sentiment_analysis(**kwargs):

    analizer = SentimentIntensityAnalyzer()

    # Read parameter "data"
    inputData = kwargs.get("data", None)

    if inputData is None:
        raise InvalidParams('"data" is required')

    text = base64.b64decode(inputData)
    # log.debug(f"add({inputData})")

    # Decode do string
    temp = text.decode('utf-8')

    # Convert in array
    tempArray = temp.split("\n")

    # Declare new array of sentences
    tempDatabase = []

    #Generating temp database
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
                file.write(str(sent_mod.sentiment(line)))
                file.write("\n\n")

    file.close()

    # Reading file
    fo = open("./output/output.txt", "r")
    tempStr = base64.b64encode(str(fo.read()).encode('utf-8'))
    fo.close()

    return {'result': str(tempStr)}


# No needed to use again
# Used only on time for generate new corpus from imdb
@methods.add
async def compile_db(**kwargs):
    newcorpus = []

    filesList = os.listdir("./corpus/imdb")

    # Generate new corpus from imdb
    newcorpus = open("./corpus/imdb/corpus.txt", "w")

    for file in filesList:
        tempfile = open("./corpus/imdb/" + file, "r")
        newcorpus.write(str(tempfile.read()))
        newcorpus.write("\n\n")
        tempfile.close()

    newcorpus.close()

    return {'result': "RODOU COMPILE"}


# No needed to use again
# Used only on time for generate positive/negative corpus from imdb
@methods.add
async def compile_sentiment_data(**kwargs):

    # Read parameter "data"
    sentiment_type = kwargs.get("sentiment_type", None)

    if sentiment_type == "positive":
        positive_corpus = []

        positive_file_list = os.listdir("./corpus/imdb/pos")

        # Generate new corpus from imdb
        positive_corpus = open("./corpus/imdb/pos/corpus.txt", "w")

        for file in positive_file_list:
            temp_file = open("./corpus/imdb/pos/" + file, "r")
            positive_corpus.write(str(temp_file.read()))
            positive_corpus.write("\n\n")
            temp_file.close()

        positive_corpus.close()

    if sentiment_type == "negative":
        negative_corpus = []

        negative_files_list = os.listdir("./corpus/imdb/neg")

        # Generate new corpus from imdb
        negative_corpus = open("./corpus/imdb/neg/corpus.txt", "w")

        for file in negative_files_list:
            temp_file = open("./corpus/imdb/neg/" + file, "r")
            negative_corpus.write(str(temp_file.read()))
            negative_corpus.write("\n\n")
            temp_file.close()

        negative_corpus.close()

    return {'result': "Compiled " + sentiment_type + " with success!"}


async def json_rpc_handle(request):
    request = await request.text()
    response = await methods.dispatch(request, trim_log_values=True)
    if response.is_notification:
        return web.Response()
    else:
        return web.json_response(response, status=response.http_status)


if __name__ == '__main__':
    '''
    Runs the JSON-RPC server to communicate with the Snet Daemon.
    '''
    parser = JSON_RPC.services.common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    JSON_RPC.services.common.main_loop(json_rpc_handle, args)
