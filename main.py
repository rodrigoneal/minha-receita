
class Field:
    def __init__(self, nome):
        self.nome = nome

    def __eq__(self, outro):
        # Retorna uma função que verifica se o valor do campo é igual ao valor passado
        return lambda obj: obj.get(self.nome) == outro

    def __ne__(self, outro):
        return lambda obj: obj.get(self.nome) != outro

    def __gt__(self, outro):
        return lambda obj: obj.get(self.nome) > outro

    def __lt__(self, outro):
        return lambda obj: obj.get(self.nome) < outro

    def __ge__(self, outro):
        return lambda obj: obj.get(self.nome) >= outro

    def __le__(self, outro):
        return lambda obj: obj.get(self.nome) <= outro

class Query:
    def __init__(self, dados):
        self.dados = dados

    def filter(self, *criterios):
        resultado = self.dados
        for criterio in criterios:
            breakpoint()
            resultado = list(filter(criterio, resultado))
        return resultado

# Exemplo de uso:

# Define o "campo" nota, imitando o Model.nota do SQLAlchemy
nota = Field("nota")

# Lista de dados (poderia ser um conjunto de dicionários ou objetos)
notas = [
    {"nome": "João", "nota": 15},
    {"nome": "Maria", "nota": 18},
    {"nome": "Carlos", "nota": 15},
    {"nome": "Ana", "nota": 20},
	{"nome": "Pedro", "nota": 12},
]

# Cria a "query"
query = Query(notas)

# Filtra os dados de forma similar ao SQLAlchemy:
result_equal = query.filter(nota == 15)   # notas iguais a 15
result_gt    = query.filter(nota > 15)      # notas maiores que 15
result_lt    = query.filter(nota < 15)      # notas menores que 15
result_ne    = query.filter(nota != 15)     # notas diferentes de 15

print("Equal 15:", result_equal)
print("Greater than 15:", result_gt)
print("Less than 15:", result_lt)
print("Not equal to 15:", result_ne)
