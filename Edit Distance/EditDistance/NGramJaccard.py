# il set non ci permette di avere duplicati e con le liste non si possono fare le operazioni insiemistiche per Jaccard
from multiset import *
from math import ceil  # se una parola nella divisione ha resto tra 0 e 1 restituisce 1
from math import floor
from os import path


def ngram(n, string):
    if n > len(string):
        return "Value n is bigger than string length!"
    # result = set()
    # result = []
    result = Multiset()
    in_range = True
    first_index = 0
    last_index = n
    while in_range:
        # result.add(string[first_index:last_index])
        # result.append(string[first_index:last_index])
        result.add(string[first_index:last_index])
        first_index += 1
        last_index += 1
        if last_index > len(string):
            in_range = False
    return result


def jaccard_coefficient(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    jaccard = len(intersection) / len(union)
    # per arrotondare alla prima cifra decimale, sennò ad esempio con "suboto" non trova nulla con cui correggere
    # jaccard = ceil(jaccard * 10)/10
    return jaccard


def create_ngrams_from_file():
    # lettura file
    if not path.exists("NGrams List.txt"):
        list_of_ngrams = []
        to_insert = ""
        with open("1160 parole italiane.txt", 'r', encoding='utf-8') as txt:
            for line in txt:
                if '\n' in line:
                    line = line[0:len(line) - 1]
                n = ceil(len(line) / 3)
                """
                n = floor(len(line) / 3)
                if n == 0:
                    n = 1
                """
                ngrams = ngram(n, line)
                word_and_ngram = {line: Multiset(ngrams)}
                """
                if to_insert == "":
                    to_insert += line[0:len(line) - 1] + ": "
                else:
                    to_insert += "\n" + line[0:len(line) - 1] + ": "
                for i in range(len(ngrams)):
                    to_insert += list(ngrams)[i] + ", "
                """
                # insert_in_list(list_of_ngrams, n, ngrams, "multiset")
                insert_in_list(list_of_ngrams, n, word_and_ngram, "ngram")
                ngrams.clear()
        for i in range(len(list_of_ngrams)):
            to_insert += str(i + 1) + ':\n'
            for j in range(len(list_of_ngrams[i])):
                # to_insert += str(list(list_of_ngrams[i])[j]) + '\n'
                key = list(list_of_ngrams[i][j].keys())[0]
                to_insert += key + " = {"
                for k in range(len(list_of_ngrams[i][j][key])):
                    if k == len(list_of_ngrams[i][j][key]) - 1:
                        to_insert += str(list(list_of_ngrams[i][j][key])[k]) + '}'
                    else:
                        to_insert += str(list(list_of_ngrams[i][j][key])[k]) + ', '
                to_insert += '\n'
            # to_insert += '\n'

        to_save = open("NGrams List.txt", 'a+')
        to_save.write(to_insert)


def insert_in_list(lista, index, value, caller):
    if caller == "multiset":
        if index > len(lista):
            to_insert = index - len(lista)
            for i in range(to_insert):
                lista.append([])
        lista[index - 1].append(Multiset(value))
    elif caller == "edit":
        if index + 1 > len(lista):
            """
            to_insert = index - len(lista) + 1
            for i in range(to_insert):
                lista.append([])
            """
            while len(lista) < index + 1:
                lista.append([])
        lista[index].append(value)
    else:
        if index > len(lista):
            to_insert = index - len(lista)
            for i in range(to_insert):
                lista.append([])
        lista[index - 1].append(value)
    # lista.pop(index - 1)
