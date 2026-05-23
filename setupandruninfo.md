Powershell

Initialize the virtual environment
python -m venv venv

Activate the virtual environment
.\venv\Scripts\Activate.ps1

Install the core dependencies
pip install "gql[requests]" pydantic python-dotenv
