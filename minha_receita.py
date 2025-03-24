from dataclasses import dataclass
from requests import Session
import requests

from core.handlers.requests_handlers.login_handler import create_session, login
from core.handlers.requests_handlers.meus_dados_handlers import meus_dados
from core.handlers.requests_handlers.nota_handlers import pegar_notas


@dataclass
class MeusDados:
    cnpj: str
    nome: str
    telefone: str
    email: str

    def __post_init__(self):
        fields = self.__dataclass_fields__
        for field in fields:
            value = getattr(self, field)
            if "não informado" in value.lower():
                setattr(self, field, None)


class NotaSimplificada:
    def __init__(
        self, geracao, emitido_para, municipio, valor, situacao, imposto, chave_nota
    ):
        self.geracao = geracao
        self.emitido_para = emitido_para
        self.municipio = municipio
        self.valor = valor
        self.situacao = situacao
        self.imposto = imposto
        self.chave_nota = chave_nota
        self.session = None

    def __repr__(self):
        return f"Notas_Simplificadas <Geração: {self.geracao} Emitido para: {self.emitido_para} Município: {self.municipio} Valor: {self.valor} Situação: {self.situacao} Imposto: {self.imposto}>"

    def _download(self, url: str, local: str):
        with open(local, "wb") as f:
            f.write(self.session.get(url).content)

    def download_xml(self, nome_arquivo: str):
        url = f"https://www.nfse.gov.br/EmissorNacional/Notas/Download/NFSe/{self.chave_nota}"
        self._download(url, nome_arquivo)

    def download_pdf(self, nome_arquivo: str):
        url = f"https://www.nfse.gov.br/EmissorNacional/Notas/Download/DANFSe/{self.chave_nota}"
        self._download(url, nome_arquivo)


class MinhaReceita:
    def __init__(self, cnpj, senha):
        self.cnpj = cnpj
        self.senha = senha
        self.session = create_session(cnpj=self.cnpj, password=self.senha)
        # login(self.session, self.cnpj, self.senha)

    def __repr__(self):
        return f"Minha Receita\nCNPJ: {self.cnpj}"

    @property
    def meus_dados(self):
        _meus_dados = meus_dados(self.session)
        return MeusDados(**_meus_dados)

    def notas_emitidas(self):
        notas = []
        for nota in pegar_notas(self.session):
            nota_simplificada = NotaSimplificada(**nota)
            nota_simplificada.session = self.session
            notas.append(nota_simplificada)
        return notas
