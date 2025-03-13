"""
Модуль, который содержит функции по считыванию
TOML файла и аргументов командной строки
"""

import tomllib
import argparse


def read_conf(conf_file: str) -> dict:
    """
    Считывает TOML файл
    :param conf_file:
    :return:
    """
    with open(conf_file, "rb") as conf:
        config = tomllib.load(conf)
    return config


def get_script_args(
    name_args: list, args_descrptns: list, parser_descr: str = ""
) -> argparse.Namespace:
    """
    Считывает и возвращает аргументы командной строки,
    которые были переданы призапуске
    :param name_args:
    :param args_descrptns:
    :param parser_descr:
    :return:
    """
    parser = argparse.ArgumentParser(description=parser_descr)
    for name_arg, args_descrpt in zip(name_args, args_descrptns):
        parser.add_argument(name_arg, type=str, help=args_descrpt)
    return parser.parse_args()
