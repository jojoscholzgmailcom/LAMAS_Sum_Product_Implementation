import re

class Parser(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.functionNumber = 1
        return cls._instance

    def parse(self, logicStatement: str) -> Callable[[World, dict[tuple [int, int], World]], bool]:
        return globals()[self._parseToString(logicStatement, 0)]

    def _parseToString(self, logicStatement: str, start: int) -> str:
        functionStr = "def generatedFunctionName" + self.functionNumber + "(world, worlds):\n"
        currentFunctionNumber = self.functionNumber
        self.functionNumber += 1

        exec(functionStr)
        return "generatedFunctionName" + currentFunctionNumber