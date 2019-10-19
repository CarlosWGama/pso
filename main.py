import numpy as np
import math
import random
import matplotlib.pyplot as plt


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
        vetor.append(random.randrange(-20, 20))
    return vetor


class Particula:
    def __init__(self, posicao, melhorIndividual, velocidade, melhorGlobal, w, funcao):
        """
        Parameters
        ----------
        posicao : array
            Posição Inicial da Particula
        melhorIndividual : array
            Melhor posição individual desta particula
        velocidade : array
            Velocidade da direção da particula
        melhorGlobal :
            Melhor posição global definida inicialmente
        w :
            Inercia
        funcao :
            Função para analisar o terreno do estudo e avaliar o fitness
        """
        #Ddados da Particula
        self.posicao = np.array(posicao)
        self.melhorIndividual = np.array(melhorIndividual)
        self.velocidade = np.array(velocidade)

        #Dados Globais
        self.melhorGlobal = np.array(melhorGlobal) 
        self.funcao = funcao
        #DEFININDO AS CONSTANTES
        self.r1 = self.r2 = 0.25 #Um valor aleatório entre 0 e 1, foi escolhido 0.25
        self.c1 = self.c2 = 2.05 #Comportamento da particula para melhor posição local (c1) global (c2)
        self.w = w #Valor da Inercia usada na velocidade ao mover a particular
    
    def mover(self, melhorPosicaoGlobal):        
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
        self.__novaVelocidade()

        #Move
        #novaPosicao = posicao + novaVelocidade
        self.posicao = self.posicao + self.velocidade

        #Retorna a melhor posição global
        return self.melhorGlobal

    def __novaVelocidade(self):
        """
        Define a nova Particula
        Formula:
            novaVelocidade = w*V + r1*c1*(melhorIndividual - posicao) + r2*c2*(melhorGlobal - posicao)
        """
        velocidadeMelhorI = self.r1*self.c1*(self.melhorIndividual-self.posicao) #Direção Velocidade Melhor Local
        velocidadeMelhorG = self.r1*self.c1*(self.melhorGlobal-self.posicao) #Direção Velocidade Melhor Global
        self.velocidade = self.w*self.velocidade + velocidadeMelhorI + velocidadeMelhorG

    def __acharMelhorPosicaoIndividual(self):
        """ Verifica se a posição atual é melhor do que antiga melhor individual """
        #Checa se já está na melhor posição local
        
        if (self.funcao(self.posicao) < self.funcao(self.melhorIndividual)):
            self.melhorIndividual = self.posicao

    def __acharMelhorPosicaoGlobal(self):
        """ Verifica se a posição atual é melhor do que antiga melhor global """
        #Checa se já está na melhor posição global
        if (self.funcao(self.posicao) < self.funcao(self.melhorGlobal)):
            self.melhorGlobal = self.posicao

######### -------------------- INICIO Q1 ----------------------  #################
print(" --------- QUESTÃO 1 ----------")
#Posição Inicial, Melhor Posição, Velocidade e Melhor Global
melhorGlobal = [5,5]
w = 1
funcao = sphere #sphere ou rastringin

particulas = [
    Particula([5,5], [5,5], [2,2], melhorGlobal, w, funcao), #x1
    Particula([8,3], [7,3], [3,3], melhorGlobal, w, funcao), #x2
    Particula([6,7], [5,6], [4,4], melhorGlobal, w, funcao), #x3
]   

print("a)")
print("Após 1 Iteração")
#Faz em cada particula
i = 1
for particula in particulas: 
    melhorGlobal = particula.mover(melhorGlobal)
    print('Particula X'+str(i), particula.posicao)
    i+= 1
    
print("\nb)")
print("A velocidade inicial da particula, define sua posição, porém essa será alterada de acordo com a posição do melhor resultado individual da particula e global. De forma que a formula abaixo vai definir a nova velocidade com a diração correta que a particular irá seguir: ")
print("novaVelocidade = w*v + c1*r1*(melhorLocal-posicao) + c2*r2*(melhorGlobal-posicao) \n")

print("Com a nova velocidade, será definido a nova posição da particula com a formula:")
print("novaPosicao = posicao + novaVelocidade")


print("\n\n --------- QUESTÃO 2 ----------")
#Inicia os dados
np.seterr(all='warn')
qtParticulas = 30 #Quantas particular criar
dimensoes = 30 #Qual a dimensão de cada particula
iteracoes = 1000 #Quantas iterações serão realizadas
w = 0.8
melhorGlobal = gerarVetor(dimensoes) #As melhor posição global
funcao = rastringin #sphere ou rastringin

#Crias a particulas
particulas = []
for i in range(qtParticulas):

    posicao = gerarVetor(dimensoes) #As posições de cada particula aleatóriamente
    melhorPosicao = gerarVetor(dimensoes) #Melhor posiçã ode cada particula aleatoriamente
    velocidade = gerarVetor(dimensoes) #Define a velocidade de cada particula de forma aleatória

    particulas.append(Particula(posicao, melhorPosicao, velocidade, melhorGlobal, w, funcao))

#Realiza a operação
listaFitnessGlobal = []
for i in range(1, iteracoes):
    
    for particula in particulas:
        melhorGlobal = particula.mover(melhorGlobal)
    
    fitnessMelhorGlobal = funcao(melhorGlobal)
    listaFitnessGlobal.append(fitnessMelhorGlobal) #Adiciona o fitness do melhor global para gerar o grafico
    print("Iteração: ", i, '|Fitness Melhor Resultado:', fitnessMelhorGlobal);

#Plota o gráfico
plt.plot(listaFitnessGlobal)
plt.xlabel('Iterações')
plt.ylabel('Fitness')
plt.show()

print(melhorGlobal)
