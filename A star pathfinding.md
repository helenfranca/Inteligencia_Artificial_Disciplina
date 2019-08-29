
## Atividade desenvolvida para a disciplina de Inteligência Artificial

### O Algoritmo A*

Algoritmo A* (Lê-se: A-estrela) é um algoritmo para Busca de Caminho. Ele busca o caminho em um grafo de um nó inicial até um nó final. É a combinação de aproximações heurísticas como do algoritmo Breadth First Search (Busca em Largura) e da formalidade do Algoritmo de Dijkstra. Foi descrito pela primeira vez em 1968 por Peter Hart, Nils Nilsson, e Bertram Raphael. Na publicação deles, foi chamado de algoritmo A. 

Usando este algoritmo com uma heurística apropriada atinge-se um comportamento ótimo, e passou a ser conhecido por A*. Sua aplicação vai desde aplicativos para encontrar rotas de deslocamento entre localidades a resolução de problemas, como a resolução de um quebra-cabeças.

O algoritmo A* avalia os nós através da combinação de g(n) que é o custo para alcançar cada nó com a função h(n) que é o menor custo partindo da origem para se chegar ao destino, matematicamente dado na equação:



                                                f(n) = g(n) + h(n)

* g(n): é o custo do movimento para se mover do nó de início até o nó determinado no grafo seguindo o caminho criado para chegar lá.

* h(n): é o custo estimado do movimento para mover daquele nó determinado até o destino final, o objetivo.

* f(n): é o custo estimado da solução de custo mais baixo passando por n.

-----------------

### Problema proposto

Foi nos dado como atividade implementar o algoritmo A* para resolver o seguinte problema:
<br>Dado um mapa com obstáculos, o algoritmo deve traçar o caminho menos custoso de um ponto A a um ponto B. 

Como recurso temos: 

* Um mapa em arquivo txt composto por 0 e 1, onde 0 representa um caminho livre e o 1 representa um obstáculo;
* Um ponto de partida que chamaremos de A;
* Um ponto de fim ou objetivo que chamaremos de B.


As especificações para resolução foram:

* Permitir o uso de mapas diferentes;
* Leitura do ponto de partida e de chegada;
* Implementar uma heuristica para conhecer o menor custo para o caminho;
* Só é permitido realizar rotas em linha reta ou de 90°;
* Ao final, mostrar um mapa com o desenho da trajetória e a lista das coordenadas a serem percorridas.

<img src="https://github.com/helenfranca/Inteligencia_Artificial_Disciplina/tree/master/Imagem/Capturar.PNG" title="A* pathfinding" width="200" />


Legenda: 
* Quadrado vermelho: Ponto de partida
* Quadrado verde: Ponto de chegada
* Quadrado preto: Obstáculo

_______


### Resolução

### Detalhamento das funções

#### Monta o mapa conforme no arquivo informado


```python
def montaMapa(nomedoarquivo):
    arquivo= pd.read_csv(nomedoarquivo+".txt")

    mapa = []
    for linha in arquivo[arquivo.columns[0]]:
        b = []
        for elem in linha:
            if elem != ' ':
                b.append(int(elem))
        mapa.append(b)
    return mapa
```



#### Classe do objeto nó


```python
class Node():

    def __init__(self, pai=None, posicao=None):
        self.pai = pai
        self.posicao = posicao

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, outro):
        return self.posicao == outro.posicao

```

#### Heuristica baseada na função distância de Manhattan (calculo literal da distância do nó atual e o nó destino - desconsiderando os obstáculos)


```python
def calcH(vizinhoPos,fimPos):
    return ((abs(vizinhoPos[0]-fimPos[0]))+(abs(vizinhoPos[1]-fimPos[1])))

```

#### Define os vizinhos "possiveis" do nó atual (definido na função buscaMenorF)


```python
def defVizinhos(matriz,atual,lstAberta,lstVizinhos,posPossiveis,tamLMatriz,tamCMatriz):
    
    for item in posPossiveis:
        
        posEncontrada = (atual.posicao[0]+item[0],atual.posicao[1]+item[1])
                
        if  ((posEncontrada[0]<tamLMatriz and posEncontrada[0]>=0) and (posEncontrada[1]<tamCMatriz and posEncontrada[1]>=0)):
            if(matriz[posEncontrada[0]][posEncontrada[1]] != 1):
                lstVizinhos.append(Node(atual, posEncontrada))
    return lstVizinhos
```

