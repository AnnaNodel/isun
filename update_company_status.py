import datetime
import json
import logging
import random
from time import sleep, gmtime, strftime, time
import requests
import string
from mongo_client import MongoClient
import subprocess

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,  # If smth wrong, change to 'DEBUG'
                    filename="isun_createCompany.log")  # Name of log file
logger = logging.getLogger("Isun")
timeout = 15  # Timeout for APIs check (login not included!), in seconds
loop_time = 60  # Time between every loop, in second
mongo = MongoClient("companies", "mongodb://Wallter:Wallter2020@127.0.0.1:27017")

# token credentials
client_id = "vgCjKlRUeObC0NivSQhlXyTTVMwm8lFW"
client_secret = "CMm94X9wbze-cGwCx8IcYW6lkxf6b0flWMQM8P5gSCj8tEOmzrmFDourMp8D7sY6"
token_API = "https://api-stage.wallter.com/api/v2/auth/token"
tokenPayload = {
    "client_id": client_id,
    "client_secret": client_secret
}
createCompany_API = "https://api-stage.wallter.com/api/v2/company"


def main_flow_create_all():
    with requests.Session() as s:
        try:
            tokenResponse = s.post(token_API, json=tokenPayload, verify=False)
            tokenCreate = tokenResponse.json().get("access_token")
            if tokenResponse.status_code in (200, 201, 202, 204):
                logger.info("Successfully logged in!")
            else:
                logger.info(tokenPayload.status_code)
        except requests.exceptions.RequestException as e:
            logger.exception(e)

        # create company
        company_name = random.choices(string.ascii_letters, k=7)

        createCompany_payload = {
            "legal_name": company_name,
            "status": "PENDING",
            "fee_program": 2,
            "entity": [
                "UAB"
            ],
            "info": {
                "registered_address": {
                    "street": "",
                    "city": "",
                    "postal_code": "123456",
                    "country": "LT"}
            }
        }
        try:
            createCompany_response = s.post(createCompany_API, headers={'Authorization': "Bearer " + tokenCreate},
                                            json=createCompany_payload, verify=False)
            result = createCompany_response.json().get("result")
            companyID = result.get("id")
            company_name = result.get("legal_name")

            if createCompany_response.status_code in (200, 201, 202, 203, 204):
                a = "ssh -i wlt-test-20230104.pem ec2-user@13.41.160.110"
                b = '"mongo --eval \'db.companies.find'
                c = '({ \"id\": '
                e = f"{companyID}"
                f = "})"
                d = ".projection ({_id: 1})' wallter --quiet\""
                command = f"{a} {b} {c} {e} {f} {d}"
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                k = result.stdout.split('{ "_id" : ObjectId("')[1]
                _id = k.split('") }\n')[0]

                logger.info(companyID)
                logger.info(company_name)
                updateStatusAPI = "https://api-stage.wallter.com/api/company/"
                statusCompany_array = ["SIGNATURE", "SUSPENDED", "APPROVED", "TERMINATED", "REJECTED", "CLOSED", "CLOSE-APP"]
                for statusCompany in statusCompany_array:
                    statusPayload = {"status": statusCompany}
                    try:
                        updateStatusResponse = s.patch(updateStatusAPI + _id, headers={'Authorization': "Bearer " + tokenCreate},
                                                      json=statusPayload, verify=False)
                        updateResult = updateStatusResponse.json().get("result")
                        companyName = updateResult.get("legal_name")
                        companyStatus = updateResult.get("status")

                        if updateStatusResponse.status_code in (200, 201, 202, 204):
                            # logger.info(companyName)
                            logger.info(companyStatus)
                        else:
                            logger.info(updateStatusResponse.status_code)
                            logger.info(updateStatusResponse.text)
                    except requests.exceptions.RequestException as e:
                        logger.exception(e)

            else:
                logger.info(createCompany_response.status_code)
                logger.info(createCompany_response.text)

        except requests.exceptions.RequestException as e:
            logger.exception(e)


main_flow_create_all()
