"""Лабораторная 4. Длительность одного цикла анимации."""

from __future__ import annotations

import pytest

from tests.helpers.animation_helper import (
    select_animation,
    set_animation_speed,
    set_combine,
    start_animation,
    wait_for_running_animations,
)
from tests.helpers.chart_helper import plot_animation_cycle_comparison
from tests.helpers.metrics_helper import (
    Measurement,
    calculate_statistics,
    collect_cycle_measurements,
    measure_animation_cycle,
    save_measurements,
)


def _prepare(page, key: str, speed: float, combine: bool = False):
    set_combine(page.driver, combine)
    set_animation_speed(page.driver, speed)
    select_animation(page.driver, key)
    start_animation(page.driver)
    wait_for_running_animations(page.driver, minimum=2 if combine else 1)


# Измеряется один цикл Pulse на скорости 1.0.
@pytest.mark.student
@pytest.mark.performance
def test_measure_pulse_cycle(animation_page):
    _prepare(animation_page, "pulse", 1.0)
    sample = measure_animation_cycle(animation_page.driver)
    assert sample["durationMs"] > 200


# Измеряется один цикл Rotate без учёта запуска браузера.
@pytest.mark.student
@pytest.mark.performance
def test_measure_rotate_cycle(animation_page):
    _prepare(animation_page, "rotate", 1.0)
    sample = measure_animation_cycle(animation_page.driver)
    assert sample["durationMs"] > 500


# Измеряются циклы Slide, Fade и Bounce.
@pytest.mark.student
@pytest.mark.performance
def test_measure_slide_fade_bounce(animation_page):
    rows: list[Measurement] = []
    for key in ("slide", "fade", "bounce"):
        _prepare(animation_page, key, 1.0)
        rows.extend(collect_cycle_measurements(animation_page.driver, 1, key, key, 1.0))
    assert all(row.duration_ms > 200 for row in rows)


# Измеряется Pulse на поддерживаемых скоростях 0.5, 1.0, 2.0, 3.0.
@pytest.mark.student
@pytest.mark.performance
def test_measure_cycles_at_supported_speeds(animation_page):
    rows = []
    for speed in (0.5, 1.0, 2.0, 3.0):
        _prepare(animation_page, "pulse", speed)
        rows.extend(collect_cycle_measurements(animation_page.driver, 2, "pulse-speed", "pulse", speed))
    fast = [row.duration_ms for row in rows if row.speed == 3.0]
    slow = [row.duration_ms for row in rows if row.speed == 0.5]
    assert calculate_statistics(fast)["median"] < calculate_statistics(slow)["median"]


# Измеряются отдельные циклы Rotate и Pulse в комбинации.
@pytest.mark.student
@pytest.mark.performance
def test_measure_combined_rotate_pulse(animation_page):
    _prepare(animation_page, "slide", 1.0, combine=True)
    first = measure_animation_cycle(animation_page.driver, 0)
    second = measure_animation_cycle(animation_page.driver, 1)
    assert first["durationMs"] > 200
    assert second["durationMs"] > 200


# Сохраняются CSV, статистика и сравнительные графики.
@pytest.mark.student
@pytest.mark.performance
def test_save_cycle_csv_and_charts(animation_page, reports_dir):
    rows: list[Measurement] = []
    for key in ("pulse", "rotate", "slide", "fade", "bounce"):
        _prepare(animation_page, key, 1.0)
        rows.extend(collect_cycle_measurements(animation_page.driver, 1, "single", key, 1.0))
    for speed in (0.5, 1.0, 2.0, 3.0):
        _prepare(animation_page, "pulse", speed)
        rows.extend(collect_cycle_measurements(animation_page.driver, 1, "speed", "pulse", speed))
    _prepare(animation_page, "pulse", 1.0, combine=True)
    rows.extend(collect_cycle_measurements(animation_page.driver, 1, "combine", "pulse", 1.0, 0))
    rows.extend(collect_cycle_measurements(animation_page.driver, 1, "combine", "rotate", 1.0, 1))
    stats = calculate_statistics(row.duration_ms for row in rows)
    assert stats["count"] >= 10
    path = save_measurements(rows, "animation-cycles.csv")
    charts = plot_animation_cycle_comparison(rows)
    assert path.exists()
    assert all(chart.exists() for chart in charts)
