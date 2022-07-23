import random
import pickle
from time import sleep

vocab = {}

man = [
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """,
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """
]

def save_data_to_file(filename, data):
    """Saves data to a file in the same directory using pickle.
    Args:
        filename ([str]): Name of file in the same directory
        data ([dict]): Dictionary containing the data to save
    """
    with open(filename, "wb") as file:
        file.seek(0)
        pickle.dump(data, file)

def load_data_from_file(filename):
    """Loads data from a file in the same directory using pickle.
    Creates a file if it doesn't exist.
    Args:
        filename ([str]): Name of file in the same directory
    Returns:
        [dict]: Dictionary containing the data imported
    """
    file_data = {}
    try:
        with open(filename, "rb") as file:
            file.seek(0)
            file_data = pickle.load(file)
    except IOError:
        print(filename, "doesn't exist, creating")
        save_data_to_file(filename, file_data)
    finally:
        return file_data

def create_input(prompt):
    """Returns a stylised prompt.
    Args:
        prompt ([string]): Prompt string to seek user input
    Returns:
        [str]: The user input
    """
    return input(prompt).upper().strip()

class Game:
    """A class to represent an instantiated VocaHangman game.
    Args:
        answer (str): Answer to the Hangman game
    """
    vowels = ['A', 'E', 'I', 'O', 'U']

    def __init__(self, answer):
        self._answer = answer
        self._wrong = 0
        self._correct = 0
        self._max_wrong_tries = 6
        self._word = "-" * len(answer)

    def get_answer(self):
        """Gets the answer that the players have to guess.
        Returns:
            [str]: Answer string
        """
        return self._answer

    def get_guess_word(self):
        """Gets the current guess string.
        Returns:
            [str]: Guess string e.g "---A---"
        """
        return self._word
    
    def get_correct_guesses(self):
        """Number of correct guesses by the player.
        Returns:
            [int]: Number of correct guesses
        """
        return self._correct
    
    def get_wrong_guesses(self):
        """Number of wrong guesses by the player.
        Returns:
            [int]: Number of wrong guesses
        """
        return self._wrong

    def increment_correct_guesses(self):
        """Increments the number of correct guesses by the player.
        """
        self._correct += 1

    def increment_wrong_guesses(self):
        """Increments the number of wrong guesses by the player.
        """
        self._wrong += 1
    
    def has_ended(self):
        """Determines if the game has ended due to completion, or too many incorrect guesses
        Returns:
            [bool]: Boolean of whether the game has ended
        """
        return self._wrong >= self._max_wrong_tries or self._correct >= self.get_total_correct_guesses()
    
    def update_guess_word(self, character):
        """Updates the player's guess with the correct character they entered
        Args:
            character ([str]): Correct character in the word
        """
        curr_guess = self.get_guess_word()
        ans = self.get_answer()
        new_guess = ""
        for i in range(len(ans)):
            if character == ans[i]:
                new_guess += character
            else:
                new_guess += curr_guess[i]
        self._word = new_guess
    
    def get_total_correct_guesses(self):
        """Total number of correct guesses, determined by the length of the answer
        Returns:
            [int]: The total number of correct guesses
        """
        return len(self._answer)

    def guess_letter(self, character):
        """Guesses a character, returns a boolean on whether the character is in the answer
        Args:
            character ([str]): Character to guess
        Returns:
            [bool]: Whether the character is in the answer
        """
        ans = self.get_answer()
        if character in ans and character not in self.get_guess_word():
            self.update_guess_word(character)
            self.increment_correct_guesses()
            return True
        elif character not in self.get_guess_word():
            if not character in self.vowels:
                self.increment_wrong_guesses()
            return False
    
    def get_score(self):
        """Gets the current score of the game
        Returns:
            [int]: Game score
        """
        return int((self._correct/self.get_total_correct_guesses()) * 100)

def educator():
    """
    Opens the menu for the Educator.
    """
    vocab_old = load_data_from_file("words.dat")
    
    while True:
        ask2 = create_input("Do you wish to enter a word(Y/N): ")
        print()
        if ask2 == "Y":
            print("Enter a word and its synonym: ")
            word = create_input("Enter word: ")
            synonym = create_input("Enter synonym: ")

            if not word.isalpha() or not synonym.isalpha():
                print("Enter a valid input !!")
                continue
                
            vocab[word] = synonym
        elif ask2 == "N":
            print("Exiting Program!!")
            break            
        else:
            print("Enter a valid input !!")
        print()

    vocab.update(vocab_old)

    while True:
        ask3 = create_input("Do you wish to make changes to words entered(Y/N): ")
        if ask3 == "Y":
            print("Select the word you wish to make changes on: ")
            for i in vocab:
                print(i, ":", vocab[i])
            word_for_change = create_input("Enter the word you wish to change: ")
            new_word = create_input("Enter the new word: ")
            synonym_for_change = create_input("Enter synonym for the word: ")
            del vocab[word_for_change]
            vocab[new_word] = synonym_for_change
        elif ask3 == "N":
            print("Exiting Program!!")
            break
        else:
            print("Enter a valid input !!")
        print()  

    save_data_to_file("words.dat", vocab)

