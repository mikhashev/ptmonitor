
from openapi_client import openapi


def authenticate():
    """
    get token locate locally and connect to api
    :return: client
    """

    with open('my_ti_token.txt', "r") as file:
        token = file.read()
    client = openapi.api_client(token)



    return client




if __name__ == '__main__':

    authenticate()

