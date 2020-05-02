import os
alien = Actor('alien')
alien.topright = 0, 600

def say(phrase):
    os.system("say '{}'".format(phrase))

WIDTH = 900
HEIGHT = alien.height + 600

# this is what the program calls when you first start the game
# it clears the screen and draws the alien in the position 0, 600
def draw():
    screen.clear()
    alien.draw()

# this is what the program calls to update the screen and move the alien
def update():
    # every time move the alien by 10
    alien.left += 1
    # if he gets to the end of the screen, put him back at the begining
    if alien.left > WIDTH:
        alien.right = 0

# this is what the program calls when you press your mouse
def on_mouse_down(pos):
    # this is true if the alien is hit
    if alien.collidepoint(pos):
        set_alien_hurt()
    else: # otherwise, you missed
        say('hi')

# what sets the alien to hurt
def set_alien_hurt():
    say('eep')
    alien.image = 'alien_hurt' # make the alien look sad
    #sounds.eep.play() # play the alien hurt noise
    # in 1 second call the function set_alien_normal which makes him happy again

    clock.schedule_unique(set_alien_normal, 0.5)

# makes the alien happy again
def set_alien_normal():
    alien.image = 'alien'
