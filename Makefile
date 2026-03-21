run_local:
	uvicorn main:app --reload

install_packages:
	pip install -r requirements.txt
