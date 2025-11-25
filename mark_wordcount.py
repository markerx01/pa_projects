import sys

__author__ = 'mark'

def main():
    filename = input('Enter file name (of the book, e.g. alice.txt): ').strip()
    choice = input('Would you like only the first 20 most common words, or all the words? (first/all): ').strip().lower()
    output_name = input('Enter output file name (where the word counts will be written): ').strip()

    words = words_count(filename)
    sorted_words_list = sort_words(words)

    if choice == 'first':
        write_result(sorted_words_list[:20], output_name)
        print(f'Top 20 words saved to {output_name}')
    elif choice == 'all':
        write_result(sorted_words_list, output_name)
        print(f'All words saved to {output_name}')
    else:
        print('Invalid choice. Please type first or all.')


def words_count(filename):
    with open(filename, 'r', encoding='utf-8') as book:
        words = {}
        for line in book:
            temp_line = clear_line(line)
            words_in_line = temp_line.split()
            for word in words_in_line:
                word = word.lower()
                if word:
                    words[word] = words.get(word, 0) + 1
    return words


def clear_line(line):
    invalid = [',', '.', '?', ':', ';', '!', '-', '"', "'", '(', ')', '[', ']', '{', '}', '*', '/', '\\']
    for char in invalid:
        line = line.replace(char, ' ')
    return line.strip()


def sort_words(words):
    # returns list of tuples sorted by count (from biggest to smallest)
    return sorted(words.items(), key=lambda x: x[1], reverse=True)


def write_result(sorted_words_list, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for word, count in sorted_words_list:
            file.write(f'{word}: {count}\n')


if __name__ == '__main__':
    main()
