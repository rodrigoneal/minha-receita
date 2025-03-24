import os
from tempfile import NamedTemporaryFile

from dotenv import load_dotenv
import pytest

from minha_receita import MinhaReceita

load_dotenv(override=True)

@pytest.fixture(scope="module")
def minha_receita():
    return MinhaReceita(cnpj=os.getenv("CNPJ"), senha=os.getenv("SENHA"))


def test_meus_dados(minha_receita):
    notas = minha_receita.meus_dados
    assert "19" in notas.cnpj

def test_notas_emitidas(minha_receita):
    notas = minha_receita.notas_emitidas()
    assert len(notas) > 0

def test_se_baixa_xml(minha_receita):
    notas = minha_receita.notas_emitidas()
    with NamedTemporaryFile(suffix=".xml", mode="w+", encoding="utf-8") as f:
        notas[0].download_xml(f.name)
        f.seek(0)
        xml_content = f.read()
        assert "<?xml" in xml_content
        

def test_se_baixa_pdf(minha_receita):
    notas = minha_receita.notas_emitidas()
    with NamedTemporaryFile(suffix=".pdf", mode="wb+") as f:
        notas[0].download_pdf(f.name)
        f.seek(0)
        pdf_content = f.read()
        assert pdf_content.startswith(b"%PDF")
        