#### Busca o menor caminho (g+h) até o destino


```python
def buscaMenorF(lstAberta):
    menorF = lstAberta[0]

    for i in range(1, len(lstAberta)):
        if (menorF.f > lstAberta[i].f):
            menorF = lstAberta[i]

    return menorF
```

#### Faz o caminho baseado nos "pais" dos nós


```python
def caminho(atual, inicio):
    caminho = [atual.posicao]
    
    while atual.posicao != inicio.posicao:
        caminho.append(atual.pai.posicao)
        atual = atual.pai
    return caminho
```

#### Desenha o caminho na matriz


```python
def desenhaCaminho(matriz, caminho):
    print(caminho)
    for item in caminho:
        matriz[item[0]][item[1]] = '*'
    return matriz
```

#### Imprime a matriz


```python
def printaMatriz(matriz):
    print()
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            print(" ",matriz[i][j], end= "")
        print()
```

#### Verifica entrada


```python
if (fimPos[0] <0 or fimPos[1]<0 or atualPos[0]<0 or atualPos[1] < 0):
    print("ERRO! Posição deve conter valores maiores que zero.")
    exit   
elif (matriz[fimPos[0]][fimPos[1]] == 1):
    print("ERRO! Posição final é um obstáculo.")
    exit

elif (fimPos == atualPos):
    print("Posição destino == Posição fim")
    exit
elif (matriz[atualPos[0]][atualPos[1]] == 1):
    print("ERRO! Posição inicial é um obstáculo.") 
    exit
```

____

### Entradas

#### Para inserir um novo mapa
* Certifique-se de que o arquivo do mapa que irá utilizar está na mesma pasta do arquivo que contém o algoritmo.
* Coloque o arquivo "nomedoarquivo".txt entre os parenteses. Ex: matriz = montaMapa('mapa')

#### Para informar as coordenadas
* Na variável *atualPos* informe o valor. Ex: (0,0)
* Na variável *fimPos* informe o valor. Ex: (8,9)

### Execução do algoritmo


