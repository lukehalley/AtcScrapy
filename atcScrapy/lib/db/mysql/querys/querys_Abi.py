from src.db.mysql.actions.actions_Functions import executeReadQuery

def getAbiByDbId(abiDbId):

    query = f"SELECT abis.* " \
            f"FROM abis " \
            f"WHERE abis.abi_id = {abiDbId}"

    result = executeReadQuery(
        query=query
    )

    if len(result) < 1:
        raise Exception(f"No Abi Match For Id {abiDbId}")
    if len(result) == 1:
        return result[0]
    else:
        raise Exception(f"More Than One Abi Matches For Id {abiDbId}")

