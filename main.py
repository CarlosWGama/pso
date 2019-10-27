import numpy as np
import math
import random
import matplotlib.pyplot as plt
import copy

def clone(particulas):
    clone = []
    for p in particulas:
        clone.append(copy.copy(p));
    return clone

def sphere(posicao): 
    """ Retorna o fitness em uma esfera """
    
    total = 0
    for index in range(len(posicao)):
        total += posicao[index]**2
    return total

def rastringin(posicao):
    """ Retorna o fitness em uma rastringin """
    return 10*len(posicao) + sum([(x**2 - 10 * np.cos(2 * math.pi * x)) for x in posicao])

def gerarVetor(dimensao):
    """ Retorna um vetor na dimensão desejada """
    vetor = []
    for i in range(dimensao):
        vetor.append(random.randrange(1, 10))
    return vetor


def melhorFocal(foco, atual, funcao):
    """ Retorna a melhor posição baseada na particula foco """
    if (funcao(foco.melhorIndividual) < funcao(atual.melhorIndividual)):
        return foco.melhorIndividual
    else:
        return atual.melhorIndividual


def melhorLocal(particulas, posicao, qtParticulas, funcao):
    """ Retorna como melhor resultado o melhor encontrado entre o nó atual, anterior e próximo """
    anterior = particulas[posicao - 1] if posicao != 0  else particulas[qtParticulas - 1] #Pega o elemento anterior
    proximo =  particulas[posicao + 1] if posicao != (qtParticulas - 1)  else particulas[0] #Pega o próximo elemento
    atual = particulas[posicao]

    fitnessAnterior = funcao(anterior.melhorIndividual)
    fitnessProximo = funcao(proximo.melhorIndividual)
    fitnessAtual = funcao(atual.melhorIndividual)

    menor = min([fitnessAnterior, fitnessAtual, fitnessProximo])
    if (menor == fitnessAnterior):
        return anterior.melhorIndividual
    if (menor == fitnessAtual):
        return atual.melhorIndividual
    return proximo.melhorIndividual

class Particula:
    def __init__(self, posicao, melhorIndividual, velocidade, w, funcao, sofreVariacaoInercia=False):
        """
        Parameters
        ----------
        posicao : array
            Posição Inicial da Particula
        melhorIndividual : array
            Melhor posição individual desta particula
        velocidade : array
            Velocidade da direção da particula
        w :
            Inercia
        funcao :
            Função para analisar o terreno do estudo e avaliar o fitness
        sofreVariacaoInercia :
            Checa se o W vai sofrer alguma variavel  
        """
        #Ddados da Particula
        self.posicao = np.array(posicao)
        self.melhorIndividual = np.array(melhorIndividual)
        self.velocidade = np.array(velocidade)

        #Dados Globais
        self.melhorGlobal = None
        self.sofreVariacaoInercia = sofreVariacaoInercia 
        self.funcao = funcao
        self.ignoraGlobal = False #Ignora a troca da melhor Global
        #DEFININDO AS CONSTANTES
        self.r1 = self.r2 = 0.25 #Um valor aleatório entre 0 e 1, foi escolhido 0.25
        self.c1 = self.c2 = 2.05 #Comportamento da particula para melhor posição local (c1) global (c2)
        self.w = w #Valor da Inercia usada na velocidade ao mover a particular
    
    def mover(self, melhorPosicaoGlobal, melhorFocal=None):        
        """
        Move a Particula
        Formula:
            novaPosicao = posicao + novaVelocidade

        Parameters :
        -----------
        melhorPosicaoGlobal :
            Variavel atualizada com a melhor posição global
        """
        #Atualiza qual é a melhor posição Global antes de mover
        self.melhorGlobal = melhorPosicaoGlobal

        #Antes de mover checa se já está na melhor posição
        #Verifica se é o Melhor Posição Individual ou Global
        self.__acharMelhorPosicaoIndividual()
        self.__acharMelhorPosicaoGlobal()

        #Define a nova velocidade
        self.__novaVelocidade(melhorFocal)

        #Move
        #novaPosicao = posicao + novaVelocidade
        self.posicao = self.posicao + self.velocidade

        #Retorna a melhor posição global
        return self.melhorGlobal

    def __novaVelocidade(self, melhorFocal):
        """
        Define a nova Particula
        Formula:
            novaVelocidade = w*V + r1*c1*(melhorIndividual - posicao) + r2*c2*(melhorGlobal - posicao)
        """
        if (self.sofreVariacaoInercia):
            self.w = random.uniform(0.4, 0.9)


        posicaoSeguir = self.melhorGlobal if melhorFocal is None else melhorFocal 
        velocidadeMelhorI = self.r1*self.c1*(self.melhorIndividual-self.posicao) #Direção Velocidade Melhor Local
        velocidadeMelhorG = self.r1*self.c1*(posicaoSeguir-self.posicao) #Direção Velocidade Melhor Global
        self.velocidade = self.w*self.velocidade + velocidadeMelhorI + velocidadeMelhorG

    def __acharMelhorPosicaoIndividual(self):
        """ Verifica se a posição atual é melhor do que antiga melhor individual """
        #Checa se já está na melhor posição local
        
        if (self.funcao(self.posicao) < self.funcao(self.melhorIndividual)):
            self.melhorIndividual = self.posicao

    def __acharMelhorPosicaoGlobal(self):
        """ Verifica se a posição atual é melhor do que antiga melhor global """
        #Checa se já está na melhor posição global
        if (not self.ignoraGlobal and self.funcao(self.posicao) < self.funcao(self.melhorGlobal)):
            self.melhorGlobal = self.posicao

