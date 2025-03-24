# import os


# import pytest
# import requests


# from dotenv import load_dotenv

# from core.handlers.requests_handlers.login_handler import login

# load_dotenv(override=True)


# @pytest.fixture(scope="module")
# def session():
#     return requests.Session()


# def test_se_faz_login(session):
#     response = login(session, os.getenv("CNPJ"), os.getenv("SENHA"))
#     assert response.status_code == 200
#     assert "Página Principal" in response.text
