import api
import requests
import re


class Yolanda:

    def __init__(self, host, port):
        self.base = f"http://{host}:{port}"
        self.regex_validador_fechas = "^[0-9]{1,2}[\s]+de[\s]+([a-zA-Z])+[\s]+de[\s]+(((19|20){1}[0-9]{2})|[0-9]{2})$"
        self.regex_extractor_signo = "^L[oa]{1}s[\s]+([^\s]+[oaOA]{1}[sS]{1})([\s]+)pueden([\s]+)(.+)\.$"

    def saludar(self) -> dict:
        response = requests.get(f"{self.base}")
        diccionario = {"status-code": response.status_code, "saludo": response.json()["result"]}
        return diccionario

    def verificar_horoscopo(self, signo: str) -> bool:
        response = requests.get(f"{self.base}/signos")
        lista_signos = response.json()["result"]
        if signo in lista_signos:
            return True
        else:
            return False

    def dar_horoscopo(self, signo: str) -> dict:
        diccionario = {"signo": signo}
        response = requests.get(f"{self.base}/horoscopo", diccionario)
        resultado = response.json()["result"]
        return {"status-code": response.status_code, "mensaje": resultado}



    def dar_horoscopo_aleatorio(self) -> dict:
        response = requests.get(f"{self.base}/aleatorio")
        if response.status_code == 200:
            url = response.json()["result"]
            response_2 = requests.get(url)
            status_code = response_2.status_code
            mensaje = response_2.json()["result"]
        else:
            status_code = response.status_code
            mensaje = response.json()["result"]
        return {"status-code": status_code, "mensaje": mensaje}


    def agregar_horoscopo(self, signo: str, mensaje: str, access_token: str) -> str:
        token_dict = {"Authorization": access_token}
        data_dict = {"signo": signo, "mensaje": mensaje}
        response = requests.post(f"{self.base}/update", headers=token_dict, data=data_dict)
        if response.status_code == 401:
            return "Agregar horóscopo no autorizado"
        elif response.status_code == 400:
            return response.json()["result"]
        else:
            return "La base de YolandAPI ha sido actualizada"
    def actualizar_horoscopo(self, signo: str, mensaje: str, access_token: str) -> str:
        token_dict = {"Authorization": access_token}
        data_dict = {"signo": signo, "mensaje": mensaje}
        response = requests.put(f"{self.base}/update", headers=token_dict, data=data_dict)
        if response.status_code == 401:
            return "Editar horóscopo no autorizado"
        elif response.status_code == 400:
            return response.json()["result"]
        else:
            return "La base de YolandAPI ha sido actualizada"
    def eliminar_signo(self, signo: str, access_token: str) -> str:
        token_dict = {"Authorization": access_token}
        data_dict = {"signo": signo}
        response = requests.delete(f"{self.base}/remove", headers=token_dict, data=data_dict)
        if response.status_code == 401:
            return "Eliminar signo no autorizado"
        elif response.status_code == 400:
            return response.json()["result"]
        else:
            return "La base de YolandAPI ha sido actualizada"


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4444
    DATABASE = {
        "acuario": "Hoy será un hermoso día",
        "leo": "No salgas de casa.... te lo recomiendo",
    }
    thread = api.Server(HOST, PORT, DATABASE)
    thread.start()

    yolanda = Yolanda(HOST, PORT)
    print(yolanda.saludar())
    print(yolanda.dar_horoscopo_aleatorio())
    print(yolanda.verificar_horoscopo("acuario"))
    print(yolanda.verificar_horoscopo("pokemon"))
    print(yolanda.dar_horoscopo("acuario"))
    print(yolanda.dar_horoscopo("pokemon"))
    print(yolanda.agregar_horoscopo("a", "aaaaa", "pepaiic2233"))
    print(yolanda.dar_horoscopo("a"))
