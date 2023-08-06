#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime


from django.conf import settings

from m3_legacy.middleware import get_thread_data


def ms_from_timedelta(td):
    """
    Получает дельту, возвращает миллисекунды
    """
    return (td.seconds * 1000) + (td.microseconds / 1000.0)


@contextmanager
def calc_sql_time(cursor):
    """
    Контекстный менеджер для подсчета времени выполнения SQL-запроса
    :param cursor: курсок к БД
    """
    start = datetime.now()

    yield

    request_uuid = getattr(
        get_thread_data(), 'production_request_uuid', None)
    if request_uuid:
        if not hasattr(cursor.db, 'sql_time'):
            cursor.db.sql_time = defaultdict(float)

        duration = ms_from_timedelta(datetime.now() - start)
        cursor.db.sql_time[request_uuid] += duration


def get_client_ip(request):
    """
    Возвращает IP-адрес клиента, от которого пришел запрос
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')

    return ip


def register_logger(
        lname, log_file=None, log_level=logging.INFO, formatter=None):
    """
    Регистрирует логгер
    """
    log_file = log_file or u'{0}.log'.format(lname)
    log_dir = settings.LOG_PATH
    log_path = os.path.join(log_dir, log_file)

    if formatter is None:
        formatter = logging.Formatter(
            "\n%(pathname)s:%(lineno)d\n[%(asctime)s] %(levelname)s: "
            "%(message)s")
    formatter.datefmt = '%Y-%m-%d %H:%M:%S'

    l = logging.getLogger(lname)
    l.setLevel(log_level)

    # Защита от reload()
    if not l.handlers:
        handler = TimedRotatingFileHandler(
            log_path, when='D', encoding='utf-8')
        handler.setFormatter(formatter)
        l.addHandler(handler)

    return l

