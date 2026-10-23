"""Лабораторная 7. Производительность поиска фона и заставки."""

from __future__ import annotations

import pytest


@pytest.mark.student
@pytest.mark.performance
@pytest.mark.skip(reason="TODO: implement test")
def test_measure_background_search_time(animation_page):
    # TODO 1: Измерить время успешного поиска фона.
    # TODO 2: Разделить каталог, HTTP-проверку и отображение, если возможно.
    pass


@pytest.mark.student
@pytest.mark.performance
@pytest.mark.skip(reason="TODO: implement test")
def test_measure_screensaver_search_time(animation_page):
    # TODO 1: Измерить поиск заставки aurora.
    pass


@pytest.mark.student
@pytest.mark.performance
@pytest.mark.skip(reason="TODO: implement test")
def test_compare_search_success_and_failure(animation_page):
    # TODO 1: Сравнить длительность успешного и неуспешного поиска.
    pass


@pytest.mark.student
@pytest.mark.performance
@pytest.mark.skip(reason="TODO: implement test")
def test_search_under_active_effects(animation_page):
    # TODO 1: Измерить поиск при Pulse и при Rotate + Pulse.
    # TODO 2: Сохранить сравнение.
    pass


@pytest.mark.student
@pytest.mark.performance
@pytest.mark.skip(reason="TODO: implement test")
def test_search_time_by_users_and_charts(isolated_room, animation_page, reports_dir):
    # TODO 1: Сравнить время поиска при разном числе пользователей комнаты.
    # TODO 2: Построить графики готовыми утилитами.
    pass
