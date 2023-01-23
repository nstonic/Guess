import os
import random
from string import ascii_lowercase

import argparse


def get_rand_word(filename: str) -> str:
    os.chdir(os.path.dirname(__file__))
    with open(filename) as file:
        return random.choice([line.strip() for line in file]).lower()


def print_turn(target_word: str, guessed_letters: list[str], wrong_guesses: list):
    print('\nWrong guess:', ', '.join(wrong_guesses))
    print(' '.join([letter if letter else ' ' for letter in guessed_letters]))
    masked_word = [character if character == ' ' else '-' for character in target_word]
    print(' '.join(masked_word))


def get_letter(attempts: int, previous_guesses: list[str]) -> str:
    user_guess = input(f'> Guess a letter ({attempts} attempts left): ').lower()
    if len(user_guess) != 1 or user_guess not in ascii_lowercase:
        print("> Please input a letter!")
    elif user_guess in previous_guesses:
        print(f"> You have guessed '{user_guess}' before")
    else:
        return user_guess


def main(target_word: str):
    attempts = 6
    previous_guesses = []
    wrong_guesses = []
    guessed_letters = [letter if letter == ' ' else None for letter in target_word]
    while attempts > 0:
        print_turn(target_word, guessed_letters, wrong_guesses)
        if None not in guessed_letters:
            print('> You win!')
            break
        user_letter = get_letter(attempts, previous_guesses)
        if user_letter is not None:
            if user_letter not in guessed_letters:
                wrong_guesses.append(user_letter)
                attempts -= 1
            else:
                for index, letter in enumerate(target_word):
                    if user_letter == letter:
                        guessed_letters[index] = user_letter
                previous_guesses.append(user_letter)

    else:
        print_turn(target_word, guessed_letters, wrong_guesses)
        print('> You lose...')
        print(f'> Answer: {target_word.capitalize()}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sowpods',
                        default='sowpods.txt',
                        help='The name of the word file located in the sowpods folder')
    args = parser.parse_args()
    target_word = get_rand_word(os.path.join('sowpods', args.filename))
    main(target_word)
