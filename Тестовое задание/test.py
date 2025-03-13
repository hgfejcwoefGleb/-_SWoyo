"""Модуль содержит функции для тестирования
выполненного задания"""
import sys
from unittest.mock import patch, MagicMock
from classes import HttpRequest
from classes import HttpResponse
from take_config import read_conf
from take_config import get_script_args
from main import make_request_to_serv



def test_http_request_creation():
    """Проверка создания объекта HttpRequest."""
    request = HttpRequest(
        auth_b64="dXNlcjpwYXNz",
        host="example.com",
        sender="12345",
        recipient="67890",
        message="Hello",
        path="/send",
        protocol="HTTP/1.1",
        content_type="application/json",
    )
    assert request.auth_b64 == "dXNlcjpwYXNz"
    assert request.host == "example.com"
    assert (
        request.body_bytes
        == b'{"sender": "12345", "recipient": "67890", "message": "Hello"}'
    )
    assert request.path == "/send"
    assert request.protocol == "HTTP/1.1"
    assert request.content_type == "application/json"


def test_http_request_to_bytes():
    """Проверка преобразования HttpRequest в байты."""
    request = HttpRequest(
        auth_b64="dXNlcjpwYXNz",
        host="example.com",
        sender="12345",
        recipient="67890",
        message="Hello",
        path="/send",
        protocol="HTTP/1.1",
        content_type="application/json",
    )
    request_bytes = request.to_bytes()
    assert isinstance(request_bytes, bytes)
    assert b"POST /send HTTP/1.1" in request_bytes
    assert b"Host: example.com" in request_bytes
    assert b"Authorization: Basic dXNlcjpwYXNz" in request_bytes


def test_http_request_from_bytes():
    """Проверка создания HttpRequest из байтов."""
    request_bytes = (
        b"POST /send HTTP/1.1\r\n"
        b"Host: example.com\r\n"
        b"Authorization: Basic dXNlcjpwYXNz\r\n"
        b"Content-Type: application/json\r\n"
        b"Content-Length: 36\r\n"
        b"\r\n"
        b'{"sender": "12345", "recipient": "67890", "message": "Hello"}'
    )
    request = HttpRequest.from_bytes(request_bytes)
    assert request.auth_b64 == "dXNlcjpwYXNz"
    assert request.host == "example.com"
    assert (
        request.body_bytes
        == b'{"sender": "12345", "recipient": "67890", "message": "Hello"}'
    )
    assert request.path == "/send"
    assert request.protocol == "HTTP/1.1"
    assert request.content_type == "application/json"


def test_http_response_creation():
    """Проверка создания объекта HttpResponse."""
    response = HttpResponse(
        protocol="HTTP/1.1",
        answer_code="200 OK",
        acc_control_allow_origin="*",
        acc_control_allow_headers="Content-Type",
        acc_control_allow_cred="true",
        acc_control_expose_headers="Content-Length",
        content_type="application/json",
        connection="keep-alive",
        keep_alive="timeout=5, max=100",
        body='{"status": "success", "message_id": "12345"}',
    )
    assert response.protocol == "HTTP/1.1"
    assert response.answer_code == "200 OK"
    assert response.acc_control_allow_origin == "*"
    assert response.acc_control_allow_headers == "Content-Type"
    assert response.acc_control_allow_cred == "true"
    assert response.acc_control_expose_headers == "Content-Length"
    assert response.content_type == "application/json"
    assert response.connection == "keep-alive"
    assert response.keep_alive == "timeout=5, max=100"
    assert response.body_bytes == b'{"status": "success", "message_id": "12345"}'


