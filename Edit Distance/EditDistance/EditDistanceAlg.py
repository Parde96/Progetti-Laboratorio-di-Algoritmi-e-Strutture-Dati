from math import inf  # infinito
from NGramJaccard import *
from math import floor

"""
Per fare l'edit distance con ngram si suppone di avere già caricato in memoria una lista con tutti gli ngram per tutte 
le parole, infatti nel costruttore li si vanno a mettere nella variabile ngrams_list
"""


class Edit:

    def __init__(self, delete, insert, copy, replace, swap):
        self.delete = delete
        self.insert = insert
        self.copy = copy
        self.replace = replace
        self.swap = swap
        create_ngrams_from_file()
        self.ngrams_list = []  # lista di ngram nel file in ordine: 0 = 1-gram, 1 = 2-gram, ..., da usare in ED-ngram
        next_words = True
        list_pos = -1
        n_ngram_number = 0
        with open("NGrams List.txt", 'r') as txt:
            for line in txt:
                if line == str(n_ngram_number + 1) + ':\n':
                    next_words = True
                    n_ngram_number += 1
                if not next_words:
                    index = 0
                    while line[index] != '=':
                        index += 1
                    grams = []
                    step = n_ngram_number + 2
                    for i in range(len(line[:index + 3]), len(line) - 1, step):
                        grams.append(line[i:i + n_ngram_number])
                    grams = Multiset(grams)
                    line = line[0:index - 1]
                    self.ngrams_list[list_pos].append({line: grams})
                else:
                    self.ngrams_list.append([])
                    list_pos += 1
                    next_words = False

    def correction_word(self, word):
        with open("1160 parole italiane.txt", 'r', encoding='utf-8') as txt:
            words_cost_list = []
            for line in txt:
                if '\n' in line:
                    line = line[0:len(line) - 1]
                c, op = self.edit_distance(word, line)
                index = c[len(word)][len(line)]
                insert_in_list(words_cost_list, index, line, "edit")
            # print(words_cost_list)
            # found = False
            i = 0
            """
            while not found and i < len(words_cost_list):
                if len(words_cost_list[i]) != 0:
                    found = True
                    if i == 0:
                        # se zero allora dovrebbe appartenere ma si controlla, siamo sicuri serva? Se non appartiene
                        # non dovrebbe succedere
                        if word in words_cost_list[i]:
                            # print("The word is correct")
                            return True
                        else:
                            # print("Word not in lexicon")
                            return False
                    else:
                        # possible_corrections = "Possible corrections:\n"
                        # for j in range(len(words_cost_list[i])):
                        #    possible_corrections += words_cost_list[i][j] + "\n"
                        # print(possible_corrections)
                        # print("The cost is: " + str(i))
                        return words_cost_list, i
                else:
                    i += 1
            if not found:
                print("Word not in lexicon")
                return False
            """
            # trovo la prima lista di parole non vuota, sarà la lista di parole che ha dato il costo minimo
            while len(words_cost_list[i]) == 0 and i < len(words_cost_list):
                i += 1
            if i == 0:
                return True, i
            elif i == len(words_cost_list):
                return False, i
            else:
                return words_cost_list, i

    def correction_word_ngram(self, word):
        n = ceil(len(word) / 3)
        """
        n = floor(len(word) / 3)
        if n == 0:
            n = 1
        """
        # log = open("log.txt", 'a+')
        # log.write(str(n) + " " + str(len(self.ngrams_list)) + "\n")
        corresponding_ngrams = self.ngrams_list[n - 1]
        word_ngram = ngram(n, word)
        to_compare = []
        for i in range(len(corresponding_ngrams)):
            key = list(corresponding_ngrams[i].keys())[0]
            if jaccard_coefficient(word_ngram, corresponding_ngrams[i][key]) >= 0.4:
                to_compare.append(key)
        words_cost_list = []
        # questo ciclo poteva essere compreso dopo l'if di Jaccard probabilmente
        for i in range(len(to_compare)):
            compare_word = to_compare[i]
            c, op = self.edit_distance(word, compare_word)
            index = c[len(word)][len(compare_word)]
            insert_in_list(words_cost_list, index, compare_word, "edit")

        i = 0
        if len(words_cost_list) != 0:
            while len(words_cost_list[i]) == 0 and i < len(words_cost_list):
                i += 1
            if i == 0:
                return True, i
            elif i == len(words_cost_list):
                return False, i
            else:
                return words_cost_list, i
        else:
            return False, i

    def correction_word_with_fixed_n(self, n, word_to_correct, correct_words):
        to_correct_ngram = ngram(n, word_to_correct)
        # correct_ngrams = []
        # to_compare = []
        words_cost_list = []
        for word in correct_words:
            # correct_ngrams.append(ngram(n, correct_words[i]))
            correct_ngram = ngram(n, word)
            if jaccard_coefficient(to_correct_ngram, correct_ngram) > 0.7:
                # to_compare.append(word)
                c, op = self.edit_distance(word_to_correct, word)
                index = c[len(word_to_correct)][len(word)]
                insert_in_list(words_cost_list, index, word, "edit")
        i = 0
        if len(words_cost_list) != 0:
            while len(words_cost_list[i]) == 0 and i < len(words_cost_list):
                i += 1
            if i == 0:
                return True, i
            elif i == len(words_cost_list):
                return False, i
            else:
                return words_cost_list, i
        else:
            return False, i

    def edit_distance(self, x, y):
        m = len(x)
        n = len(y)
        c = []
        op = []
        for i in range(m + 1):
            c.append([])
            op.append([])
            for j in range(n + 1):
                c[i].append(None)
                op[i].append(None)
        for i in range(m + 1):
            c[i][0] = i * self.delete
            op[i][0] = "delete"
        for i in range(n + 1):
            c[0][i] = i * self.insert
            op[0][i] = "insert"
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                c[i][j] = inf
                if x[i - 1] == y[j - 1]:
                    c[i][j] = c[i - 1][j - 1] + self.copy
                    op[i][j] = "copy"
                if x[i - 1] != y[j - 1] and c[i - 1][j - 1] + self.replace < c[i][j]:
                    c[i][j] = c[i - 1][j - 1] + self.replace
                    op[i][j] = "replace by " + y[j - 1]
                if i >= 2 and j >= 2 and x[i - 1] == y[j - 1 - 1] and x[i - 1 - 1] == y[j - 1] and c[i - 2][
                    j - 2] + self.swap < c[i][j]:
                    c[i][j] = c[i - 2][j - 2] + self.swap
                    op[i][j] = "swap"
                if c[i - 1][j] + self.delete < c[i][j]:
                    c[i][j] = c[i - 1][j] + self.delete
                    op[i][j] = "delete"
                if c[i][j - 1] + self.insert < c[i][j]:
                    c[i][j] = c[i][j - 1] + self.insert
                    op[i][j] = "insert " + y[j - 1]
        return c, op

    def op_sequence(self, op, i, j):
        if i == 0 and j == 0:
            return
        if op[i][j] == "copy" or op[i][j][0:7] == "replace":
            i1 = i - 1
            j1 = j - 1
        elif op[i][j] == "swap":
            i1 = i - 2
            j1 = j - 2
        elif op[i][j] == "delete":
            i1 = i - 1
            j1 = j
        else:
            i1 = i
            j1 = j - 1
        self.op_sequence(op, i1, j1)
        print(op[i][j])





























