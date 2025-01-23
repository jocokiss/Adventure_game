import os
from dotenv import load_dotenv

import pymongo

from src.utilities.api_actions import GameAPIClient



if __name__ == "__main__":
    load_dotenv()
    token_key = os.getenv('TOKEN_KEY')
    print(token_key)


    # api_client = GameAPIClient()
    # mongo_string = api_client.mongo_string()
    # print(mongo_string)
