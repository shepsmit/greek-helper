$path_to_venv = poetry env info --path
[string] $body = "$path_to_venv\Scripts\activate.ps1"    

Write-Output "Activating Virtual Environment at $body"
& $body

Write-Output "Starting up Python GUI"
python src/main.py