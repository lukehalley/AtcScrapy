import requests

FOUR_BYTE_ENDPOINT = "https://www.4byte.directory/api/v1"

def SearchHexSignature(HexSignature):

    ApiEndpoint = f"{FOUR_BYTE_ENDPOINT}/signatures/?hex_signature={HexSignature}"

    Response = requests.get(url=ApiEndpoint)

    ResultsJSON = Response.json()

    if Response.ok and ResultsJSON["count"] > 0:
        return True, ResultsJSON
    else:
        return False, None