######### -------------------- INICIO Q1 ----------------------  #################
print(" --------- QUESTÃO 1 ----------")
#Posição Inicial, Melhor Posição, Velocidade e Melhor Global
melhorGlobal = [5,5]
w = 0.8
funcao = sphere #sphere ou rastringin

particulas = [
    Particula([5,5], [5,5], [2,2], w, funcao), #x1
    Particula([8,3], [7,3], [3,3], w, funcao), #x2
    Particula([6,7], [5,6], [4,4], w, funcao), #x3
]   

print("a)")
print("Após 1 Iteração")
#Faz em cada particula
for i in range(len(particulas)): 
    melhorGlobal = particulas[i].mover(melhorGlobal)
    print('Particula X'+str(i), particulas[i].posicao)
    
print("\nb)")
print("A velocidade inicial da particula, define sua posição, porém essa será alterada de acordo com a posição do melhor resultado individual da particula e global. De forma que a formula abaixo vai definir a nova velocidade com a diração correta que a particular irá seguir: ")
print("novaVelocidade = w*v + c1*r1*(melhorLocal-posicao) + c2*r2*(melhorGlobal-posicao) \n")

print("Com a nova velocidade, será definido a nova posição da particula com a formula:")
print("novaPosicao = posicao + novaVelocidade")

print("\nC) Adicionando uma vantagem ou desvantagem na inércia")
for i in range(len(particulas)): 
    particulas[i].w += random.uniform(-0.5, 0.5) #Adiciona uma vantagem ou desvantagem a inercia 
    melhorGlobal = particulas[i].mover(melhorGlobal)
    print('Particula X'+str(i), particulas[i].posicao)
    
    


print("\n\n --------- QUESTÃO 2 ----------")
#Inicia os dados
qtParticulas = 30 #Quantas particular criar
dimensoes = 30 #Qual a dimensão de cada particula
iteracoes = 1000 #Quantas iterações serão realizadas
w = 7
melhorGlobal = gerarVetor(dimensoes) #As melhor posição global
funcao = rastringin #sphere ou rastringin

#Escolhe qual gráfica 
exibirGlobal = True
exibirFocal = True
exibirLocal = True


#Crias a particulas
particulas = []
for i in range(qtParticulas):

    posicao = gerarVetor(dimensoes) #As posições de cada particula aleatóriamente
    melhorPosicao = gerarVetor(dimensoes) #Melhor posiçã ode cada particula aleatoriamente
    velocidade = gerarVetor(dimensoes) #Define a velocidade de cada particula de forma aleatória

    particulas.append(Particula(posicao, melhorPosicao, velocidade, w, funcao, True))

