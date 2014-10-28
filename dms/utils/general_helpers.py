
def percentize(numerator, denominator):
    if not denominator:
        return 0
    return 100 * int(numerator) / int(denominator)


def flatten(list_):
     return [item for sublist in list_ for item in sublist]