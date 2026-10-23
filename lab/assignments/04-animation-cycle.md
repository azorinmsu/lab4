# Лабораторная работа 4. Длительность одного цикла анимации

## Цель

Сравнить длительность одного повторения Pulse, Rotate, Slide, Fade, Bounce и Rotate + Pulse на скоростях 0.5, 1.0, 2.0, 3.0.

## Краткая теория

Один цикл — одно повторение бесконечной анимации, а не ожидание её окончания. Базовые длительности: Pulse 1200, Rotate 3000, Slide 2000, Fade 1500, Bounce 1500 мс, делённые на скорость. У комбинации длительности разные — измеряйте каждый эффект отдельно. Запуск браузера в измерение не входит.

## Что нужно сделать

Реализовать измерения в `tests/performance/test_animation_cycle.py` и построить графики.

## Как это сделать

1. Выбрать эффект и скорость готовыми хелперами.
2. Запустить анимацию и дождаться WAAPI.
3. Вызвать `measure_animation_cycle`.
4. Повторить несколько раз.
5. Для комбинации измерить индекс 0 и индекс 1.
6. Сохранить CSV и вызвать `plot_animation_cycle_comparison`.

## Инструменты

`time.perf_counter` внутри утилит, `performance.now()` в браузере, matplotlib, pandas/CSV.

## Какие файлы редактировать

- `tests/performance/test_animation_cycle.py`

## Рекомендуемые вспомогательные методы

| Метод | Файл | Назначение | Аргументы | Возвращает | Пример |
|---|---|---|---|---|---|
| `measure_animation_cycle` | `metrics_helper.py` | Один цикл уже запущенной анимации | `driver`, `effect_index=0` | dict | `measure_animation_cycle(driver)` |
| `collect_cycle_measurements` | `metrics_helper.py` | Несколько повторений | `driver`, `repeats`, `scenario`, `effect`, `speed` | list | `collect_cycle_measurements(driver, 3, 'pulse', 'pulse', 1.0)` |
| `calculate_statistics` | `metrics_helper.py` | mean/median/p95/stdev | iterable | dict | `calculate_statistics(values)` |
| `save_measurements` | `metrics_helper.py` | CSV в reports/ | rows, filename | Path | `save_measurements(rows, 'cycles.csv')` |
| `plot_animation_cycle_comparison` | `chart_helper.py` | Три графика | rows | list[Path] | `plot_animation_cycle_comparison(rows)` |

## Как запустить тест

```bash
pytest tests/performance/test_animation_cycle.py
```

Полная матрица 6×4 может занять несколько минут: Rotate на 0.5 — около 6 с на цикл.

## Как получить результаты

`reports/*cycle*.csv` и PNG.

## Как построить график

Утилита строит:

1. Длительность по типам эффектов.
2. Длительность от скорости.
3. Одиночные против комбинированных.

## Ожидаемый результат

CSV с повторениями, статистика и три PNG. Более высокая скорость уменьшает цикл.

## Критерии приёмки

Есть измерения всех шести эффектов и четырёх скоростей хотя бы в сводном тесте. Браузер не входит в замер. Есть median, mean, p95 и разброс.

## Дополнительно

Сравнить измеренный цикл с `expected_cycle_ms(key, speed)`.
