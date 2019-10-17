import random
import math


class Cromossomo:
    def __init__(self, corpo):
        self.corpo = corpo
        
        # Normaliza
        dec = bin2Dec(formata(corpo))
        self.x = (-20) + (20 + 20) * (dec / (pow(2,10) - 1))
        
        # Calcula a aptidao baseado no numero normalizado
        self.aptidao = math.cos(self.x) * self.x + 2

    def get_corpo(self):
        return self.corpo

    def get_x(self):
        return self.x

    def get_aptidao(self):
        return self.aptidao
    
    def atualiza(self):
        dec = bin2Dec(formata(self.corpo))
        self.x = (-20) + (20 - (-20)) * (dec / pow(2,10) - 1)
        self.aptidao = math.cos(self.x) * self.x + 2


def cria_cromossomo():

    cromossomo = [random.randrange(0, 2) for x in range(0, 10)]

    return cromossomo


def cria_populacao(numero_populacao):

    populacao = [
        Cromossomo(cria_cromossomo()) for x in range(0, numero_populacao)
    ]
    return populacao

def selecao_torneio(populacao):
    pais = []
    

    for _ in range(0,len(populacao)):
        a = random.choice(populacao) # Pega um cromossomo 
        b = random.choice(populacao) # Pega um cromossomo

    # Verifica quem é menor. O menor se torna um pai para a nova geração
        if (a.get_aptidao() < b.get_aptidao()):
            pai = a
        else:
            pai = b

        pais.append(pai)
    
    return pais


def crossover(pais):
    nova_geracao = []
    tam = 0
    while tam < len(pais):
        taxa_cross = random.uniform(0,1) * 100

        paiUm = pais[tam]
        paiDois = pais[tam + 1]

        if taxa_cross <= 60 :
            #Cruzamento
            corte = random.randrange(1,10)
            cromossomo_pai_um = paiUm.get_corpo()
            cromossomo_pai_dois = paiDois.get_corpo()

            filhoUm = cromossomo_pai_um[0:corte] + cromossomo_pai_dois[corte:]
            filhoDois = cromossomo_pai_dois[0:corte] + cromossomo_pai_um[corte:]

            filhoUm = Cromossomo(filhoUm)
            filhoDois = Cromossomo(filhoDois)
            
        else:
            filhoUm = paiUm
            filhoDois = paiDois

        nova_geracao.append(filhoUm)
        nova_geracao.append(filhoDois) 
        tam = tam + 2

    return nova_geracao

def mutacao(nova_geracao):
    for filho in nova_geracao:
        cromossomo = filho.get_corpo()
        
        for i in range(0,len(cromossomo)):
            taxa_mutacao = random.randrange(0,2)
            if(taxa_mutacao == 1):
                if(cromossomo[i] == 0):
                    cromossomo[i] = 1
                else:
                    cromossomo[i] = 0
        filho.atualiza()


def elitismo(nova_geracao, populacao):
    
    melhor_pai = sorted(populacao, key=Cromossomo.get_aptidao)[0]
    filhos_ordenados = sorted(nova_geracao, key=Cromossomo.get_aptidao)
    melhor_filho = filhos_ordenados[0]
    
    if melhor_pai.get_aptidao() < melhor_filho.get_aptidao():
        nova_geracao[len(nova_geracao) - 1] = melhor_pai


def bin2Dec(binary):

    decimal, i = 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal


def formata(corpo):
    b = ''
    for i in corpo:
        b = str(i) + '' + b
    return int(b)


def main():

    numero_populacao = 10
    pais = []
    nova_geracao = []

    # 1° Passo: Criar População c/ aptidão
    populacao = cria_populacao(numero_populacao)

    for _ in range(0,10):
        # 2° Passo: Seleção por Torneio
        pais = selecao_torneio(populacao)
    
        # 3° Passo: Crossover
        nova_geracao = crossover(pais)

        # 4° Passo: Mutação
        mutacao(nova_geracao)

        # 5° Passo: Elitismo
        elitismo(nova_geracao, populacao)
        populacao = nova_geracao
        
        print(sorted(nova_geracao, key=Cromossomo.get_aptidao)[0].get_aptidao())
    
    
                        
main()