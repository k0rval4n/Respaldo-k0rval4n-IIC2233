import re

regex_validador_fechas = "([0-9]{1,2}) de ([a-zA-Z])+ de ([0-9]{2}|((19|20){1}[0-9]{2}))"
regex_extractor_signo = "^L[oa]{1}s[\s]+([^\s]+)([\s]+)(.+)\.$"

















texto = "Los capricornianos pueden dormir la mejor siesta del semestre."
respuesta = re.search("^([a-zA-Z]|\s)+\.$", texto)
print(respuesta.group(0))