#------------------------------ MELHOR GLOBAL ---------------------------------- #
if (exibirGlobal):
    #Realiza a operação de achar a melhor Global
    listaFitnessGlobal = []
    particulasTGlobal = clone(particulas)
    melhorGlobalG = copy.copy(melhorGlobal);
    for i in range(0, iteracoes):
        
        for particula in particulasTGlobal:
            melhorGlobalG = particula.mover(melhorGlobalG)
        
        fitnessMelhorGlobal = funcao(melhorGlobalG)
        listaFitnessGlobal.append(fitnessMelhorGlobal) #Adiciona o fitness do melhor global na topologia global para gerar o grafico
        print("Iteração: ", i+1, '|Fitness Melhor Resultado [Global]:', fitnessMelhorGlobal)


#------------------------------ MELHOR FOCAL ---------------------------------- #
if (exibirFocal):
    # Todas as particulas comparando o melhor valor global delas com o valor da particula foco
    # Realiza a Operação de achar o melhor focando em uma particula:
    listaFitnessFocal = []
    particulasTFocal = clone(particulas)

    particulaSelecionada = random.randrange(0, qtParticulas-1) #Seleciona um particula aleatoriamente para ser o foco
    melhorGlobalF = copy.copy(melhorGlobal)

    for i in range(0, iteracoes):
        #O melhor global sempre será a posição dessa particula

        for particula in particulasTFocal:
            if (particula == particulasTFocal[particulaSelecionada]):
                melhorGlobalF = particula.mover(melhorGlobalF)
            else:
                melhorGlobalF = particula.mover(melhorGlobalF, particulasTFocal[particulaSelecionada].posicao)   #Move a particula atual

        fitnessMelhorFocal = funcao(melhorGlobalF)
        listaFitnessFocal.append(fitnessMelhorFocal) #Adiciona o fitness do melhor global na topologia focal para gerar o grafico
        print("Iteração: ", i+1, '|Fitness Melhor Resultado [Focal]:', fitnessMelhorFocal)

        melhorGlobal = particulasTFocal[particulaSelecionada].posicao

#------------------------------ MELHOR LOCAL ---------------------------------- #
if (exibirLocal):
    # Todas as particulas comparando o melhor vlaor encontrado entre elas e seu vizinho anterior e próximo
    #Realiza a Operação de achar o melhor focando na particula P1:
    listaFitnessLocal = []
    particulasTLocal = clone(particulas)
    fitnessMelhorGlobal = 99999999999

    for i in range(0, iteracoes):
        #O melhor global sempre será a posição dessa particula

        for posicao in range(len(particulasTLocal)):
            melhorEncontrado = melhorLocal(particulas, posicao, qtParticulas, funcao) #Melhor posição entre o anterior, atual e próximo
            melhorEncontrado = particulas[posicao].mover(melhorEncontrado) #retorna a melhor posiçaõ ao mover
            if funcao(melhorEncontrado) < fitnessMelhorGlobal: #Se a posição for melhor que o melhor de todos já atualiza
                fitnessMelhorGlobal = funcao(melhorEncontrado) 

        listaFitnessLocal.append(fitnessMelhorGlobal) #Adiciona o fitness do melhor global na topologia focal para gerar o grafico
        print("Iteração: ", i+1, '|Fitness Melhor Resultado [Local]:', fitnessMelhorGlobal)



#Plota o gráfico
legendas = []
if (exibirGlobal):
    legendas.append('Global')
    plt.plot(listaFitnessGlobal)
if (exibirFocal):
    legendas.append('Focal')
    plt.plot(listaFitnessFocal)
if (exibirLocal):
    legendas.append('Local')
    plt.plot(listaFitnessLocal)


plt.legend(legendas, loc='upper right')

plt.xlabel('Iterações')
plt.ylabel('Fitness')
plt.show()