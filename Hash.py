alph: str = "0123456789abcdefghijklmnopqrstuvxwyzABCDEFGHIJKLMNOPQRSTUVXWYZ"

def Hash_1(value: str, limit: int) -> int:
    rawValue: int = 0
    for char in value:
        if char in alph:
            rawValue += alph.find(char) ** 7
    rawValue += len(value) * 11
    return rawValue % limit

# def Hash_2(string: str, limit: int) -> int:
#     base_value: int = 0
#     for char in alph:
#         base_value += alph.find(char) ** 97 
#     pass