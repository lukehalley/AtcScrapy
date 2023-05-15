from eth_abi import abi
from atcScrapy.lib.api.api_fourbyte import SearchHexSignature

def APIDecode(InputData):
    MethodId = InputData[0:10]
    MethodParams = bytes.fromhex(InputData[10:])
    HexFound, APIResults = SearchHexSignature(MethodId)
    ResultsToReturn = []
    if HexFound and len(APIResults) > 0:
        for Signature in APIResults["results"]:
            SplitFunction = Signature["text_signature"].split("(")

            FunctionName = SplitFunction[0]

            FunctionParametersTypes = SplitFunction[1].replace(")", "").split(",")

            try:

                DecodedInput = abi.decode(FunctionParametersTypes, MethodParams)

                DecodedParameters = []

                for Input in DecodedInput:

                    DecodedParameter = {}

                    i = DecodedInput.index(Input)
                    DecodedParameter["name"] = f"unknown_input_{i + 1}"

                    DecodedParameter["type"] = FunctionParametersTypes[i]

                    if isinstance(Input, (bytes, bytearray)):
                        Input = Input.decode("utf-8")

                    if isinstance(Input, (list, tuple)):
                        FunctionParameter = ','.join(Input)
                    else:
                        FunctionParameter = str(Input)

                    DecodedParameter["value"] = FunctionParameter

                    DecodedParameters.append(DecodedParameter)

                DecodeObject = {
                    "functionName": FunctionName,
                    "functionParameters": DecodedParameters
                }

                ResultsToReturn.append(DecodeObject)

            except:
                continue

        if len(ResultsToReturn) > 0:
            return True, 'DB Decode Success', ResultsToReturn
        else:
            return False, 'DB Decode Failure', None
    else:
        return False, 'DB Decode Failure', None