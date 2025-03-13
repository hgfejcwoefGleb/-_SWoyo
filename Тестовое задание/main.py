"""
Этот модуль содержит функцию по отправке запроса
к серверу и ее вызов, включая логирование результатов
"""

import argparse
import socket
import base64
import logging
import classes as cls
import take_config as conf
from classes import HttpResponse, HttpRequest


def make_request_to_serv(server_name: str, port: int) -> None:
    """
    Функция выполняет подключение, запрос к серверу, а также логирует резултат
    В конце функкции выводится код ответа и текста ответа сервера
    :param server_name:
    :param port:
    :return: None
    """
    try:
        logging.basicConfig(
            level=logging.INFO,
            filename="server.log",
            format="%(asctime)s %(levelname)s %(message)s",
        )
        config: dict[str, dict[str, str]] = conf.read_conf("conf.toml")

        args: argparse.Namespace = conf.get_script_args(
            ["sender", "recipient", "message"],
            ["Номер отправителя СМС", "Номер получателя СМС", "Текст СМС"],
            "Сервис по отправке смс сообщений",
        )
        logging.info(
            "Sender: %s, Recipient: %s, Message: %s",
            args.sender,
            args.recipient,
            args.message,
        )
        auth_str: str = (
            f"{config['test_sms_sender']['user']}:{config['test_sms_sender']['password']}"
        )
        auth_b64: str = base64.b64encode(auth_str.encode()).decode()
        http_req: HttpRequest = cls.HttpRequest(
            auth_b64,
            config["test_sms_sender"]["server_url"],
            args.sender,
            args.recipient,
            args.message,
            "/send_sms",
            "HTTP/1.1",
            "application/json",
        )
        res: bytes = http_req.to_bytes()
        sock = socket.socket()
        sock.connect((server_name, port))
        sock.send(res)
        data: bytes = sock.recv(1024)
        sock.close()
        # new_http_req = HttpRequest.from_bytes(res)
        # new_res = new_http_req.to_bytes()
        # print(new_res)
        # print(data.decode().split('\r\n'))
        https_resp: HttpResponse = HttpResponse.from_bytes(data)
        # resp = https_resp.to_bytes()
        logging.info("Server response: %s", https_resp.answer_code)
        print(https_resp.answer_code)
    except ConnectionRefusedError:
        logging.error(
            "Error: The connection was not established because the server rejected the request"
        )
        print(
            "Error: The connection was not established because the server rejected the request"
        )
    # except Exception as e:
    # print(f"Найдена ошибка: {e}")


if __name__ == "__main__":
    make_request_to_serv("localhost", 4010)
