@echo off
title Professor Treinador
cd /d "%~dp0"

echo ==============================================
echo   Professor Treinador
echo ==============================================
echo.

rem --- Verifica/inicia o Ollama (IA de correcao) ---
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I "ollama.exe" >NUL
if errorlevel 1 (
    echo Iniciando Ollama ^(IA de correcao^) em segundo plano...
    start "" /min ollama serve
    ping -n 4 127.0.0.1 >NUL
) else (
    echo Ollama ja esta em execucao.
)
echo.

rem --- Verifica se o Treinador ja esta rodando ---
curl -s --max-time 2 -o NUL -w "%%{http_code}" http://127.0.0.1:8000/ > "%TEMP%\treinador_check.txt" 2>NUL
set /p STATUS=<"%TEMP%\treinador_check.txt"
del "%TEMP%\treinador_check.txt" >NUL 2>&1

if "%STATUS%"=="200" (
    echo O Treinador ja esta rodando. Abrindo no navegador...
    start "" http://localhost:8000
    ping -n 3 127.0.0.1 >NUL
    exit /b 0
)

echo Iniciando o Professor Treinador...
echo ^(Esta janela precisa ficar aberta enquanto voce usa o app.
echo  Feche-a quando terminar.^)
echo.

where python >NUL 2>&1
if errorlevel 1 (
    py server.py
) else (
    python server.py
)

pause
