"""Лабораторная 6. Наблюдаемость событий."""

from __future__ import annotations

import pytest


@pytest.mark.student
@pytest.mark.observability
@pytest.mark.skip(reason="TODO: implement test")
def test_registered_join_event(animation_page, app_server):
    # TODO 1: Прочитать /api/room feed.
    # TODO 2: Найти событие type=join для текущего пользователя.
    pass


@pytest.mark.student
@pytest.mark.observability
@pytest.mark.skip(reason="TODO: implement test")
def test_event_sequence_start_stop(animation_page, app_server):
    # TODO 1: Запустить и остановить анимацию.
    # TODO 2: Проверить порядок событий в ленте.
    pass


@pytest.mark.student
@pytest.mark.observability
@pytest.mark.skip(reason="TODO: implement test")
def test_sse_events_match_actions(animation_page, app_server):
    # TODO 1: Открыть SSE-клиент.
    # TODO 2: Изменить скорость.
    # TODO 3: Дождаться события type=action/feed.
    pass


@pytest.mark.student
@pytest.mark.observability
@pytest.mark.skip(reason="TODO: implement test")
def test_missing_model_error_is_not_in_server_feed(animation_page, app_server):
    # TODO 1: Вызвать ошибку загрузки модели.
    # TODO 2: Проверить, что серверный feed не содержит такого события.
    # TODO 3: Это не дефект, если контракт его не описывает.
    pass


@pytest.mark.student
@pytest.mark.observability
@pytest.mark.skip(reason="TODO: implement test")
def test_failed_http_request_observability(app_server):
    # TODO 1: Отправить заведомо неверный /api/join.
    # TODO 2: Проверить, появилось ли событие в логах и feed.
    pass


@pytest.mark.student
@pytest.mark.observability
@pytest.mark.skip(reason="TODO: implement test")
def test_build_event_coverage_table(animation_page, app_server, reports_dir):
    # TODO 1: Пройти сценарии из lab/EVENTS.md.
    # TODO 2: Собрать таблицу UI / SSE / server logs / обнаружено.
    # TODO 3: Сохранить CSV в reports/.
    pass
