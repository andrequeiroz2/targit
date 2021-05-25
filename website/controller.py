import ast
import requests


def cep_search(cep: str) -> dict:
    
        r = requests.get('http://viacep.com.br/ws/'+cep+'/json/unicode/')

        if r.status_code != 200:
            resp = {
                "erro": r.status_code
            }
            return resp
        
        byte_str = r.content
        dict_str = byte_str.decode("UTF-8")
        
        #validate
        if "erro" in dict_str:
            resp = {
                "erro": dict_str
            }
            return resp
        
        data = ast.literal_eval(dict_str)

        resp = {
            "cep": data["cep"],
            "logradouro": data["logradouro"],
            "complemento": data["complemento"],
            "bairro": data["bairro"],
            "localidade" : data["localidade"],
            "uf": data["uf"],
            "ibge": data["ibge"],
            "gia": data["gia"],
            "ddd": data["ddd"],
            "siafi": data["siafi"]
        }
        return resp
        
        