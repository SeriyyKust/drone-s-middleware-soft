import enum


class TypePacket(enum.Enum):
    DETECTOR_CONTROL_COMMAND = 2
    SUPPRESSOR_CONTROL_COMMAND = 9
    SPOOFING_CONTROL_COMMAND = 12
    CONFIRMED_FRAME = 18


class TypeResultExecute(enum.Enum):
    OK = 1
    ERROR = 2


class TypeDevice(enum.Enum):
    DETECTOR = 1  # (СРЧО) средства радиочастотного обнаружения (он же Обнаружитель)
    DIRECTION_FINDING = 2  # (РОН) устройство пеленгации
    SUPPRESSOR = 3  # (СРП) средства радиоподавления (он же Подавитель)
    SPOOFING = 4  # (СЛНС) средство ложных навигационных сигналов (он же Имитатор)
    SIMULATOR = 5  # (РЧО) устройство противодействия


class TypeObjectDetected(enum.Enum):
    DRONE = 1  # _("БЛА")
    CONTROLLER = 2  # _("ПУ")
    PLACE_START = 3  # _("МС")


class TypeCommand(enum.Enum):
    TURN_ON = 1  # _("Включить")
    TURN_OF = 2  # _("Выключить")
    NO_COMMAND = 3  # _("Оставить в текущем состоянии")


class TypePower(enum.Enum):
    MAXIMUM = 1  # , _("Максимальная")
    NORMAL = 2  # , _("Обычная")
    REDUCED = 3  # , _("Пониженная")


class TypeSignal(enum.Enum):
    DJI_OcuSync_1 = 1  # , _("Идентифицирован протокол DJI OcuSync 1.0")
    DJI_OcuSync_2 = 2  # , _("Идентифицирован протокол DJI OcuSync 2.0")
    DJI_OcuSync_3 = 3  # , _("Идентифицирован протокол DJI OcuSync 3.0")
    DJI_OcuSync_3_Plus = 4  # , _("Идентифицирован протокол DJI OcuSync 3.0 +")
    DJI_OcuSync_4 = 5  # , _("Идентифицирован протокол DJI OcuSync 4.0")
    DJI_LightBridge_1 = 6  # , _("Идентифицирован протокол DJI LightBridge 1.0")
    DJI_LightBridge_2 = 7  # , _("Идентифицирован протокол DJI LightBridge 2.0")
    Autel_SkyLink_2 = 8  # , _("Идентифицирован протокол Autel SkyLink 2.0")
    Autel_SkyLink_3 = 9  # , _("Идентифицирован протокол Autel SkyLink 3.0")
    Analog_Video = 10  # , _("Идентифицирован протокол Analog Video")
    DJI_DroneID = 51  # , _("Идентифицирован протокол DJI DroneID")
    RemoteID = 52  # , _("Идентифицирован протокол RemoteID")


class TypeSignalDetection(enum.Enum):
    CORRELATION_FUNCTION = 1  # , _("Корреляционная функция")
    NEURAL_NETWORK = 2  # , _("Нейросеть")


class TypeModeRouteMap(enum.Enum):
    POINT = 1  # , _("Точка")
    FORWARD = 2  # , _("Вперед")
    CYCLE = 3  # , _("Цикл")
    PING_PONG = 4  # , _("Пинг-Понг")


class ModeDetectedData(enum.Enum):
    LINE = 1
    CYCLE = 2


class TypeFrame(enum.Enum):
    INFO = "info"
    CONFIRMATION = "confirmation"
    BLOCK_NOTIFICATION = "block_notification"
    ERROR_BLOCK_NOTIFICATION = "error_block_notification"
    GENERAL_NOTIFICATION = "general_notification"


class TypeBlock(enum.Enum):
    DETECTOR = 1
    SUPPRESSOR = 2
    SPOOFING = 3
    DELAY = 4
    ADD_SCRIPT = 5
    RESETTING_SYSTEM = 6
