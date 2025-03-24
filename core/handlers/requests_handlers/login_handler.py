from http.cookiejar import MozillaCookieJar
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import Session

from settings import BASE_URL

class LoginError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def validar_login(response):
    soup = BeautifulSoup(response.text, "html.parser")
    alerta = soup.find("div", {"class": "alert"})
    if alerta:
        raise LoginError(alerta.get_text(strip=True))

def create_session(cnpj: str, password: str):
    session = Session()
    # Define o arquivo de cookies
    session.cookies = MozillaCookieJar("cookies.txt")
    
    # Tenta carregar os cookies salvos
    try:
        session.cookies.load(ignore_discard=True, ignore_expires=True)
        response = session.get(BASE_URL)
        if "Acesso com" in response.text:
            raise FileNotFoundError
    except FileNotFoundError:
        print("Arquivo de cookies não encontrado. Será necessário fazer login.")
        login(session, cnpj, password)
    
    return session


def login(session: Session, cnpj: str, password: str):
    url = urljoin(BASE_URL, "login")
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    token = soup.find("input", {"name": "__RequestVerificationToken"}).get("value")
    data = {"__RequestVerificationToken": token, "Inscricao": cnpj, "Senha": password}
    response = session.post(url, data=data)
    with open("login.html", "w") as file:
        file.write(response.text)
    validar_login(response)
    session.cookies.save(ignore_discard=True, ignore_expires=True)
    return response
