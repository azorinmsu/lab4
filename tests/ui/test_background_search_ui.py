"""Лабораторная 7. Функциональные проверки поиска фона и заставки."""

from __future__ import annotations

import pytest


@pytest.mark.student
@pytest.mark.ui
@pytest.mark.skip(reason="TODO: implement test")
def test_successful_background_search(animation_page):
    # TODO 1: Ввести запрос sunset.
    # TODO 2: Вызвать поиск фона.
    # TODO 3: Проверить статус и наличие совпадения.
    pass


@pytest.mark.student
@pytest.mark.ui
@pytest.mark.skip(reason="TODO: implement test")
def test_unsuccessful_background_search(animation_page):
    # TODO 1: Ввести запрос, которого нет в каталоге.
    # TODO 2: Проверить отсутствие результата.
    pass


@pytest.mark.student
@pytest.mark.ui
@pytest.mark.skip(reason="TODO: implement test")
def test_background_collisions(animation_page):
    # TODO 1: Найти запрос с несколькими совпадениями (sunset).
    # TODO 2: Проверить, что метод обрабатывает коллизию предсказуемо.
    pass


@pytest.mark.student
@pytest.mark.ui
@pytest.mark.skip(reason="TODO: implement test")
def test_broken_and_missing_images(animation_page):
    # TODO 1: Искать broken и missing.
    # TODO 2: Повреждённые и недоступные изображения не должны применяться.
    pass
