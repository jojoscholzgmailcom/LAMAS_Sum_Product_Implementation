import re

# This is the old approach, please disregard, only used for inspiration
class Parser(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.functionNumber = 1
        return cls._instance

    def parse(self, logicStatement: str) -> Callable[[World, dict[tuple [int, int], World]], bool]:
        return globals()[self._parseToString(logicStatement, 0)]

    def _parseToString(self, logicStatement: str, index: int) -> str:
        functionStr = "def generatedFunctionName" + self.functionNumber + "(world, worlds):\n"
        currentFunctionNumber = self.functionNumber
        self.functionNumber += 1
        tempFuncStr = ""
        match logicStatement[index]:
            case 'x':
                numMatch = re.match(r'[0-9]+', logicStatement[index + 1:])
                assert numMatch is not None; "The propositional atom x needs to have a number behind for example: x12 "
                number = logicStatement[numMatch.pos:numMatch.endpos]
                tempFuncStr += " x == " + number
            case 'y':
                numMatch = re.match(r'[0-9]+', logicStatement[index + 1:])
                assert numMatch is not None; "The propositional atom y needs to have a number behind for example: y12 "
                number = logicStatement[numMatch.pos:numMatch.endpos]
                tempFuncStr += " y == " + number
            case '-':
                tempFuncStr += " not"
            case '|':
                tempFuncStr += " or"
            case '&':
                
        exec(functionStr)
        return "generatedFunctionName" + currentFunctionNumber