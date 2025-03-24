from bs4 import BeautifulSoup
from requests import Session
from settings import BASE_URL


def meus_dados_requests(session: Session):
    url = BASE_URL
    return session.get(url)


def meus_dados(session: Session):
    response = meus_dados_requests(session)
    soup = BeautifulSoup(response.text, "html.parser")
    telefone = (
        soup.find("b", string="Telefone:")
        .parent.get_text(strip=True, separator=" ")
        .replace("Telefone:", "")
        .strip()
    )
    nome = (
        soup.find("b", string="Nome:")
        .parent.get_text(strip=True, separator=" ")
        .replace("Nome:", "")
        .strip()
    )
    email = (
        soup.find("b", string="E-mail:")
        .parent.get_text(strip=True, separator=" ")
        .replace("E-mail:", "")
        .strip()
    )
    cnpj = soup.find("span", {"class": "cnpj"}).get_text(strip=True, separator=" ")
    return {"telefone": telefone, "nome": nome, "email": email, "cnpj": cnpj}
