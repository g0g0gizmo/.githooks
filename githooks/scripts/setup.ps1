# Go to the root of the repository..so up one level
Set-Location -Path ".."

Write-Host "Create the .venv directory if it doesn't exist"
python -m venv .venv
Write-Host "Activate the virtual environment"
.\\.venv\\Scripts\\Activate.ps1
Write-Host "Upgrade pip to the latest version"
python -m pip install --upgrade pip
Write-Host "Install editable package with all extras like dev and test dependencies"
Write-Host "Current directory is: $(Get-Location)"
pip install -e .
pip install -e .[dev]
pip install -e .[test]
Write-Host "===============================SETUP IS NOT COMPLETE==============================="
Write-Host "VScode still needs python interpreter to be set to .venv/Scripts/python.exe"
Write-Host "You can do this by pressing Ctrl+Shift+P and selecting 'Python: Select Interpreter'"
Write-Host "Then select the .venv/Scripts/python.exe interpreter"
Write-Host "Hit Ctrl+Shift+P and select Reload Developer Window"
Write-Host "===============================++++++++++++++++++++++==============================="