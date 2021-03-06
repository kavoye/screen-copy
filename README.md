# Copy-Screen
Windows tray application for copying text from screen snip to clipboard.

![Copy Screen](screenshot_settings.png)
## About 
- This tool is using [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) engine.
- To use Copy Screen install **Tesseract installer for Windows** from [here](https://github.com/UB-Mannheim/tesseract/wiki).
- Currently only **english** and **russian** languages available.
- To activate Area Grab simply click on tray icon or RMB then select **Grab Area**.
- *Experimental* **CTRL+SHIFT+X** hotkey can be enabled in the settings menu.
- Different tesseract parameters such as **--pcm --oem** can be added in the settings.

## Setup
How to build:  

    pip install pipenv
    mkdir .venv
    pipenv install
    py setup.py build
    run post_clean-up.bat from build folder

## Known issues
- [ ] Using both hotkey and right click on tray will result in crash.
  - **Workaround**: use only one option at a time.
- [ ] Screen capture rectangle gets brighter only in one direction.
- [ ] Currently keyboard shortcut to cancel a screenshot not available.