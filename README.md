# 🎬 K-On audio adder

Автоматический Python-скрипт для добавления русской аудиодорожки (Ancord) к сериям **K-On!** в формате `.mkv`.

Скрипт:

* Конвертирует `.mka` (AC3) → Opus
* Добавляет аудиодорожку в `.mkv`
* Устанавливает русский звук как default
* Удаляет временные файлы
* Сохраняет результат в папку `output/`

---

## 📂 Структура проекта

```
.
├── main.py
├── RUS Sound/
│   └── [Ancord]/
│       ├── Episode 01.mka
│       └── ...
├── Episode 01.mkv
├── Episode 02.mkv
└── ...
```

---

## ⚙ Требования

Arch Linux:

```bash
sudo pacman -S ffmpeg mkvtoolnix-cli
```

Проверка:

```bash
ffmpeg -version
mkvmerge --version
```

---

## 🚀 Запуск

```bash
python main.py
```

После выполнения обработанные файлы появятся в:

```
output/
```

---

## 🔧 Что делает скрипт

1. Находит `.mkv` файлы вида:

   ```
   [Winter] K-On! XX [BDrip ...].mkv
   ```

2. Ищет соответствующее аудио:

   ```
   RUS Sound/[Ancord]/... .mka
   ```

3. Конвертирует аудио:

   ```
   AC3 → Opus (192kbps)
   ```

4. Выполняет mux через `mkvmerge`

---

## 🛠 Возможные ошибки

### ❌ ffmpeg not found

Установите:

```bash
sudo pacman -S ffmpeg
```

### ❌ mkvmerge not found

Установите:

```bash
sudo pacman -S mkvtoolnix-cli
```

---

## 💡 Почему используется Opus?

Без конвертации дорожка не воспроизводила звук
