"""Лабораторная 2. Совмещение анимаций и эффектов."""

from __future__ import annotations

import pytest

from tests.helpers.animation_helper import (
    get_running_animations_info,
    select_animation,
    set_animation_speed,
    set_combine,
    start_animation,
    stop_animation,
    wait_for_animation_state,
    wait_for_running_animations,
)
from tests.helpers.session_helper import create_test_session, get_room_state, post_action


# Проверяется запуск Rotate + Pulse через существующий флаг combine.
@pytest.mark.student
@pytest.mark.e2e
def test_rotate_plus_pulse_can_start(animation_page):
    driver = animation_page.driver
    set_combine(driver, True)
    select_animation(driver, "pulse")
    info = wait_for_running_animations(driver, minimum=2)
    assert len(info) >= 2


# Проверяется одновременная активность двух WAAPI-анимаций.
@pytest.mark.student
@pytest.mark.e2e
def test_combined_effects_are_both_active(animation_page):
    driver = animation_page.driver
    set_combine(driver, True)
    start_animation(driver)
    info = wait_for_running_animations(driver, minimum=2)
    assert all(item["playState"] == "running" for item in info)
    durations = {round(item["duration"]) for item in info}
    assert len(durations) >= 2


# Проверяется, что рост скорости уменьшает duration.
@pytest.mark.student
@pytest.mark.e2e
def test_combined_effects_change_speed(animation_page):
    driver = animation_page.driver
    set_combine(driver, True)
    set_animation_speed(driver, 1.0)
    start_animation(driver)
    before = wait_for_running_animations(driver, minimum=2)
    set_animation_speed(driver, 2.0)
    after = wait_for_running_animations(driver, minimum=2)
    assert min(item["duration"] for item in after) < min(item["duration"] for item in before)


# Проверяется остановка без остаточной активности.
@pytest.mark.student
@pytest.mark.e2e
def test_combined_effects_stop_cleanly(animation_page):
    driver = animation_page.driver
    set_combine(driver, True)
    start_animation(driver)
    wait_for_running_animations(driver, minimum=2)
    stop_animation(driver)
    wait_for_animation_state(driver, False)
    assert get_running_animations_info(driver) == []


# Проверяется повторный запуск комбинации.
@pytest.mark.student
@pytest.mark.e2e
def test_combined_effects_can_restart(animation_page):
    driver = animation_page.driver
    set_combine(driver, True)
    start_animation(driver)
    stop_animation(driver)
    wait_for_animation_state(driver, False)
    start_animation(driver)
    info = wait_for_running_animations(driver, minimum=2)
    assert len(info) >= 2


# Проверяется независимость эффектов у разных пользователей комнаты.
@pytest.mark.student
@pytest.mark.e2e
def test_effects_are_independent_for_two_users(app_server, animation_page, lab_config):
    driver = animation_page.driver
    set_combine(driver, True)
    start_animation(driver)
    other = create_test_session(app_server["url"], "other-user")
    post_action(
        app_server["url"],
        other["userId"],
        "animation",
        "выбрал анимацию Slide",
        {"selectedKey": "slide", "combine": False, "playing": True, "speed": 1},
    )
    room = get_room_state(app_server["url"])
    states = {user["name"]: user["state"] for user in room["users"]}
    assert states[animation_page.user_name]["combine"] is True
    assert states["other-user"]["combine"] is False
    assert states["other-user"]["selectedKey"] == "slide"
