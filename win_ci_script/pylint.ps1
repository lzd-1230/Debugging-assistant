Write-Host "-------------------build job-------------------"
conda activate pyqt-runner
python -m pip install pylint
pylint --errors-only Plot/ Network/ uart/ utils/
