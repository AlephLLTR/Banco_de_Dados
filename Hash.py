alph: str = "0123456789abcdefghijklmnopqrstuvxwyzABCDEFGHIJKLMNOPQRSTUVXWYZ"

def Hash_1(value: str, limit: int) -> int:
    base_value: int = 0
    for char in value:
        if char in alph:
            base_value += alph.find(char) ** 7
    base_value += len(value) * 11
    return base_value % limit

def Hash_2(value: str, limit: int) -> int:
    base_value: int = 0
    for char in value:
        if char in alph:
            base_value += alph.find(char) ** 97
    base_value += len(value) * 11
    return base_value % limit



    # for char in alph:
    #     base_value += alph.find(char) ** 97 
    # base_value += len(alph)
    # return base_value % limit