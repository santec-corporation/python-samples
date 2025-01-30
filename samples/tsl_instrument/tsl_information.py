from enum import Enum


class AlertCode(Enum):
    No00 = "Power supply Error1"
    No02 = "Power supply Error2"
    No03 = "Power supply Error3"
    No04 = "Power setting error (Unconfigurable power)"
    No05 = "Wavelength Error"
    No06 = "Attenuator Error"
    No07 = "Interlock detection"
    No20 = "Temperature control Error1"
    No21 = "Temperature control Error2"
    No22 = "Temperature control Error3"
    No23 = "Temperature control Error4"
    No24 = "Sensor Error1"
    No25 = "Shutter Error"
    No26 = "Sensor Error2"
    No27 = "Connection Error"
    No30 = "Exhaust Fan Error"


class CommandError(Enum):
    NoError = "No error"
    SyntaxError = "Syntax error"
    InvalidSeparator = "Invalid separator"
    ParameterNotAllowed = "Parameter not allowed"
    MissingParameter = "Missing parameter"
    UndefinedHeader = "Undefined header"
    CharacterDataNotAllowed = "Character data not allowed"
    ExecutionError = "Execution error"
    DataOutOfRange = "Data out of range"
    QueryInterrupted = "Query INTERRUPTED"
