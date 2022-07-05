
#This method is used to divide the single list of words to chunks from a to z
def word_preprocessing (word_list):
    file = open("words", "r", encoding="UTF-8")
    word = "words_"
    for words in file:
        words = words.lower()
        first_char = words[0]
        filename = word + str(first_char) + ".txt"

        try:
            file = open(filename, encoding="UTF-8")
            file.close()
        except OSError as e:
            file = open(filename, 'x', encoding="UTF-8")
            file.close()
        file = open(filename, 'a+', encoding="UTF-8")
        file.write(words)
        file.close()