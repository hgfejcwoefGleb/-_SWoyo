"""
Модуль содержит классы ответа и запроса HTTP
к серверу,
а также методы для формирования
запроса/ответа и
его обратное преобразование
в объект класса
"""

import json
from typing import Self


class HttpRequest:
    """
    Класс HTTP запроса к серверу, который формируется по ТЗ,
    включает в себя заголовки:
    auth_b64 - заголовок Authorization
    host - HOST сервера
    path - путь, куда отправляется запрос,
    protocol - протокол HTTP
    content_type - тип данных тела запроса
    тело запроса:
    sender - отправительб
    recipient - получатель,
    message - сообщение
    """

    def __init__(
        self,
        auth_b64: str,
        host: str,
        sender: str,
        recipient: str,
        message: str,
        path: str,
        protocol: str,
        content_type: str,
    ):
        self.path = path
        self.protocol = protocol
        self.body_bytes = json.dumps(
            {"sender": sender, "recipient": recipient, "message": message}
        ).encode()
        self.auth_b64 = auth_b64
        self.host = host
        self.content_type = content_type

    def to_bytes(self) -> bytes:
        """
        Создает HTTP запрос из данных,
        сохранённых в экземпляре класса
        """
        headers: list[str] = [
            f"POST {self.path} {self.protocol}\r\n"
            f"Host: {self.host}\r\n"
            f"Authorization: Basic {self.auth_b64}\r\n"
            f"Content-Type: {self.content_type}\r\n"
            f"Content-Length: {len(self.body_bytes)}\r\n"
            "\r\n"
        ]
        return ("".join(headers)).encode() + self.body_bytes

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> Self:
        """
        Преобразует последовательность байт в объект HTTP-запроса
        """
        http_parts: list[str] = binary_data.decode().split("\r\n")
        headers: dict[str, str] = {
            "post": "",
            "host": "",
            "authorization": "",
            "content-type": "",
        }
        http_parts_low: list[str] = list(map(lambda x: x.lower(), http_parts))
        body: dict[str, str] = {}
        path: str = ""
        protocol: str = ""
        for header in headers:
            for i, part in enumerate(http_parts_low):
                if header in part and header != "post":
                    headers[header] = http_parts[i].split(" ")[-1]
                elif header in part and header == "post":
                    start_str: list[str] = http_parts[i].split(" ")
                    path = start_str[1]
                    protocol = start_str[2]
                elif part == "":
                    body = json.loads(http_parts[i + 1])
                    break
        return cls(
            auth_b64=headers["authorization"],
            host=headers["host"],
            sender=body["sender"],
            recipient=body["recipient"],
            message=body["message"],
            path=path,
            protocol=protocol,
            content_type=headers["content-type"],
        )


class HttpResponse:
    """
    Класс HTTP ответа от сервера, который формируется по ТЗ,
    включает в себя заголовки:
    acc_control_allow_origin - указывающий,
        какие домены могут получать доступ к ресурсу
    acc_control_allow_headers - указывающий,
        какие HTTP-заголовки могут быть использованы при запросе
    acc_control_allow_cred - указывающий,
        могут ли быть переданы учетные данные
    acc_control_expose_headers указывающий,
        какие заголовки могут быть доступны клиенту
    content_type - тип данных тела ответа
    date - дата и время формирования ответа в формате RFC 7231 (например, "Mon, 23 Oct 2023 12:34:56 GMT").
    connection - управляющий соединением
    keep_alive - указывающий параметры для поддержания соединения
    тело запроса:
    при успешном выполнении:
    status, message_id
    при неуспешном выполнении:
    error
    """

    def __init__(
        self,
        protocol: str,
        answer_code: str,
        acc_control_allow_origin: str,
        acc_control_allow_headers: str,
        acc_control_allow_cred: str,
        acc_control_expose_headers: str,
        content_type: str,
        connection: str,
        keep_alive: str,
        body: str,
    ):
        self.protocol = protocol
        self.answer_code = answer_code
        self.acc_control_allow_origin = acc_control_allow_origin
        self.acc_control_allow_headers = acc_control_allow_headers
        self.acc_control_allow_cred = acc_control_allow_cred
        self.acc_control_expose_headers = acc_control_expose_headers
        self.content_type = content_type
        self.connection = connection
        self.keep_alive = keep_alive
        self.body_bytes = body.encode()

    def to_bytes(self) -> bytes:
        """
        Создает HTTP ответ из данных,
        сохранённых в экземпляре класса
        """
        headers: list[str] = [
            f"{self.protocol} {self.answer_code}\r\n"
            f"Access-Control-Allow-Origin: {self.acc_control_allow_origin}\r\n"
            f"Access-Control-Allow-Headers: {self.acc_control_allow_headers}\r\n"
            f"Access-Control-Allow-Credentials: {self.acc_control_allow_cred}\r\n"
            f"Access-Control-Expose-Headers: {self.acc_control_expose_headers}\r\n"
            f"Content-Type: {self.content_type}\r\n"
            f"Content-Length: {len(self.body_bytes)}\r\n"
            f"Connection: {self.connection}\r\n"
            f"Keep-Alive: {self.keep_alive}\r\n"
            f"\r\n"
        ]
        return ("".join(headers)).encode() + self.body_bytes

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> Self:
        """
        Преобразует последовательность байт в объект HTTP-ответа
        """
        http_parts: list[str] = binary_data.decode().split("\r\n")
        headers: dict[str, str] = {
            "access-control-allow-origin": "",
            "access-control-allow-headers": "",
            "access-control-allow-credentials": "",
            "access-control-expose-headers": "",
            "content-type": "",
            "content-length": "",
            "connection": "",
            "keep-alive": "",
        }
        http_parts_low: list[str] = list(map(lambda x: x.lower(), http_parts))
        body: str = ""
        answer_code: str = ""
        protocol: str = ""
        for header in headers:
            for i, part in enumerate(http_parts_low):
                if header in part and i != 0:
                    headers[header] = http_parts[i].split(":")[-1][1:]
                elif i == 0:
                    start_str: list[str] = http_parts[i].split()
                    # print(f"{start_str} is start_str\n")
                    answer_code = start_str[1] + " " + start_str[2]
                    protocol = start_str[0]
                elif part == "":
                    body = http_parts[i + 1]
                    break
        return cls(
            protocol=protocol,
            answer_code=answer_code,
            acc_control_allow_origin=headers["access-control-allow-origin"],
            acc_control_allow_headers=headers["access-control-allow-headers"],
            acc_control_allow_cred=headers["access-control-allow-credentials"],
            acc_control_expose_headers=headers["access-control-expose-headers"],
            content_type=headers["content-type"],
            connection=headers["connection"],
            keep_alive=headers["keep-alive"],
            body=body,
        )
