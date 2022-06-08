Write-Host "-------------------build job-------------------"
conda run python -m pip install pylint
conda run pylint --errors-only Plot/ Network/ uart/ utils/