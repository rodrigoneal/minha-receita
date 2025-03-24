from dateutil.parser import parse
from decimal import Decimal

from bs4 import BeautifulSoup
from requests import Session


def notas_emitidas(session: Session):
    URL: str = "https://www.nfse.gov.br/EmissorNacional/Notas/Emitidas"
    response = session.get(URL)
    return response


def pegar_notas(session: Session):
    response = notas_emitidas(session)
    soup = BeautifulSoup(response.text, "html.parser")
    trs = soup.find_all("tr")
    dados_nota = {}
    del trs[0]
    for tr in trs:
        _data = tr.find("td", {"class": "td-data"}).get_text(strip=True)
        dados_nota["geracao"] = parse(_data, dayfirst=True)
        dados_nota["emitido_para"] = (
            tr.find("td", {"class": "td-texto-grande"})
            .get_text(strip=True)
            .replace("\r\n", " ")
        )
        dados_nota["municipio"] = tr.find("td", {"class": "td-center"}).get_text(
            strip=True
        )
        dados_nota["valor"] = Decimal(
            tr.find("td", {"class": "td-valor"})
            .get_text(strip=True)
            .replace("R$", "")
            .replace(".", "")
            .replace(",", ".")
        )
        dados_nota["situacao"] = (
            tr.find("td", {"class": "td-situacao"}).find("img")["title"].strip()
        )
        dados_nota["imposto"] = (
            tr.find("td", {"class": "td-impostos"}).find("img")["title"].strip()
        )
        dados_nota["chave_nota"] = tr.find("a", {"class": "list-group-item"})[
            "href"
        ].split("/")[-1]
        yield dados_nota
