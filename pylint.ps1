conda init
conda activate pyqt
Write-Host "lint job"
python -m pip install pylint
pylint --errors-only Plot/ Network/ uart/ utils/