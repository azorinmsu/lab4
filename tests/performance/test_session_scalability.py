"""Лабораторная 5. Производительность при росте числа сессий."""

from __future__ import annotations

import time

import pytest
import requests

from tests.helpers.chart_helper import plot_session_scalability
from tests.helpers.event_helper import SseClient
from tests.helpers.metrics_helper import Measurement, measure_duration, save_measurements
from tests.helpers.session_helper import create_test_session, post_action, reset_room
from tests.helpers.session_helper import get_room_state

USER_COUNTS = (1, 5, 10, 25, 50)


def _fill_users(url: str, count: int) -> list[dict]:
    return [create_test_session(url, f"load-{count}-{index}") for index in range(count)]


# Измеряется latency /api/join при росте числа пользователей.
@pytest.mark.student
@pytest.mark.performance
def test_join_latency_scales_with_users(isolated_room):
    rows = []
    for count in USER_COUNTS:
        reset_room(isolated_room["url"])
        for index in range(count):
            _session, ms = measure_duration(lambda: create_test_session(isolated_room["url"]))
            rows.append(Measurement(scenario="join", users=count, repetition=index + 1, duration_ms=ms))
    assert {row.users for row in rows} == set(USER_COUNTS)
    save_measurements(rows, "join-latency.csv")


# Измеряются /api/action и /api/room для каждой группы.
@pytest.mark.student
@pytest.mark.performance
def test_action_and_room_latency(isolated_room):
    rows = []
    for count in USER_COUNTS:
        reset_room(isolated_room["url"])
        users = _fill_users(isolated_room["url"], count)
        _room, room_ms = measure_duration(lambda: get_room_state(isolated_room["url"]))
        rows.append(Measurement(scenario="room", users=count, duration_ms=room_ms))
        _action, action_ms = measure_duration(
            lambda: post_action(isolated_room["url"], users[0]["userId"], "speed", "изменил скорость на x1.0", {"speed": 1})
        )
        rows.append(Measurement(scenario="action", users=count, duration_ms=action_ms))
    assert len(rows) == len(USER_COUNTS) * 2


# Измеряется задержка доставки SSE на одном клиенте.
@pytest.mark.student
@pytest.mark.performance
def test_sse_delivery_delay(isolated_room):
    rows = []
    for count in (1, 10, 25):
        reset_room(isolated_room["url"])
        users = _fill_users(isolated_room["url"], count)
        client = SseClient(isolated_room["url"]).start()
        sent = time.time() * 1000.0
        post_action(isolated_room["url"], users[0]["userId"], "start", "запустил анимацию")
        event = client.wait_for(lambda item: item.get("type") in {"action", "feed"}, timeout=5)
        client.stop()
        delay = (event["_received_ts"] - sent) if event else 0
        rows.append(Measurement(scenario="sse", users=count, duration_ms=delay, status="ok" if event else "error"))
    assert all(row.status == "ok" for row in rows)


# Считаются throughput и доля ошибок.
@pytest.mark.student
@pytest.mark.performance
def test_throughput_and_errors(isolated_room):
    reset_room(isolated_room["url"])
    session = create_test_session(isolated_room["url"], "bench")
    started = time.perf_counter()
    ok = 0
    errors = 0
    for _ in range(40):
        try:
            get_room_state(isolated_room["url"])
            post_action(isolated_room["url"], session["userId"], "ping-like", "обновил состояние", {"speed": 1})
            ok += 1
        except requests.RequestException:
            errors += 1
    elapsed = time.perf_counter() - started
    throughput = ok / elapsed
    error_rate = 100.0 * errors / max(1, ok + errors)
    rows = [
        Measurement(scenario="throughput", users=1, duration_ms=throughput, extras={"ops": ok}),
        Measurement(scenario="errors", users=1, duration_ms=error_rate, extras={"errors": errors}),
    ]
    save_measurements(rows, "throughput-errors.csv")
    assert throughput > 0


# Сохраняются сравнительные графики масштабируемости.
@pytest.mark.student
@pytest.mark.performance
def test_save_scalability_charts(isolated_room, reports_dir):
    rows: list[Measurement] = []
    for count in USER_COUNTS:
        reset_room(isolated_room["url"])
        started = time.perf_counter()
        users = _fill_users(isolated_room["url"], count)
        elapsed = time.perf_counter() - started
        rows.append(Measurement(scenario="join", users=count, duration_ms=(elapsed / count) * 1000))
        _room, room_ms = measure_duration(lambda: get_room_state(isolated_room["url"]))
        rows.append(Measurement(scenario="room", users=count, duration_ms=room_ms))
        rows.append(Measurement(scenario="throughput", users=count, duration_ms=count / max(elapsed, 1e-6)))
        rows.append(Measurement(scenario="errors", users=count, duration_ms=0.0, status="ok"))
        client = SseClient(isolated_room["url"]).start()
        sent = time.time() * 1000.0
        post_action(isolated_room["url"], users[0]["userId"], "start", "запустил анимацию")
        event = client.wait_for(lambda item: item.get("type") in {"action", "feed"}, timeout=5)
        client.stop()
        rows.append(
            Measurement(
                scenario="sse",
                users=count,
                duration_ms=(event["_received_ts"] - sent) if event else 0,
                status="ok" if event else "error",
            )
        )
    save_measurements(rows, "session-scalability.csv")
    charts = plot_session_scalability(rows)
    assert all(path.exists() for path in charts)


@pytest.mark.load
@pytest.mark.student
def test_optional_one_hundred_users(isolated_room):
    reset_room(isolated_room["url"])
    users = _fill_users(isolated_room["url"], 100)
    room = get_room_state(isolated_room["url"])
    assert len(users) == 100
    assert len(room["users"]) == 100
