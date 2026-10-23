"""Лабораторная 8. Скорость скачивания из разных источников."""

from __future__ import annotations

import pytest


@pytest.mark.student
@pytest.mark.performance
@pytest.mark.skip(reason="TODO: implement test")
def test_download_from_local_source(mock_server, lab_config):
    # TODO 1: Скачать payload.bin из локального HTTP-источника.
    # TODO 2: Проверить, что тело получено полностью.
    pass


@pytest.mark.student
@pytest.mark.performance
@pytest.mark.skip(reason="TODO: implement test")
def test_download_from_mock_cdn(mock_server, lab_config):
    # TODO 1: Скачать тот же файл из mock CDN.
    # TODO 2: Сравнить время с локальным источником.
    pass


@pytest.mark.student
@pytest.mark.performance
@pytest.mark.skip(reason="TODO: implement test")
def test_download_with_delay(mock_server, lab_config):
    # TODO 1: Измерить источник delayed.
    pass


@pytest.mark.student
@pytest.mark.performance
@pytest.mark.skip(reason="TODO: implement test")
def test_download_with_throttle(mock_server, lab_config):
    # TODO 1: Измерить источник с ограничением скорости.
    pass


@pytest.mark.student
@pytest.mark.performance
@pytest.mark.skip(reason="TODO: implement test")
def test_download_http_error_and_timeout(mock_server, lab_config):
    # TODO 1: Проверить HTTP-ошибку.
    # TODO 2: Проверить timeout коротким лимитом на delayed URL.
    pass


@pytest.mark.student
@pytest.mark.performance
@pytest.mark.skip(reason="TODO: implement test")
def test_incomplete_download_is_not_success(mock_server, lab_config):
    # TODO 1: Скачать incomplete URL.
    # TODO 2: Не считать загрузку успешной, если тело короче Content-Length.
    pass


@pytest.mark.student
@pytest.mark.performance
@pytest.mark.skip(reason="TODO: implement test")
def test_cold_vs_warm_cache_and_charts(mock_server, lab_config, reports_dir):
    # TODO 1: Измерить холодный и повторный запрос.
    # TODO 2: Посчитать throughput.
    # TODO 3: Сохранить CSV и графики.
    pass
