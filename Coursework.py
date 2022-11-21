import pygame  # imports a module that allows a GUI to be opened
import secrets  # imports a module that allows pseudorandom numbers suitable for cryptographic purposes to be generated
import string  # imports a module that allows for a string containing of every single letter (upper and lowercase)
# to be generated
import os  # imports a module which allows for usage of pathways to files in different folders
from pynput.keyboard import *

keyboard = Controller()
vigernkey = open("vigernkey.txt", "r+")  # opens the text file for the key
finish_message = ""
ciphertext_file = open("cip.txt", "r+")  # opens the text file for the ciphertext
pygame.init()  # initialises the library that allows a GUI to be opened


# Encrypt subroutine:
def vigenere(x):
    ciphertext = []
    vigkey = []  # this declares the list which will store the key for each individual letter
    for letter in x:
        individualletterkey = secrets.choice(string.ascii_letters)  # this generates the key for each letter as a
        # random character in the ASCII set
        newletter = ord(letter) ^ ord(individualletterkey)  # This transforms the letters of the key and the
        # plaintext into numbers  and performs an XOR operation on the two to create the encoding of the ciphertext
        # character
        vigkey.append(individualletterkey)  # this stores the key of each letter in a list, so it can be passed on
        # to the intended recipient for decryption
        ciphertext.append(newletter)  # this adds the newly encrypted letter to the ciphertext
    for element in vigkey:  # this loop ensures that the key for every letter is in a text file that can be passed
        # on to the intended recipient for them to decrypt the ciphertext
        vigernkey.write(str(element))
        vigernkey.write("\n")  # Each character in the key will be stored in an individual line
    for element in ciphertext:
        ciphertext_file.write(str(element))  # Each character in the ciphertext will be stored in a line in a file
        ciphertext_file.write("\n")
    global finish_message
    finish_message = "The key is in the file vigernkey.txt, and the ciphertext is in the file cip.txt"
    return ciphertext, finish_message


# Decrypt subroutine:
def vigenere_decrypt(y):
    y = [int(x) for x in y]
    Plaintext = ""  # this declares the plaintext variable
    vigkey = vigernkey.read().splitlines()
    for i in range(len(y)):
        newletter = chr(y[i] ^ ord(vigkey[i]))
        Plaintext += newletter  # this adds each newly decrypted character to the Plaintext
    return Plaintext


# GUI creation:
WIDTH, HEIGHT = 900, 500  # this declares the size of the window the GUI will open in
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vigenere cipher")  # this titles the window
FPS = 60  # this declares the  magnitude of the framerate of the window
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Button:  # This class will be used as buttons to allow the user to make selections in the program

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):  # This method allows the button to draw itself on the screen
        WIN.blit(self.image, (self.rect.x, self.rect.y))

    def isclicked(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(x, y):
                return 1
            else:
                return 0


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = WHITE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.colour)
        self.active = False
        self.done = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            self.colour = WHITE if self.active else BLUE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.done = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.colour)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.colour, self.rect, 2)


FONT = pygame.font.Font(None, 32)

encryptimg = pygame.image.load(os.path.join("Assets", "Encrypt_button.png"))  # This line and the next contain the
# images that will be the program's buttons and allow them to be utilised in the programs
decryptimg = pygame.image.load(os.path.join("Assets", "Decrypt_button.png"))

encrypt_button = Button(100, 150, encryptimg)  # These following two lines create the buttons to select the two main
# subroutines
decrypt_button = Button(550, 150, decryptimg)

textbox = InputBox(100, 100, 140, 32)
GREY = (54, 45, 45)


def draw_window():  # this function colours the window
    WIN.fill(GREY)  # this colours the window grey
    encrypt_button.draw()
    decrypt_button.draw()
    pygame.display.update()  # this updates the colouring of the window the next time the frame cycles


def reset_window():  # this functions draws a version of the window with a textbox instead of buttons
    WIN.fill(GREY)
    textbox.draw(WIN)
    pygame.display.update()


def Coursework():  # the application loop that all pygame programs require to function
    clock = pygame.time.Clock()  # this creates a variable, that, when a value is assigned to it, it will be the
    # refresh rate of the application
    run = True
    encrypt = False
    decrypt = False
    finished = False
    draw_window()
    while run:  # everything in this loop will only happen when the window is open
        clock.tick(FPS)  # this refreshes the frame every 1/FPS seconds, setting a framerate for the program
        for event in pygame.event.get():  # the event loop that ensures that any events are properly managed
            if event.type == pygame.QUIT:
                run = False  # this closes the window if the user quits the program
            textbox.handle_event(event)
            if encrypt_button.isclicked(event) == 1:  # The two following loops create a text box on the screen
                # when one of the options is chosen
                reset_window()
                encrypt = True
            if decrypt_button.isclicked(event):
                reset_window()
                decrypt = True

        if finished:
            reset_window()
            if encrypt:
                textbox.txt_surface = FONT.render(finish_message, True, textbox.colour)
                encrypt = False
                textbox.active = False
                textbox.done = False
            elif decrypt:
                textbox.txt_surface = FONT.render(decr_text, True, textbox.colour)
                decrypt = False
                textbox.active = False
                textbox.done = False


        if encrypt:  # the following code encrypts the user input and outputs a message onto the screen
            ciphertext_file.truncate(0)
            vigernkey.truncate(0)
            vigernkey.seek(0)
            ciphertext_file.seek(0)
            reset_window()
            textbox.update()
            if textbox.done:
                encr_text = vigenere(textbox.text)
                print(textbox.text)
                finished = True

        elif decrypt:  # the following code decrypts the contents of cip.txt and outputs the result onto the screen
            reset_window()
            textbox.update()
            if textbox.done:
                ciphtext = ciphertext_file.read().splitlines()
                decr_text = vigenere_decrypt(ciphtext)
                textbox.txt_surface = FONT.render(decr_text, True, textbox.colour)
                print(textbox.text)
                finished = True

    pygame.quit()


if __name__ == "__main__":  # this ensures that the GUI will open when this specific program is running
    Coursework()
