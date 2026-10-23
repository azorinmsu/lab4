"""Лабораторная 1. UI-проверки загрузки моделей."""

from __future__ import annotations

import pytest
from selenium.webdriver.common.by import By

from tests.helpers.animation_helper import select_animation, wait_for_animation_state
from tests.helpers.browser_helper import wait_for_condition
from tests.helpers.model_helper import get_loaded_model_status, get_model_load_error, get_shape_class


def _wait_status(driver, text, timeout=8):
    wait_for_condition(driver, lambda d: text.lower() in get_loaded_model_status(d).lower(), timeout)


# Проверяется загрузка CSS-модели из локального каталога.
@pytest.mark.student
@pytest.mark.ui
def test_load_local_model(animation_page, lab_config):
    animation_page.load_model("local", "pulse-circle")
    _wait_status(animation_page.driver, "Pulse Circle")
    assert "Pulse Circle" in animation_page.driver.find_element(By.ID, "loadedModelName").text


# Проверяется загрузка модели по HTTP mock-источнику.
@pytest.mark.student
@pytest.mark.ui
def test_load_http_model(animation_page, lab_config):
    animation_page.load_model("http", "rotate-square")
    _wait_status(animation_page.driver, "Rotate Square")
    assert "square" in get_shape_class(animation_page.driver)


# Проверяется загрузка модели из mock CDN.
@pytest.mark.student
@pytest.mark.ui
def test_load_cdn_model(animation_page, lab_config):
    animation_page.load_model("cdn", "fade-circle")
    _wait_status(animation_page.driver, "Fade Circle")
    assert "circle" in get_shape_class(animation_page.driver)


# Проверяется отображение ошибки недоступного источника.
@pytest.mark.student
@pytest.mark.ui
def test_load_model_error(animation_page, lab_config):
    animation_page.load_model("errors", "pulse-circle")
    wait_for_condition(animation_page.driver, lambda d: get_model_load_error(d) != "", timeout=8)
    assert get_model_load_error(animation_page.driver)


# Проверяется, что загруженная модель видна на сцене.
@pytest.mark.student
@pytest.mark.ui
def test_loaded_model_is_visible(animation_page, lab_config):
    animation_page.load_model("local", "bounce-square")
    _wait_status(animation_page.driver, "Bounce Square")
    assert "square" in get_shape_class(animation_page.driver)
    assert "Bounce Square" in animation_page.driver.find_element(By.ID, "loadedModelName").text


# Проверяется запуск эффекта на уже загруженной модели.
@pytest.mark.student
@pytest.mark.ui
def test_effect_runs_on_loaded_model(animation_page, lab_config):
    animation_page.load_model("local", "pulse-circle")
    _wait_status(animation_page.driver, "Pulse Circle")
    select_animation(animation_page.driver, "pulse")
    wait_for_animation_state(animation_page.driver, True)
    state = animation_page.driver.execute_script("return window.motionGetLocalState();")
    assert state["playing"] is True
    assert state["animationCount"] >= 1
