@echo off
echo ===== Starting Nightly Regression =====

REM Go to project folder
cd /d C:\Users\Sakshi Gangurde\Desktop\TMind-Automation\source_code

REM Clean old reports
if exist allure-results rmdir /s /q allure-results
if exist allure-report rmdir /s /q allure-report
if exist Nightly_Regression_Report.html del Nightly_Regression_Report.html

echo ===== Running Pytest =====

REM Run Pytest with BOTH reports
pytest -v RunTest.py ^
 --html=Nightly_Regression_Report.html ^
 --self-contained-html ^
 --alluredir=allure-results

echo ===== Generating Allure HTML Report =====
allure generate allure-results --clean -o allure-report

echo ===== Opening Reports =====

REM Open simple HTML report
start "" "Nightly_Regression_Report.html"

REM Open Allure report
start "" "allure-report\index.html"

echo ===== Nightly Regression Completed =====
pause
