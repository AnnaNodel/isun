import datetime
import json
import logging
import random
from time import sleep, gmtime, strftime, time
import requests
import string
# update the transaction's amount in json file before you run the test

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,  # If smth wrong, change to 'DEBUG'
                    filename="isun_createTransaction.log")  # Name of log file
logger = logging.getLogger("Isun")
timeout = 15  # Timeout for APIs check (login not included!), in seconds
loop_time = 60  # Time between every loop, in second

# token credentials
client_id = "vgCjKlRUeObC0NivSQhlXyTTVMwm8lFW"
client_secret = "CMm94X9wbze-cGwCx8IcYW6lkxf6b0flWMQM8P5gSCj8tEOmzrmFDourMp8D7sY6"
token_API = "https://api-stage.wallter.com/api/v2/auth/token"
tokenPayload = {
    "client_id": client_id,
    "client_secret": client_secret
}

# transaction credentials
DebitOPRtrxAPI = "https://isun-stage.wallter.com/api/v2/payments/new_transaction"


def main_create_trx():
    with requests.Session() as s:
        try:
            tokenResponse = s.post(token_API, json=tokenPayload, verify=False)
            tokenCreate = tokenResponse.json().get("access_token")
            if tokenResponse.status_code in (200, 201, 202, 204):
                logger.info("Successfully logged in!")
            else:
                logger.info(tokenResponse.status_code)
        except requests.exceptions.RequestException as e:
            logger.exception(e)

        try:
            with open("C:\\Users\\annan\\Downloads\\OPRDEBITTRX.json") as payload_file:
                DebitOPRtrxPayload = payload_file.read()

            DebitOPRtrxResponse = s.post(DebitOPRtrxAPI, headers={'Authorization': "Bearer " + tokenCreate},
                                     data=DebitOPRtrxPayload, verify=False)

            if DebitOPRtrxResponse.status_code in (200, 201, 202, 204) and DebitOPRtrxResponse.text != 'null\n':
                result = DebitOPRtrxResponse.json().get("result")
                TRXType = result.get("type")
                TRXDirection = result.get("direction")
                TRXAmount = result.get("amount")
                TRXFee = result.get("fee")
                TRXSubtype = result.get("subtype")
                TRXStatus = result.get("status")
                TRXID = result.get("id")
                logger.info(TRXID)
                logger.info(TRXStatus)
                logger.info(TRXDirection)
                logger.info(TRXType)
                logger.info(TRXSubtype)
                logger.info(TRXAmount)
                logger.info(TRXFee)
            else:
                logger.info(DebitOPRtrxResponse.status_code)
                logger.info(DebitOPRtrxResponse.text)

        except requests.exceptions.RequestException as e:
            logger.exception(e)


main_create_trx()
