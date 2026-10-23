"""Лабораторная 3. Отрисовка 2D и 3D."""

from __future__ import annotations

import pytest
from selenium.webdriver.common.by import By

from tests.helpers.animation_helper import (
    capture_model_screenshot,
    get_computed_transform,
    get_element_bounds,
    select_animation,
    set_3d,
    start_animation,
)
from tests.helpers.browser_helper import set_window_size, wait_for_condition
from tests.helpers.model_helper import is_3d_visible


def _shape_visible(driver) -> bool:
    display = driver.find_element(By.ID, "shape").value_of_css_property("display")
    return display != "none" and not is_3d_visible(driver)


# Проверяется видимость 2D-фигуры при выключенном 3D.
@pytest.mark.student
@pytest.mark.ui
def test_2d_model_is_visible(animation_page):
    set_3d(animation_page.driver, False)
    wait_for_condition(animation_page.driver, _shape_visible)
    assert not is_3d_visible(animation_page.driver)


# Проверяется переключение модели в 3D.
@pytest.mark.student
@pytest.mark.ui
def test_switch_to_3d(animation_page):
    set_3d(animation_page.driver, True)
    wait_for_condition(animation_page.driver, is_3d_visible)
    assert is_3d_visible(animation_page.driver)


# Проверяется наличие 3D-трансформации у куба.
@pytest.mark.student
@pytest.mark.ui
def test_3d_has_transform(animation_page):
    set_3d(animation_page.driver, True)
    wait_for_condition(animation_page.driver, is_3d_visible)
    style = get_computed_transform(animation_page.driver, "#model3d")
    assert style["transform"] not in ("none", "", None)
    assert "matrix" in style["transform"] or "rotate" in style["transform"]


# Проверяется возврат из 3D в 2D.
@pytest.mark.student
@pytest.mark.ui
def test_return_to_2d(animation_page):
    set_3d(animation_page.driver, True)
    wait_for_condition(animation_page.driver, is_3d_visible)
    set_3d(animation_page.driver, False)
    wait_for_condition(animation_page.driver, _shape_visible)
    assert not is_3d_visible(animation_page.driver)


# Проверяется, что фигура и куб не видны одновременно.
@pytest.mark.student
@pytest.mark.ui
def test_no_unexpected_overlap(animation_page, reports_dir):
    set_3d(animation_page.driver, False)
    shape_2d = get_element_bounds(animation_page.driver, "#shape")
    set_3d(animation_page.driver, True)
    wait_for_condition(animation_page.driver, is_3d_visible)
    assert animation_page.driver.find_element(By.ID, "shape").value_of_css_property("display") == "none"
    cube = get_element_bounds(animation_page.driver, "#model3d")
    assert shape_2d["width"] > 0 and cube["width"] > 0


# Проверяется сцена при разных размерах окна.
@pytest.mark.student
@pytest.mark.ui
def test_render_at_different_window_sizes(animation_page):
    driver = animation_page.driver
    for width, height in ((1280, 800), (800, 600)):
        set_window_size(driver, width, height)
        bounds = get_element_bounds(driver, "#stage")
        window = driver.get_window_size()
        assert bounds["width"] > 0
        assert bounds["left"] + bounds["width"] <= window["width"] + 20


# Проверяется, что модель остаётся видимой во время анимации.
@pytest.mark.student
@pytest.mark.ui
def test_model_visible_during_animation(animation_page, reports_dir):
    select_animation(animation_page.driver, "pulse")
    start_animation(animation_page.driver)
    path = capture_model_screenshot(animation_page.driver, str(reports_dir / "pulse-stage.png"))
    bounds = get_element_bounds(animation_page.driver, "#actor")
    assert bounds["width"] > 0 and bounds["height"] > 0
    assert path.endswith(".png")
