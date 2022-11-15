class Operation:
    def __init__(self, op: str):

        self.op = op

    def __sql__(self) -> str:

        return self.op

    def __and__(self, other: "Operation") -> "Operation":

        return Operation(f"({self.__sql__()} AND {other.__sql__()})")

    def __or__(self, other: "Operation") -> "Operation":

        return Operation(f"({self.__sql__()} OR {other.__sql__()})")

    def __xor__(self, other: "Operation") -> "Operation":

        return Operation(f"({self.__sql__()} XOR {other.__sql__()})")

    def __invert__(self) -> "Operation":

        return Operation(f"NOT {self.__sql__()}")


class Operand:
    def __init__(self, op: str):

        self.op = op

    def __sql__(self) -> str:

        return self.op

    def __lt__(self, other: "Operand") -> "Operation":
        return Operation(f"({self.__sql__()} < {other.__sql__()})")

    def __le__(self, other: "Operand") -> "Operation":
        return Operation(f"({self.__sql__()} <= {other.__sql__()})")

    def __gt__(self, other: "Operand") -> "Operation":
        return Operation(f"({self.__sql__()} > {other.__sql__()})")

    def __ge__(self, other: "Operand") -> "Operation":
        return Operation(f"({self.__sql__()} >= {other.__sql__()})")

    def __ne__(self, other: "Operand") -> "Operation":
        return Operation(f"({self.__sql__()} <> {other.__sql__()})")
