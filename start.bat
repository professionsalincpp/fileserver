@echo off

set "last_version="

cd "C:\Users\griuc\Desktop\Https Server\bin"

for /d %%d in (v*) do (
    if "%%d" gtr "%last_version%" (
        set "last_version=%%d"
    )
)


if not "%last_version%"=="" (
    echo Version: %last_version%
    cd %last_version%
    start main.exe --config "..\config.ini" 
) else (
    echo "No version found"
)

pause