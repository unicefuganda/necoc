
def percentize(numerator, denominator):
    if not denominator:
        return 0
    return 100 * int(numerator) / int(denominator)