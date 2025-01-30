from enum import Enum


class ErrorCode(Enum):
    NO_ERROR = 0
    INVALID_CHARACTER = -101
    INVALID_SEPARATOR = -103
    DATA_TYPE_ERROR = -104
    PARAMETER_NOT_ALLOWED = -108
    MISSING_PARAMETER = -109
    COMMAND_HEADER_ERROR = -110
    UNDEFINED_HEADER = -113
    SETTING_CONFLICT = -221
    DATA_OUT_OF_RANGE = -222
    PROGRAM_RUNNING = -284
    DEVICE_SPECIFIC_ERROR = -300
    NOT_MEASUREMENT_MODULE = -301
    QUEUE_OVERFLOW = -350
    QUEUE_EMPTY = -351
    UPP_COMM_HEADER_ERROR = 101
    UPP_COMM_RSP_NO = 103
    UPP_COMM_MODULE_MISMATCHED = 104
    TCPIP_COMM_ERROR = 110
    GPIB_TX_NOT_COMPLETED = 116
    GPIB_TX_TIMER_EXPIRED = 117
    MC_TRIG_ERROR = 120
    SEM_NOT_EXIST = 210

    @staticmethod
    def get_error_description(error_code):
        error_descriptions = {
            ErrorCode.NO_ERROR: "No error",
            ErrorCode.INVALID_CHARACTER: "Invalid character. This occurs when unacceptable characters are received for Command or Parameter. Unacceptable characters: '%', '&', '$', '#', '~'.",
            ErrorCode.INVALID_SEPARATOR: "Invalid separator. This occurs when an unacceptable character is received as a separator between the Command and the Parameter. Unacceptable characters: '`', ';'.",
            ErrorCode.DATA_TYPE_ERROR: "Data type error. This occurs when the Parameter is not an acceptable data type.",
            ErrorCode.PARAMETER_NOT_ALLOWED: "Parameter not allowed. This occurs when the number of parameters in the corresponding command is more or less than expected.",
            ErrorCode.MISSING_PARAMETER: "Missing parameter. This occurs when the number of characters in the Parameter is longer than 18.",
            ErrorCode.COMMAND_HEADER_ERROR: "Command header error. This occurs when the number of characters in the Command is longer than 13.",
            ErrorCode.UNDEFINED_HEADER: "Undefined Header. This occurs when an unsupported command is received.",
            ErrorCode.SETTING_CONFLICT: "Setting conflict. This occurs when one of the following setup commands (other than STOP or STAT?) was received before measurement using 'MEAS' command is completed: AVG, LEV, LOGN, AUTO, WAVE, WMOD, WSET, SPE, LOOP, UNIT.",
            ErrorCode.DATA_OUT_OF_RANGE: "Data out of range. This occurs when the parameter is outside the acceptable value.",
            ErrorCode.PROGRAM_RUNNING: "Program currently running. This occurs when the mainframe delivers new commands to the module before the process of delivering commands to the module and receiving responses is completed.",
            ErrorCode.DEVICE_SPECIFIC_ERROR: "Device specific error. This occurs when the GPIB Address number that you are trying to set exceeds 32.",
            ErrorCode.NOT_MEASUREMENT_MODULE: "Is not Measurement Module. This occurs when user attempts to deliver a command to a module (slot) that is not installed.",
            ErrorCode.QUEUE_OVERFLOW: "Queue overflow. This occurs when the Queue space used for communication between internal Tasks is full, and there is no space to store information.",
            ErrorCode.QUEUE_EMPTY: "Queue empty. This occurs when there is no message in the Queue space used for communication between internal Tasks.",
            ErrorCode.UPP_COMM_HEADER_ERROR: "uPP Comm. Header Error. This occurs when the Headers of the Packet used to send and receive data between the mainframe and the module are different.",
            ErrorCode.UPP_COMM_RSP_NO: "uPP Comm. Rsp No. This occurs when the mainframe sends data information to the module but does not receive a response.",
            ErrorCode.UPP_COMM_MODULE_MISMATCHED: "uPP Comm. Module Mismatched. This occurs when the mainframe receives information from a different module than the one that sent the data.",
            ErrorCode.TCPIP_COMM_ERROR: "TCPIP Comm. Error. This occurs when all data to be transferred is not sent in TCP/IP communication.",
            ErrorCode.GPIB_TX_NOT_COMPLETED: "GPIB Tx not completed. This occurs when no event is delivered to the internal GPIB Task used for GPIB communication.",
            ErrorCode.GPIB_TX_TIMER_EXPIRED: "GPIB Tx Timer Expired. This occurs when all data to be transferred is not sent in GPIB communication.",
            ErrorCode.MC_TRIG_ERROR: "MC Trig. Error. This occurs when the mainframe does not receive a measurement completion signal (H/W signal) from the module after the measurement command was delivered to the module.",
            ErrorCode.SEM_NOT_EXIST: "not exist SEM. This occurs when an unregistered message is delivered between internal tasks.",
        }
        return error_descriptions.get(error_code, "Unknown error")