def student():
    """
    Opens the menu for the Student.
    """
    student_name = create_input("Enter username or enter 'quit' to exit: ")
    if student_name == "QUIT":
        print("Quitting !!")
        return 
    if student_name == "":
        print("Invalid Input !!")
        return
    print("Welcome ", student_name)    
    print()

    vocab = load_data_from_file("words.dat")

    scores = []
    student_scores = {}

    student_scores = load_data_from_file("scores.dat")
    if student_name in student_scores:
        print("Username entered exists !!")
        p = create_input("Enter P if you are new to the game, or press any key to continue as {}: ".format(student_name))
        if p == "P":
            print("Returning to previous menu !!")
            return
        print()
        scores = student_scores[student_name]
    else:
        scores = []
    
    while True:
        s = create_input("Enter S to check scores for all games, Press any key to continue: ")
        
        if s == "S":
            if scores == []:
                print("You have not played any games until now !!")
                print()
            else:
                for i in range(len(scores)):
                    print("Game {}: {}".format(i+1, scores[i]))
                print()
        print()          
        play = create_input("Do you wish to play Vocahangman(Y/N): ")
            
        if play == "Y":
            words = list(vocab.keys())
            if len(words) == 0:
                print("There aren't any words to guess. Get an Educator to add some!")
                print("Exiting Program !!")
                break
            correct_word = random.choice(words)
            synonym_shown = vocab[correct_word]

            sleep(1)
                
            print('''
            Welcome to Vocabulary with Hangman
            Rules:
            1. You will be given a synonym and you have to guess the correct vocabulary word.
            2. Standard Hangman rules apply, everytime a wrong letter is guessed, more 
               body parts are added to the man.
            3. You have only 6 tries to guess the word.
            4. Guessing vowels has no penalty.
            5. While guessing, you can enter letters ONLY.
            6. 100 points are awarded for each word guessed correctly.
            7. Partial score is awarded for partially guessing the word.''')
            print()
            sleep(1)

            game = Game(correct_word)
            
            print(game.get_guess_word())
            print(man[game.get_wrong_guesses()])

            sleep(1)
            while True:
                sleep(1)
                print("Synonym: ", synonym_shown)

                print("Enter your guess to play or enter 'quit' to exit")
                guess = create_input("Enter Letter: ")
                sleep(1)
                print()

                if guess == "QUIT":
                    score = 0
                    scores.append(score)
                    print("Quiting !!")
                    print()
                    break
            
                if guess.isalpha() == False:
                    print("Invalid input !! Try Again !!")
                    print()
                    continue 
                
                if len(guess)>1:
                    print("Invalid input !! Try Again !!")

                else:
                    if game.guess_letter(guess):
                        print("Your guess is in the word !!")
                    else:
                        print("{} is not in the word!".format(guess))
                        print("Try Again !!")
                    print()
                
                print()
                sleep(1)
                print(game.get_guess_word())
                #sleep(1)
                print(man[game.get_wrong_guesses()])

                score = game.get_score()
                if correct_word == game.get_guess_word():
                    print("Congratulations on guessing the correct word !!")
                    print("Final Score: {}".format(score))
                    print("Enter 'Y' to play again, Enter 'N' to quit !!")
                    print()
                    scores.append(score)
                    break

                if game.has_ended():
                    print("You have not guessed the word correctly, better luck next time !!")
                    print("The word is: {}".format(correct_word))
                    print()
                    
                    print("Final Score: {}".format(score))
                    print("Enter 'Y' to play again, Enter 'N' to quit !!")
                    print()
                    scores.append(score)
                    break

                print("Current Score: {}".format(score))
                print()
                #sleep(1)

        
        elif play == 'N':
            print("Exiting Game !!")
            print()
            break

        else:
            print("Enter a valid input !!")
            print()
            continue

    student_scores[student_name] = scores
    save_data_to_file("scores.dat", student_scores)

def main():
    """Main menu function
    """
    print()
    print("             Welcome to Vocahangman                 ")
    print()

    ask = create_input("Are you an Educator or a Student(E/S), Press Q to exit: ")
    print()

    if ask == "E":
        educator()

    elif ask == "S":
        student()
            
    elif ask == "Q":
        print("Exiting Program !!")

    else:
        print("Enter a valid input !!")

if __name__ == "__main__":
    main()