def test_http_response_to_bytes():
    """Проверка преобразования HttpResponse в байты."""
    response = HttpResponse(
        protocol="HTTP/1.1",
        answer_code="200 OK",
        acc_control_allow_origin="*",
        acc_control_allow_headers="Content-Type",
        acc_control_allow_cred="true",
        acc_control_expose_headers="Content-Length",
        content_type="application/json",
        connection="keep-alive",
        keep_alive="timeout=5, max=100",
        body='{"status": "success", "message_id": "12345"}',
    )
    response_bytes = response.to_bytes()
    assert isinstance(response_bytes, bytes)
    assert b"HTTP/1.1 200 OK" in response_bytes
    assert b"Access-Control-Allow-Origin: *" in response_bytes
    assert b"Content-Type: application/json" in response_bytes
    assert b'{"status": "success", "message_id": "12345"}' in response_bytes


def test_http_response_from_bytes():
    """Проверка создания HttpResponse из байтов."""
    response_bytes = (
        b"HTTP/1.1 200 OK\r\n"
        b"Access-Control-Allow-Origin: *\r\n"
        b"Access-Control-Allow-Headers: Content-Type\r\n"
        b"Access-Control-Allow-Credentials: true\r\n"
        b"Access-Control-Expose-Headers: Content-Length\r\n"
        b"Content-Type: application/json\r\n"
        b"Content-Length: 36\r\n"
        b"Date: Mon, 23 Oct 2023 12:34:56 GMT\r\n"
        b"Connection: keep-alive\r\n"
        b"Keep-Alive: timeout=5, max=100\r\n"
        b"\r\n"
        b'{"status": "success", "message_id": "12345"}'
    )
    response = HttpResponse.from_bytes(response_bytes)
    assert response.protocol == "HTTP/1.1"
    assert response.answer_code == "200 OK"
    assert response.acc_control_allow_origin == "*"
    assert response.acc_control_allow_headers == "Content-Type"
    assert response.acc_control_allow_cred == "true"
    assert response.acc_control_expose_headers == "Content-Length"
    assert response.content_type == "application/json"
    assert response.connection == "keep-alive"
    assert response.keep_alive == "timeout=5, max=100"
    assert response.body_bytes == b'{"status": "success", "message_id": "12345"}'


def test_read_conf(tmp_path):
    """Проверка чтения TOML-файла."""
    config_content = """
    [test_sms_sender]
    user = "test_user"
    password = "test_password"
    server_url = "example.com"
    """
    config_file = tmp_path / "test_config.toml"
    config_file.write_text(config_content)
    config = read_conf(str(config_file))
    assert config["test_sms_sender"]["user"] == "test_user"
    assert config["test_sms_sender"]["password"] == "test_password"
    assert config["test_sms_sender"]["server_url"] == "example.com"


def test_get_script_args():
    """Проверка парсинга аргументов командной строки."""
    sys.argv = ["script.py", "sender", "recipient", "message"]
    args = get_script_args(
        ["sender", "recipient", "message"],
        ["Описание sender", "Описание recipient", "Описание message"],
        "Описание парсера",
    )
    assert args.sender == "sender"
    assert args.recipient == "recipient"
    assert args.message == "message"


@patch("socket.socket")
@patch("main.conf.get_script_args")
def test_make_request_to_serv_success(mock_get_script_args, mock_socket):
    """Проверка успешного запроса к серверу."""
    mock_get_script_args.return_value = MagicMock(
        sender="12345", recipient="67890", message="Hello"
    )
    mock_socket.return_value.recv.return_value = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: application/json\r\n"
        b"\r\n"
        b'{"status": "success", "message_id": "12345"}'
    )
    with patch("logging.info") as mock_logging:
        make_request_to_serv("localhost", 4010)
        mock_logging.assert_called_with("Server response: %s", "200 OK")


@patch("socket.socket")
@patch("main.conf.get_script_args")
def test_make_request_to_serv_connection_refused(mock_get_script_args, mock_socket):
    """Проверка обработки ошибки ConnectionRefusedError."""
    mock_get_script_args.return_value = MagicMock(
        sender="12345", recipient="67890", message="Hello"
    )
    mock_socket.return_value.connect.side_effect = ConnectionRefusedError
    with patch("logging.error") as mock_logging:
        make_request_to_serv("localhost", 4010)
        mock_logging.assert_called_with(
            "Error: The connection was not established because the server rejected the request"
        )
