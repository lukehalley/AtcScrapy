from eth_abi import abi

SwapFunctions = {
    "swapExactTokensForTokens": [
        ('uint', 'amountIn'),
        ('uint', 'amountOutMin'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapTokensForExactTokens": [
        ('uint', 'amountOut'),
        ('uint', 'amountInMax'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapExactETHForTokens": [
        ('uint', 'amountOutMin'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapTokensForExactETH": [
        ('uint', 'amountOut'),
        ('uint', 'amountInMax'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapExactTokensForETH": [
        ('uint', 'amountIn'),
        ('uint', 'amountOutMin'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapETHForExactTokens": [
        ('uint', 'amountOut'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapExactTokensForTokensSupportingFeeOnTransferTokens": [
        ('uint', 'amountIn'),
        ('uint', 'amountOutMin'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapExactETHForTokensSupportingFeeOnTransferTokens": [
        ('uint', 'amountOutMin'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapExactTokensForETHSupportingFeeOnTransferTokens": [
        ('uint', 'amountIn'),
        ('uint', 'amountOutMin'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ]
}

SwapMethods = {
    "0x38ed1739": "swapExactTokensForTokens",
    "0x7ff36ab5": "swapExactETHForTokens",
    "0x791ac947": "swapExactTokensForETHSupportingFeeOnTransferTokens",
    "0x4a25d94a": "swapTokensForExactETH",
    "0xfb3bdb41": "swapETHForExactTokens",
    "0xb6f9de95": "swapExactETHForTokensSupportingFeeOnTransferTokens",
    "0x5c11d795": "swapExactTokensForTokensSupportingFeeOnTransferTokens",
    "0x8803dbee": "swapTokensForExactTokens",
    "0x4e71d92d": "claim",
    "0x18cbafe5": "swapExactTokensForETH",
    "0x1d85bf03": "bugNFT",
    "0xded9382a": "removeLiquidityETHWithPermit",
    "0xe0f4e5b2": "swapForBNB",
    "0xa9059cbb": "transfer",
    "0x095ea7b3": "approve",
    "0x6c197ff5": "sell",
    "0x7f8661a1": "exit"
}

def OfflineDecode(InputData):
    MethodId = InputData[0:10]
    MethodParams = bytes.fromhex(InputData[10:])
    if MethodId in SwapMethods:
        MethodName = SwapMethods[MethodId]
        FunctionArgs = SwapFunctions[MethodName]
        try:
            ArgTypes = [FunctionArg[0] for FunctionArg in FunctionArgs]
            DecodedInput = abi.decode(ArgTypes, MethodParams)
            DecodedMapped = {}
            for FunctionArg in FunctionArgs:
                FunctionName = FunctionArg[1]
                Index = FunctionArgs.index(FunctionArg)
                DecodedMapped[FunctionName] = DecodedInput[Index]
            return True, 'Offline Decode Success', MethodName, DecodedMapped
        except:
            return False, 'Offline Decode Failure', None, None
    else:
        for SwapFunction in SwapFunctions:
            FunctionArgs = SwapFunctions[SwapFunction]
            try:
                ArgTypes = [FunctionArg[0] for FunctionArg in FunctionArgs]
                DecodedInput = abi.decode(ArgTypes, MethodParams)
                DecodedMapped = {}
                for FunctionArg in FunctionArgs:
                    FunctionName = FunctionArg[1]
                    Index = FunctionArgs.index(FunctionArg)
                    DecodedMapped[FunctionName] = DecodedInput[Index]
                return True, 'Offline Decode Success', SwapFunction, DecodedMapped
            except:
                continue
        return False, 'Offline Decode Failure', None, None