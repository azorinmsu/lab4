"""Лабораторная 1. E2E-сценарии загрузки моделей."""

from __future__ import annotations

import pytest
from selenium.webdriver.common.by import By

from tests.helpers.animation_helper import start_animation, wait_for_animation_state
from tests.helpers.browser_helper import wait_for_condition
from tests.helpers.model_helper import get_loaded_model_status, get_model_load_error, is_3d_visible
from tests.helpers.session_helper import get_room_state


def _wait_status(driver, text):
    wait_for_condition(driver, lambda d: text.lower() in get_loaded_model_status(d).lower())


# Сквозная загрузка модели через выбранный источник.
@pytest.mark.student
@pytest.mark.e2e
def test_load_model_from_source_end_to_end(animation_page, lab_config):
    animation_page.load_model("http", "slide-square")
    _wait_status(animation_page.driver, "Slide Square")
    assert "Slide Square" in animation_page.driver.find_element(By.ID, "loadedModelName").text


# Загруженная модель появляется на игровом поле.
@pytest.mark.student
@pytest.mark.e2e
def test_loaded_model_appears_on_stage(animation_page):
    animation_page.load_model("local", "cube-3d")
    _wait_status(animation_page.driver, "CSS Cube")
    animation_page.set_3d(True)
    wait_for_condition(animation_page.driver, lambda d: is_3d_visible(d))
    assert is_3d_visible(animation_page.driver)


# После загрузки анимация запускается.
@pytest.mark.student
@pytest.mark.e2e
def test_start_animation_after_load(animation_page):
    animation_page.load_model("local", "pulse-circle")
    _wait_status(animation_page.driver, "Pulse Circle")
    start_animation(animation_page.driver)
    wait_for_animation_state(animation_page.driver, True)


# Сессия и комната остаются живыми после загрузки.
@pytest.mark.student
@pytest.mark.e2e
def test_model_load_visible_in_session_feed(animation_page, app_server):
    animation_page.load_model("local", "fade-circle")
    _wait_status(animation_page.driver, "Fade Circle")
    room = get_room_state(app_server["url"])
    assert any(user["name"] == animation_page.user_name for user in room["users"])
    assert "сессии" in animation_page.session_badge.lower()


# После ошибки можно снова загрузить корректную модель.
@pytest.mark.student
@pytest.mark.e2e
def test_recover_after_failed_load(animation_page, lab_config):
    animation_page.load_model("errors", "pulse-circle")
    wait_for_condition(animation_page.driver, lambda d: get_model_load_error(d) != "")
    animation_page.load_model("local", "rotate-square")
    _wait_status(animation_page.driver, "Rotate Square")
    assert "Rotate Square" in get_loaded_model_status(animation_page.driver)


# Загрузка не разрывает пользовательскую сессию.
@pytest.mark.student
@pytest.mark.e2e
def test_load_model_in_user_session(animation_page, isolated_room):
    assert animation_page.driver.execute_script("return document.body.classList.contains('session-active');")
    animation_page.load_model("cdn", "pulse-circle")
    _wait_status(animation_page.driver, "Pulse Circle")
    assert animation_page.driver.execute_script("return document.body.classList.contains('session-active');")
