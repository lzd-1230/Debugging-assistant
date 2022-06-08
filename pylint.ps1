Write-Host "lint job"
conda run -n pyqt python -m pip install pylint
conda run -n pyqt pylint --errors-only Plot/ Network/ uart/ utils/