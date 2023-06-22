import datetime
import json
import logging
import random
from time import sleep, gmtime, strftime, time
import requests
import string

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,  # If smth wrong, change to 'DEBUG'
                    filename="isun_createCompany.log")  # Name of log file
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
createCompany_API = "https://api-stage.wallter.com/api/v2/company"


def main_flow_create_company():
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

        feeCategory_array = [1, 2, 3, 4, 5]
        for feeCategory in feeCategory_array:
            company_name = random.choices(string.ascii_letters, k=7)
            # company_street = random.choices(string.ascii_letters, k=5)
            # company_city = random.choices(string.ascii_letters, k=4)
            # company_country = random.choices(string.ascii_uppercase, k=2)
            createCompany_payload = {
                "legal_name": company_name,
                "status": "PENDING",
                "fee_program": feeCategory,
                "entity": [
                    "UAB"
                ],
                "info": {
                        "registered_address":{
                            "street": "",
                            "city": "",
                            "postal_code": "123456",
                            "country": "LT"}
                        }
                }
            try:
                createCompany_response = s.post(createCompany_API, headers={'Authorization': "Bearer " + tokenCreate},json=createCompany_payload, verify=False)
                result = createCompany_response.json().get("result")
                companyID = result.get("id")
                companyName = result.get("legal_name")
                feeProgram = result.get("fee_program")
                if createCompany_response.status_code not in (200, 201, 202, 203, 204):
                    logger.info(createCompany_response.status_code)
                    logger.info(createCompany_response.text)
                else:
                    logger.info(companyID)
                    logger.info(companyName)
                    logger.info(feeProgram)
            except requests.exceptions.RequestException as e:
                logger.exception(e)


main_flow_create_company()

