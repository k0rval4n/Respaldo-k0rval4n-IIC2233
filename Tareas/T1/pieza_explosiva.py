class PiezaExplosiva:
    def __init__(self, alcance: int, tipo: str, posicion: list) -> None:
        self.alcance = alcance
        self.tipo = tipo
        self.posicion = posicion

    def __str__(self) -> str:
        fila, columna = self.posicion
        texto = f"Soy la pieza {self.tipo}{self.alcance}\n"
        texto += f"\tEstoy en la fila {fila} y columna {columna}\n"
        return texto

    def verificar_alcance(self, fila: int, columna: int) -> bool:
        alcanzable = False
        if self.tipo == "V":
            if columna == self.posicion[1]:
                alcanzable = True
        elif self.tipo == "H":
            if fila == self.posicion[0]:
                alcanzable = True
        elif self.tipo == "R":
            if columna == self.posicion[1] or fila == self.posicion[0]:
                alcanzable = True
            if ((columna - self.posicion[1])**2)**(1/2) == \
                    ((fila - self.posicion[0])**2)**(1/2):
                alcanzable = True

        return alcanzable


if __name__ == "__main__":
    """
    Ejemplos:

    Dado el siguiente tablero
    [
        ["--", "V2", "PP", "--", "H2"],
        ["H3", "--", "--", "PP", "R11"]
    ]

    """
    # Ejemplo 1 - Pieza R11
    pieza_1 = PiezaExplosiva(11, "R", [5, 5])
    print(str(pieza_1))
    print(pieza_1.verificar_alcance(6, 4))

    # Ejemplo 2 - Pieza V2
    pieza_2 = PiezaExplosiva(2, "V", [0, 1])
    print(str(pieza_2))
