'''
la matrice può avere 3 diverse cifre    0 cella senza nulla 1 cella con corpo dello snake 2 frutto da mangiare
lista per tenere in memoria la posizione dello snake
ogni volta che lo snake mangia un frutto la lista si allunga di un elemento
ogni volta che lo snake si muove si elimina l ultimo elemento della lista, aggiornando quella casela del plot e aggiornando la nuova casella
(aggiunta interessante, prima di eliminare ultima casella dello snake si può controllare se lo snake si ingrandisce così che
se lo fa non devi ridipingerla con lo sfondo ma la lasci come se fosse una parte dello snake)
generazione randon dei frutti con annesso controllo se spawnano sul corpo dello snake, basta rimuovere le caselle del corpo dello snake da quelle generabili randomicamente
(idea interessante da trovare per non scorrere tutta la lista dello snake per vedere se poso generarlo o meno,
ma alla fine sarebbe grande solo se lo snake diventa grande come tutta la matrice)
serve uno score da dare alla AI se no non funziona bene
tanto il tempo di computazione sarebbe abbastanza veloce possiamo rendere il movimento dello snake basato sulla pressione del tasto corrispondente e non come magari in altri giochi che si
muove sempre senza aspettare la pressione del tasto
idea avanzata, l AI vede sempre la posizione di tutto lo snake ovvero la lista delle sue parti e il frutto che di volta in volta si viene a generare
'''
import pygame
import numpy as np
from random import randint

# dimensione lato campo di gioco
dimension = 15

fruit_value = 2
snake_value = 1

cellsize = 50
col_fruit   = (255, 0, 0)
col_snake   = (255, 255, 255)
col_grid    = (255, 255, 255)
col_background = (0, 0, 0)

# salva la posizione del frutto
fruit = ()
last_move = ()
surface = None
score = 0

def spawn_fruit(matrix: np.array, snake: list):
    found = False
    while not found:
        i = randint(0, dimension - 1)
        j = randint(0, dimension - 1)

        if (i, j) not in snake:
            matrix[i][j] = fruit_value
            global fruit
            fruit = (i, j)
            found = True


def print_GUI(matrix: np.array, snake: list):
    surface.fill(col_grid)

    for i in range(dimension):
        for j in range(dimension):
            if matrix[i][j] == snake_value:
                col = col_snake

            elif matrix[i][j] == fruit_value:
                col = col_fruit

            else:
                col = col_background

            # stampa la cella corrente
            pygame.draw.rect(surface, col, (j*cellsize, i*cellsize, cellsize-1, cellsize-1))

    pygame.display.update()

# 0 posizione accettabile
# 1 impatto
# 2 rifare input
# 3 mangia frutto


def move(matrix, snake, mossa):
    def check_move(matrix, snake, new_position):
        print(last_move, new_position)
        if new_position[0] < 0 or new_position[0] > dimension-1 or new_position[1] < 0 or new_position[1] > dimension-1:
            return 1
        elif new_position == snake[-2]:
            return 2
        elif new_position in snake:
            return 1
        elif new_position == fruit:
            return 3
        else:
            return 0

    result = check_move(matrix, snake, mossa)
    # global last_move

    i, j = mossa

    if result == 0:
        global last_move
        last_move = mossa
        # disegna nuova testa
        pygame.draw.rect(surface, col_snake, (j*cellsize, i*cellsize, cellsize-1, cellsize-1))

        # elimina l'ultima cella dello snake
        i_snake, j_snake = snake[0]
        pygame.draw.rect(surface, col_background, (j_snake*cellsize, i_snake*cellsize, cellsize-1, cellsize-1))

        # aggiunge la nuova cella dello snake
        snake.append(mossa)

        # rimuove l'ultia cella dello snake
        snake.pop(0)

        return True

    elif result == 1:
        print("Sei morto!")
        pygame.quit()
        exit()

    elif result == 2:
        print("Mossa invalida!")
        return False

    elif result == 3:
        global score
        last_move = mossa
        score += 1
        print(score)

        # disegna nuova testa
        pygame.draw.rect(surface, col_snake, (j*cellsize, i*cellsize, cellsize-1, cellsize-1))

        # aggiunge la nuova cella dello snake
        snake.append(mossa)

        # genera un nuovo frutto
        spawn_fruit(matrix, snake)

        # disegna un nuovo frutto
        i_fruit, j_fruit = fruit
        pygame.draw.rect(surface, col_fruit, (j_fruit*cellsize, i_fruit*cellsize, cellsize-1, cellsize-1))
        return True


def update(matrix, snake):
    found = False
    while not found:
        testa = snake[-1]
        user_input = input()

        if user_input.lower() == 'a':  # j-1
            found = move(matrix, snake, (testa[0], testa[1] - 1))

        elif user_input.lower() == 'd':  # j+1
            found = move(matrix, snake, (testa[0], testa[1] + 1))

        elif user_input.lower() == 'w':  # i-1
            found = move(matrix, snake, (testa[0] - 1, testa[1]))

        elif user_input.lower() == 's':  # i+1
            found = move(matrix, snake, (testa[0] + 1, testa[1]))

    pygame.display.update()


def main():
    global surface
    global last_move

    # inizializza pygame e il display
    pygame.init()
    surface = pygame.display.set_mode((dimension * cellsize, dimension * cellsize))
    pygame.display.set_caption("Typing Monkeys's Deepest Snake")

    alive = True

    # campo di gioco
    matrix = np.zeros(dimension*dimension).reshape(dimension, dimension)

    # struttura dati per tenere in memoria il serpente
    snake = [
        (
            (int(dimension/2), int(dimension/2))
        ),
        (
            int(dimension/2) - 1 , int(dimension/2)
        )

    ]


    last_move = snake[0]

    # aggiunge lo snake alla matrice
    matrix[snake[0][0]][snake[0][1]] = snake_value
    matrix[snake[1][0]][snake[1][1]] = snake_value

    # genera casualmente un frutto
    spawn_fruit(matrix, snake)

    print(score)

    # stampa l'interfaccia iniziale
    print_GUI(matrix, snake)

    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        update(matrix, snake)


if __name__ == "__main__":
    main()
