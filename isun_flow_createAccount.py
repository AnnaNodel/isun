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
            "status": "APPROVED",
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
            companyName = result.get("legal_name")
            feeProgram = result.get("fee_program")
            companyStatus = result.get("status")
            if createCompany_response.status_code not in (200, 201, 202, 203, 204):
                logger.info(createCompany_response.status_code)
                logger.info(createCompany_response.text)
            else:
                logger.info(companyID)
                logger.info(companyName)
                logger.info(feeProgram)
                logger.info(companyStatus)
                currency_Array = ["EUR", "CAD", "USD", "GBP"]
                #  create Accounts with different currencies
                for currency in currency_Array:
                    try:
                        createAccount_payload = {
                            "is_main": True,
                            "type": "DESIGNATED",
                            "status": "ACTIVE",
                            "name": "string",
                            "acc_details": {
                                "type": "IBAN",
                                "currency": currency,
                                "bic": "WAUALT21"
                            }
                        }
                        createAccount_response = s.post(
                            "https://api-stage.wallter.com/api/v2/account/company/" + str(companyID) + "/account",
                            headers=dict(
                                Authorization="Bearer " + tokenCreate), json=createAccount_payload, verify=False)
                        result = createAccount_response.json().get("result")
                        accDetails = result.get("acc_details")
                        currencyCode = accDetails.get("currency")
                        accountID = result.get("id")
                        accountType = result.get("type")
                        entity = result.get("entity")
                        if createAccount_response.status_code in (200, 201, 202, 203, 204):
                            logger.info(accountID)
                            logger.info(entity)
                            logger.info(accountType)
                            logger.info(currencyCode)
                        else:
                            logger.info(createAccount_response.status_code)
                            logger.info(createAccount_response.text)
                    except requests.exceptions.RequestException as e:
                        logger.exception(e)

        except requests.exceptions.RequestException as e:
            logger.exception(e)


main_flow_create_all()