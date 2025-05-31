import random

def generar_token(): #esta funcion genera el token un numero de 6 digitos
    return "{:06d}".format(random.randint(0, 999999))