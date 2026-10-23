/**
 * Студенческие методы лабораторных работ 1 и 7.
 * Основную логику реализует студент. Инфраструктура уже подключена.
 */
(function initStudentApi(global) {
  /**
   * Загружает модель из выбранного источника.
   *
   * TODO:
   * 1. Определить источник.
   * 2. Получить данные модели.
   * 3. Проверить корректность данных.
   * 4. Обработать ошибки.
   * 5. Передать модель в механизм отображения.
   *
   * Рекомендуемые утилиты:
   * - getConfiguredSourceBaseUrl()
   * - fetchModelResource()
   * - validateModelData()
   * - normalizeModelData()
   * - renderLoadedModel()
   * - showModelLoadError()
   */
  async function loadModel(sourceType, modelId) {
    // TODO: Реализовать загрузку.
    throw new Error("Not implemented");
  }

  /**
   * Поиск фонового изображения.
   *
   * TODO:
   * 1. Получить параметры поиска.
   * 2. Получить каталог фонов.
   * 3. Выполнить поиск.
   * 4. Обработать несколько совпадений.
   * 5. Проверить доступность изображения.
   * 6. Вернуть результат или отсутствие результата.
   *
   * Рекомендуемые утилиты:
   * - getBackgroundCatalog()
   * - filterCatalogItems()
   * - checkImageAvailability()
   * - applyStageBackground()
   */
  async function findBackground(query, options) {
    // TODO: Реализовать поиск фона.
    throw new Error("Not implemented");
  }

  /**
   * Поиск заставки.
   *
   * TODO:
   * 1. Получить критерии поиска.
   * 2. Получить каталог заставок.
   * 3. Выполнить поиск.
   * 4. Обработать коллизии.
   * 5. Проверить доступность ресурса.
   * 6. Вернуть результат.
   *
   * Рекомендуемые утилиты:
   * - getScreensaverCatalog()
   * - filterCatalogItems()
   * - checkImageAvailability()
   * - applyScreensaver()
   */
  async function findScreensaver(query, options) {
    // TODO: Реализовать поиск заставки.
    throw new Error("Not implemented");
  }

  function setStatus(id, text, ok) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = text;
    el.classList.toggle("online", Boolean(ok));
    el.classList.toggle("offline", ok === false);
  }

  async function onLoadModelClick() {
    const sourceType = document.getElementById("modelSourceSelect")?.value;
    const modelId = document.getElementById("modelIdInput")?.value?.trim();
    setStatus("modelLoadStatus", "Загрузка…", false);
    try {
      const model = await loadModel(sourceType, modelId);
      setStatus("modelLoadStatus", `Модель: ${model?.name || modelId}`, true);
    } catch (err) {
      if (typeof global.showModelLoadError === "function") {
        global.showModelLoadError(err.message || String(err));
      } else {
        setStatus("modelLoadStatus", err.message || String(err), false);
      }
    }
  }

  async function onFindBackgroundClick() {
    const query = document.getElementById("backgroundQuery")?.value || "";
    setStatus("backgroundStatus", "Поиск фона…", false);
    try {
      const result = await findBackground(query, {});
      if (!result) {
        setStatus("backgroundStatus", "Фон не найден", false);
        return;
      }
      setStatus("backgroundStatus", `Найден фон: ${result.name || result.id}`, true);
    } catch (err) {
      setStatus("backgroundStatus", err.message || String(err), false);
    }
  }

  async function onFindScreensaverClick() {
    const query = document.getElementById("screensaverQuery")?.value || "";
    setStatus("screensaverStatus", "Поиск заставки…", false);
    try {
      const result = await findScreensaver(query, {});
      if (!result) {
        setStatus("screensaverStatus", "Заставка не найдена", false);
        return;
      }
      setStatus("screensaverStatus", `Найдена заставка: ${result.name || result.id}`, true);
    } catch (err) {
      setStatus("screensaverStatus", err.message || String(err), false);
    }
  }

  function bindStudentControls() {
    document.getElementById("loadModelBtn")?.addEventListener("click", (event) => {
      event.preventDefault();
      onLoadModelClick();
    });
    document.getElementById("findBackgroundBtn")?.addEventListener("click", (event) => {
      event.preventDefault();
      onFindBackgroundClick();
    });
    document.getElementById("findScreensaverBtn")?.addEventListener("click", (event) => {
      event.preventDefault();
      onFindScreensaverClick();
    });
    document.getElementById("clearScreensaverBtn")?.addEventListener("click", (event) => {
      event.preventDefault();
      if (typeof global.applyScreensaver === "function") global.applyScreensaver("");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindStudentControls);
  } else {
    bindStudentControls();
  }

  global.loadModel = loadModel;
  global.findBackground = findBackground;
  global.findScreensaver = findScreensaver;
})(window);
