from eth_abi import abi
from atcScrapy.lib.db.dynamodb.query.query_table import QuerySigTable

def DBDecode(InputData):
    MethodId = InputData[0:10]
    MethodParams = bytes.fromhex(InputData[10:])
    SignatureQueryResults = QuerySigTable(HashedSignature=MethodId)
    if len(SignatureQueryResults) > 0:
        ResultsToReturn = []
        for Signature in SignatureQueryResults:
            FunctionName = Signature["name"]

            FunctionDef = (Signature["fullSignature"][
                           Signature["fullSignature"].find("(") + 1:Signature["fullSignature"].find(")")]).split(", ")
            FunctionArgTypes = (Signature["hashableSignature"][
                                Signature["hashableSignature"].find("(") + 1:Signature["hashableSignature"].find(
                                    ")")]).split(",")
            try:
                DecodedInputs = abi.decode(FunctionArgTypes, MethodParams)

                DecodedParameters = []

                i = 0
                for Def in FunctionDef:

                    DecodedParameter = {}

                    SplitDef = Def.split(" ")

                    DecodedParameter["name"] = SplitDef[1]
                    DecodedParameter["type"] = SplitDef[0]

                    CurrentVal = DecodedInputs[i]
                    if isinstance(CurrentVal, (list, tuple)):
                        FunctionParameter = ','.join(CurrentVal)
                    else:
                        FunctionParameter = str(CurrentVal)
                    DecodedParameter["value"] = FunctionParameter

                    DecodedParameters.append(DecodedParameter)

                    i = i + 1

                DecodeObject = {
                    "functionName": FunctionName,
                    "functionParameters": DecodedParameters,
                }

                ResultsToReturn.append(DecodeObject)

            except:
                continue

        if len(ResultsToReturn) > 0:
            return True, 'DB Decode Success', ResultsToReturn
        else:
            return False, 'DB Decode Failure - No DB Results', None

    else:
        return False, 'DB Decode Failure - No DB Results', None