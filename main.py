import random

from colorama import Fore, Style, init

from consts import MAX_ATTEMPTS

init()


def choose_word() -> str:
    """
    Выбирает случайное слово из файла и возвращает его
    """
    words = []
    with open("words.txt", "r", encoding="UTF-8") as file:
        for line in file:
            words.append(line.rstrip("\n"))
    word = random.choice(words)
    return word


def output_stat(
    word_state: list[str],
    used: list[str],
    bad_symbols: list[str],
    attempts: int,
) -> None:
    """
    Выводит статистику: состояние слова, использованные буквы,
     буквы которых нет в слове, кол-во попыток.
    """
    print(*word_state)
    print("Использованные буквы:", *used)
    print(Fore.RED + "Буквы, которых нет в слове:", *bad_symbols)
    print(Fore.MAGENTA + "Осталось попыток:", 6 - attempts)
    print(Style.RESET_ALL, end="")


def handle_input(user_input: str) -> bool:
    """
    Валидация пользовательской ввода, возвращает ОК - если
     введена одна буква русского алфавита.
    """
    if ("а" <= user_input <= "я" or "А" <= user_input <= "Я") and len(
        user_input
    ) == 1:
        return True
    print("Некорректный ввод. Введите ещё раз")
    return False


def draw_hangman(attempt: int) -> None:
    """
    Отрисовка виселицы взависимости от попытки
    """
    hangman = [
        """
         +---+
         |   |
             |
             |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
             |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
         |   |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
        /|   |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
        /|\\  |
             |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
        /|\\  |
        /    |
             |
        =========
        """,
        """
         +---+
         |   |
         O   |
        /|\\  |
        / \\  |
             |
        =========
        """,
    ]
    print(hangman[attempt])


def game() -> None:
    """
    Основной функционал игры
    """
    word = choose_word()
    word_state = ["_" for _ in range(len(word))]
    used_symbols = []
    bad_symbols = []
    try_cnt = 0
    guessed_cnt = 0
    output_stat(word_state, used_symbols, bad_symbols, try_cnt)
    while not game_over(guessed_cnt, try_cnt, word):
        user_input = input().lower()
        changed = 0
        if handle_input(user_input):
            if user_input in used_symbols:
                print("Уже была использована, введите ещё раз")
            else:
                for i in range(0, len(word)):
                    if user_input == word[i]:
                        word_state[i] = user_input
                        changed += 1
                if changed == 0:
                    try_cnt += 1
                    bad_symbols.append(user_input)
                    draw_hangman(try_cnt)
                used_symbols.append(user_input)
                output_stat(word_state, used_symbols, bad_symbols, try_cnt)
        guessed_cnt += changed


def game_over(guessed_cnt: int, try_cnt: int, word: str) -> bool:
    """
    Проверка на окончание игры
    """
    if guessed_cnt == len(word):
        print(
            "Победа! Загаданное слово "
            + Fore.CYAN
            + Style.BRIGHT
            + word
            + Style.RESET_ALL
        )
        return True
    if try_cnt == MAX_ATTEMPTS:
        print(
            "Поражение! Загаданное слово "
            + Fore.CYAN
            + Style.BRIGHT
            + word
            + Style.RESET_ALL
        )
        return True
    return False


game()
