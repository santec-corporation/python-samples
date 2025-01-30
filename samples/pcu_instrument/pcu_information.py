from enum import Enum


class ErrorCode(Enum):
    NO_ERROR = "0"
    SYNTAX_ERROR = "-102"
    INVALID_SEPARATOR = "-103"
    PARAMETER_NOT_ALLOWED = "-108"
    MISSING_PARAMETER = "-109"
    UNDEFINED_HEADER = "-113"
    INVALID_SUFFIX = "-131"
    CHARACTER_DATA_NOT_ALLOWED = "-148"
    EXECUTION_ERROR = "-200"
    DATA_OUT_OF_RANGE = "-222"
    ILLEGAL_PARAMETER_VALUE = "-224"
    QUERY_INTERRUPTED = "-410"

    @staticmethod
    def get_description(error_code) -> str:
        error_descriptions = {
            ErrorCode.NO_ERROR: "No error occurred during the operation.",
            ErrorCode.SYNTAX_ERROR: "The command contains an invalid syntax or unrecognized format.",
            ErrorCode.INVALID_SEPARATOR: "A separator in the command is missing or incorrect.",
            ErrorCode.PARAMETER_NOT_ALLOWED: "The command contains an unexpected or unsupported parameter.",
            ErrorCode.MISSING_PARAMETER: "Required parameter(s) are missing from the command.",
            ErrorCode.UNDEFINED_HEADER: "The command header is syntactically correct but not supported by the device.",
            ErrorCode.INVALID_SUFFIX: "A suffix in the command is invalid or incorrectly formatted.",
            ErrorCode.CHARACTER_DATA_NOT_ALLOWED: "Character data was received where it is not permitted.",
            ErrorCode.EXECUTION_ERROR: "The device is in a state that prevents execution of the command.",
            ErrorCode.DATA_OUT_OF_RANGE: "A parameter value is outside the permissible range.",
            ErrorCode.ILLEGAL_PARAMETER_VALUE: "A specific value expected by the command is invalid.",
            ErrorCode.QUERY_INTERRUPTED: "The query was interrupted due to an unexpected condition.",
        }
        return error_descriptions.get(ErrorCode(error_code), f"Unknown Error Code: {error_code}")
