def decode_filter(DecodeResults):
    SwapFunctions = ["swapExactTokensForTokens",
                     "swapTokensForExactTokens",
                     "swapExactETHForTokens",
                     "swapTokensForExactETH",
                     "swapExactTokensForETH",
                     "swapETHForExactTokens",
                     "swapExactTokensForTokensSupportingFeeOnTransferTokens",
                     "swapExactETHForTokensSupportingFeeOnTransferTokens",
                     "swapExactTokensForETHSupportingFeeOnTransferTokens"]

    FilteredDecodeResults = []

    if DecodeResults:
        for DecodeResult in DecodeResults:
            if DecodeResult["functionName"].lower() in (SwapFunction.lower() for SwapFunction in SwapFunctions):
                FilteredDecodeResults.append(DecodeResult)

    ResultsPresentAfterFilter = len(FilteredDecodeResults) > 0

    return ResultsPresentAfterFilter, FilteredDecodeResults