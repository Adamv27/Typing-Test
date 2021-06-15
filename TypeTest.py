import time
import random


class TypeTest:
    def __init__(self, length):
        self.words = get_word_list()
        self.current_test = ''
        self.length = length

        self.start_time = 0
        self.end_time = 0
        self.elapsed_time = 0

        self.index_on_line = 0
        self.current_letter_index = 0
        self.current_line = 0

        self.total_characters_typed = 0

        self.typed_letters = []
        self.incorrect_letters = []

        self.is_started = False
        self.is_complete = False

        self.text = []

        self.wpm = 0
        self.accuracy = 0
        self.errors = 0

    def start(self):
        self.is_started = True
        self.start_time = time.time()

    def end(self):
        self.is_complete = True
        self.end_time = time.time()
        self.is_started = False
        self.elapsed_time = round(self.end_time - self.start_time, 2)

        self.calculate_accuracy()
        self.calculate_wpm()

    def is_over(self) -> bool:
        if self.current_letter_index == len(self.current_test):
            return True
        return False

    def generate_test(self):
        random.shuffle(self.words)
        self.current_test = ' '.join(self.words[:self.length])
        print(self.current_test)

    def get_text(self):
        text = []
        max_line_size = 5
        test_size = self.length
        index = 0

        # Split up text to wrap it
        for line in range((test_size // max_line_size) + 1):
            text.append(self.current_test.split()[index:index + max_line_size])
            index += max_line_size
        return text

    def get_current_letter(self):
        return self.current_test[self.current_letter_index]

    def get_prev_letter(self):
        return self.current_test[self.current_letter_index - 1]

    def backspace(self):
        if self.current_letter_index > 0:
            # If user has deleted the incorrect letter
            if len(self.incorrect_letters) > 0:
                if [self.index_on_line - 1, self.current_line] == self.incorrect_letters[-1]:
                    self.incorrect_letters.pop(-1)
            self.current_letter_index -= 1
            self.typed_letters.pop(-1)
            self.index_on_line -= 1
            if self.index_on_line < 0 and self.current_line != 0:
                self.current_line -= 1
                # After deleting to a new line set current position on line to the end
                self.index_on_line = len(' '.join(self.text[self.current_line])) - 1

    def typed(self, key):
        self.total_characters_typed += 1
        # Any other key has been pressed
        self.typed_letters.append(key)
        self.current_letter_index += 1

        self.index_on_line += 1
        # Check if user has completed line to begin filling in next line
        if self.index_on_line > len(' '.join(self.text[self.current_line])):
            self.index_on_line = 0
            self.current_line += 1
        # Add index of incorrect letter to incorrect_letters
        if self.typed_letters[-1] != self.get_prev_letter():
            self.errors += 1
            self.incorrect_letters.append([self.index_on_line - 1, self.current_line])

    def calculate_wpm(self):
        minutes = self.elapsed_time / 60

        # Gross WPM is how fast you type with no error penalties.
        # In typing a word counts are 5 characters
        gross_wpm = (self.total_characters_typed / 5) / minutes

        # Net WPM is the most useful took in gauging typing abilities.
        # It is a measure of productivity not just speed as errors are
        # taken into account.
        uncorrected_errors = len(self.incorrect_letters)
        net_wpm = gross_wpm - (uncorrected_errors / minutes)
        self.wpm = net_wpm

    def calculate_accuracy(self):
        total_characters = self.total_characters_typed
        correct_characters = total_characters - self.errors

        # The percentage of correct entries out of the total entries typed
        accuracy = (correct_characters / total_characters) * 100
        self.accuracy = accuracy

    def get_wpm(self):
        return str(round(self.wpm, 2))

    def get_accuracy(self):
        return str(round(self.accuracy, 2))


def get_word_list():
    words = []
    with open('words.txt', 'r') as f:
        for word in f:
            words.append(word.strip().lower())
    return words