```python
import time
import pandas as pd
%config IPCompleter.greedy=True


class Node:

    def __init__(self, pai, posicao):
        self.g = 0
        self.h = 0
        self.f = 0
        self.posicao = posicao

        self.pai = pai

    def __eq__(self, other):
        if other is not Node:
            return self.posicao == other
        else:
            return self.posicao == other.posicao

        
def calcH(vizinhoPos,fimPos):
    return ((abs(vizinhoPos[0]-fimPos[0]))+(abs(vizinhoPos[1]-fimPos[1])))
    

def defVizinhos(matriz,atual,lstAberta,lstVizinhos,posPossiveis,tamLMatriz,tamCMatriz):
    
    for item in posPossiveis:
        
        posEncontrada = (atual.posicao[0]+item[0],atual.posicao[1]+item[1])
                
        if  ((posEncontrada[0]<tamLMatriz and posEncontrada[0]>=0) and (posEncontrada[1]<tamCMatriz and posEncontrada[1]>=0)):
            if(matriz[posEncontrada[0]][posEncontrada[1]] != 1):
                lstVizinhos.append(Node(atual, posEncontrada))
    return lstVizinhos


        
def buscaMenorF(lstAberta):
    menorF = lstAberta[0]

    for i in range(1, len(lstAberta)):
        if (menorF.f > lstAberta[i].f):
            menorF = lstAberta[i]

    return menorF
    
    
def caminho(atual, inicio):
    caminho = [atual.posicao]

    while atual.posicao != inicio.posicao:
        caminho.append(atual.pai.posicao)
        atual = atual.pai
    return caminho


def desenhaCaminho(matriz, caminho):
    for item in caminho:
        matriz[item[0]][item[1]] = '*'
    return matriz


def printaMatriz(matriz):
    print()
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            print(" ",matriz[i][j], end= "")
        print()
        

def montaMapa(nomedoarquivo):
    arquivo= pd.read_csv(nomedoarquivo+".txt")

    mapa = []
    for linha in arquivo[arquivo.columns[0]]:
        b = []
        for elem in linha:
            if elem != ' ':
                b.append(int(elem))
        mapa.append(b)
    return mapa

    
# Entradas
atualPos = (0,0)
fimPos = (8,9)
matriz = montaMapa('mapa')

#-----
lstAberta = []
lstFechada = []
lstVizinhos = []
posPossiveis = ((-1,0), (1,0), (0,-1), (0, 1))
tamLMatriz = len(matriz)
tamCMatriz = len(matriz[0])
inicio = Node(None, atualPos)
fim = Node(None, fimPos)
 

if (fimPos[0] <0 or fimPos[1]<0 or atualPos[0]<0 or atualPos[1] < 0):
    print("ERRO! Posição deve conter valores maiores que zero.")
    exit   
elif (matriz[fimPos[0]][fimPos[1]] == 1):
    print("ERRO! Posição final é um obstáculo.")
    exit

elif (fimPos == atualPos):
    print("Posição destino == Posição fim")
    exit
elif (matriz[atualPos[0]][atualPos[1]] == 1):
    print("ERRO! Posição inicial é um obstáculo.") 
    exit
else:

    lstAberta.append(inicio)

    while(len(lstAberta) > 0):

        # Definição do nó atual como sendo o que possui menor distância até o destino    
        atual = buscaMenorF(lstAberta)

        #Se a posicao do nó atual for igual a posicao do nó destino significa que chegamos ao nó destino
        if (atual.posicao == fim.posicao): break


        #Adiciona o no atual na lista fechada e remove da lista aberta, afinal ele já foi analisado
        lstAberta.remove(atual)
        lstFechada.append(atual)


        #Definimos os vizinhos "possíveis" do nó atual
        vizinhos = defVizinhos(matriz,atual,lstAberta,lstVizinhos,posPossiveis,tamLMatriz,tamCMatriz)

        #Para cada vizinho possível 
        for vizinho in vizinhos:

            #Verificamos se está na lista fechada, se estiver, passa para o próximo vizinho
            if (vizinho in lstFechada): continue

            #Se ele não estiver na lstAberta quer dizer que ainda não sabemos os valores do F, portanto calculamos e o 
            #adicionamos na lstAberta
            if (vizinho not in lstAberta):
                vizinho.pai = atual
                vizinho.g = atual.g + 1
                vizinho.h = calcH(vizinho.posicao,fimPos)
                vizinho.f = vizinho.g + vizinho.h
                lstAberta.append(vizinho)

            #Se o vizinho estiver na lstAberta e "passando pelo nó atual o valor de g do vizinho é menor do que o 
            #que ele tem agora?" então recalculamos os valores de g, h e f e mudamos o pai dele para o nó atual
            elif (vizinho in lstAberta and ((atual.g+1) < vizinho.g)):
                vizinho.g = atual.g+1
                vizinho.h = calcH(vizinho.posicao,fimPos)
                vizinho.f = vizinho.g + vizinho.h
                vizinho.pai = atual


    caminho = caminho(atual, inicio)
    caminho.reverse()
    
    print('\n*** Resultado ***\n\nPonto de partida:',atualPos)
    print('Ponto de chegada:',fimPos)
    print('\n',caminho)
    
    printaMatriz(desenhaCaminho(matriz,caminho)) 

    
```

    
    *** Resultado ***
    
    Ponto de partida: (0, 0)
    Ponto de chegada: (8, 9)
    
     [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9)]
    
      *  0  1  0  0  0  0  0  0  0
      *  0  1  0  0  0  0  0  0  0
      *  0  1  0  0  0  0  0  0  0
      *  0  0  0  0  0  0  1  1  1
      *  *  *  *  *  *  0  0  0  0
      0  0  0  0  1  *  0  0  0  0
      0  0  0  0  1  *  0  1  1  1
      0  0  0  0  1  *  0  0  0  0
      0  0  0  0  1  *  *  *  *  *
    