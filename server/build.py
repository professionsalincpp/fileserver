import subprocess
import sys
import platform

def build():
    ENTRY_POINT = "main.py"          # ваш главный файл
    OUTPUT_NAME = "myserver"            # имя выходного файла
    INCLUDE_DATA_DIRS = [               # папки с данными (templates, static)
        # "templates",
        # "static",
    ]
    PLUGINS = []                  # плагины

    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",                   # папка с библиотеками (без сжатия)
        "--follow-imports",
        "--output-dir=build",              # отключить UPX-сжатие
        f"--output-file={OUTPUT_NAME}",
    ]
    for plugin in PLUGINS:
        cmd.append(f"--enable-plugin={plugin}")
    for data_dir in INCLUDE_DATA_DIRS:
        cmd.append(f"--include-data-dir={data_dir}={data_dir}")
    cmd.append(ENTRY_POINT)

    print("🚀 Запуск сборки...")
    subprocess.run(cmd)
    print(f"✅ Готово. Исполняемый файл: build/{OUTPUT_NAME}.dist/")

if __name__ == "__main__":
    build()