import random
import os

min = 0
max = 999
right_number = random.randint(min, max)
right = False
a = 0
while( not right ):

    f = input('what do you want f to be? ')
    try:
        f = float(f.strip(' '))
    except:
        os.system("say 'you idiot, go back to preschool {} is not a number'".format(f))
        continue

    if (f < right_number):
        os.system("say 'WRONG! your guess is less than the right number'")
        a += 1
    if (f > right_number):
        os.system("say 'you are wrong go lower!'")
        a += 1
    if (f == right_number):
        os.system("say 'you won now stop looking at a screen its bad for your eyes'")
        right = True
    if (a == 10 ):
        print('Game Over')
        os.system("say 'i think you messed up'")
        exit()
