from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from pydantic import BaseModel

import logging

WORD = "words_"
EXTENSION = ".txt"
PATH = "../words/"

app = FastAPI()


class Sentence(BaseModel):
    input: str


def sentence_to_list(sentence):
    return sentence.split()


def log_response(response):
    logging.basicConfig(filename='../log/responses.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logger = logging.getLogger()
    logger.info(response)


def get_dictionary(character):
    word_dict = {}
    try:
        file_name = PATH + WORD + character + EXTENSION
        file = open(file_name, "r")
        for word in file:
            word = word.replace("\n", "")
            word = word.replace("'s", "")
            word_dict[word] = True
        return word_dict
    except OSError as e:
        return word_dict



@app.post("/")
async def classify_input(sentence: Sentence):
    input = sentence.input
    words = sentence_to_list(input)
    response = {}
    for word in words:
        word = word.lower()
        word_dict = get_dictionary(word[0])
        if word_dict.get(word) :
            pass
        else:
            log_info = {'input': input, 'response': '400 Bad Request' }
            log_response(log_info)
            response['status'] = 'error'
            response['message'] = 'Bad Request'
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response)

    log_info = {'input': input, 'response': 'en-US'}
    log_response(log_info)
    response['status'] = 'success'
    response['message'] = 'en-US'
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)



