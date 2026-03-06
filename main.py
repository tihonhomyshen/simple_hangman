import random


def choose_word() -> str:
    words = []
    with open("words.txt", "r", encoding="UTF-8") as file:
        for line in file:
            words.append(line.rstrip("\n"))
    word = random.choice(words)
    return word


def output_stat(word_state: list[str], used: list[str],
                bad_symbols: list[str], attempts: int) -> None:
    print(*word_state)
    print("Использованные буквы:", *used)
    print("Буквы, которых нет в слове:", *bad_symbols)
    print("Осталось попыток:", 6 - attempts)


def handle_input(user_input : str) -> bool:
    if (('а' <= user_input <= 'я' or 'А' <= user_input <= 'Я')
            and len(user_input) == 1):
        return True
    print("Некорректный ввод. Введите ещё раз")
    return False


def draw_hangman(attempt: int):
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
        """
    ]
    print(hangman[attempt])


def init_game() -> None:
    word = choose_word()
    word_state = ["_" for _ in range(len(word))]
    used_symbols = []
    bad_symbols = []
    try_cnt = 0
    guessed_cnt = 0
    output_stat(word_state, used_symbols, bad_symbols, try_cnt)
    while try_cnt < 6:
        user_input = input()
        changed = 0
        if handle_input(user_input):
            user_input = user_input.lower()
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
        if guessed_cnt == len(word):
            win(word)
            break
        if try_cnt == 6:
            lose(word)
            break


def win(word) -> None:
    print(f"Победа! Загаданное слово: {word}")


def lose(word) -> None:
    print(f"Поражение! Загаданное слово: {word}")


init_game()
