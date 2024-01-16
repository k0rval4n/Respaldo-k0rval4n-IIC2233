from abc import ABC, abstractmethod
import random


class Vehiculo(ABC):
    identificador = 0

    def __init__(self, rendimiento, marca, energia=120, *args, **kwargs):
        self.rendimiento = int(rendimiento)
        self.marca = str(marca)
        self._energia = int(energia)
        self.identificador = Vehiculo.identificador
        Vehiculo.identificador += 1

    @abstractmethod
    def recorrer(self, kilometros) -> None:
        pass

    @property
    def autonomia(self) -> float:
        return self.rendimiento * self._energia

    @property
    def energia(self):
        return self._energia

    @energia.setter
    def energia(self, nueva_energia):
        self._energia = max(0, nueva_energia)


class AutoBencina(Vehiculo):
    def __init__(self, bencina_favorita, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bencina_favorita = int(bencina_favorita)

    def recorrer(self, kilometros) -> str:
        if kilometros < self.autonomia:
            km_recorridos = kilometros
        else:
            km_recorridos = self.autonomia
        l_gastados = (km_recorridos / self.rendimiento)
        if str(l_gastados)[-2:] == ".0":
            l_gastados = int(l_gastados)
        self.energia -= l_gastados
        # Diferencia enunciado - test_cases: se prioriza lo mostrado por los test_cases.
        return f"Anduve por {km_recorridos}Km y gasté {l_gastados}L de bencina"


class AutoElectrico(Vehiculo):
    def __init__(self, vida_util_bateria, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.vida_util_bateria = int(vida_util_bateria)

    def recorrer(self, kilometros) -> str:
        if kilometros < self.autonomia:
            km_recorridos = kilometros
        else:
            km_recorridos = self.autonomia
        w_gastados = (km_recorridos / self.rendimiento)
        if str(w_gastados)[-2:] == ".0":
            w_gastados = int(w_gastados)
        self.energia -= w_gastados
        return f"Anduve por {km_recorridos}Km y gasté {w_gastados}W de energía eléctrica"


class Camioneta(AutoBencina):
    def __init__(self, capacidad_maleta, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.capacidad_maleta = int(capacidad_maleta)


class Telsa(AutoElectrico):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def recorrer(self, kilometros) -> str:
        return AutoElectrico.recorrer(kilometros) + "de forma inteligente"


class FaitHibrido(AutoBencina, AutoElectrico):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(vida_util_bateria=5, *args, **kwargs)

    def recorrer(self, kilometros) -> str:
        km_bencina = kilometros / 2
        km_electrico = kilometros / 2
        return AutoBencina.recorrer(self, km_bencina) + AutoElectrico.recorrer(self, km_electrico)
