import matplotlib.pyplot as plt
import random
import string
import sys

from EditDistanceAlg import *
from NGramJaccard import *
from timeit import default_timer as timer
from random import randint
from statistics import mean

"""
COSA TESTARE:
parola in lessico e corretta, parola in lessico ma non corretta, parola corretta ma non in lessico
DIFFERENZE TROVATE:
-Quando si usa gli ngram potrebbero non essere corrette le parole a cui manca una lettera, esempio: car è correggibile
con caro ma non lo fa per via di come viene creato l'ngram, in particolare sarà un 1-gram, invece caro è un 2-gram e 
quindi non viene poi considerato perchè si vanno a prendere tutti gli 1-gram, invece con quello senza trova la 
correzione.
-Quando le parole sono già corrette l'ed con ngram ci mette di meno a terminare e verificare che effettivamente lo è.
-Con ngram anche se ci sono delle parole potenziali cadidate come correzioni non vengono considerate per via che hanno
un coefficiente di Jaccard basso. Es: subutu -> subito non trovato. (Con Jaccard >= 0.4, se arrotondiamo al decimo 
superiore trova qualcosa in più)
-Con ngram piccolo (ad esempio calcolandolo con la divisione per 4) più è probabile che trovi una correzione, anche con 
due lettere sbagliate, se si usa il /3 e il ceil ne trova solo con una lettera sbagliata

PRIMO TEST PAROLE NON IN LESSICO:
0.11381694427737479
0.004061516090668175

4.667120799273388
1.2496954933008526

PRIMO TEST PAROLE SBAGLIATE (NON COMPRESO DELLA LETTERA MANCANTE)
0.36566548465516935
0.014321554310342028

1.0189655172413794
1.0340632603406326
"""


def main():
    str1 = "Genoveffo"
    str2 = "Genoveffaaa"
    result1 = ngram(4, str1)
    print(result1)
    result2 = ngram(2, str2)
    print(result2)
    j = jaccard_coefficient(result1, result2)
    print(j)
    print()
    delete = 1
    insert = 1
    copy = 0
    replace = 1
    swap = 2
    edit_d = Edit(delete, insert, copy, replace, swap)
    c, op = edit_d.edit_distance(str1, str2)
    # print c table
    for i in range(len(str1) + 1):
        print(c[i])

    # print edit distance cost
    print(c[len(str1)][len(str2)])
    # print(c)
    # print(op)
    edit_d.op_sequence(op, len(str1), len(str2))


def draw_plot(results, test_name, word):
    # times = results[range(len(results))][0]
    plt.figure(constrained_layout=True, dpi=1200)
    # colors = ['g'] * len(results)
    times = []
    index = 0
    setted = False
    for i in range(len(results)):
        times.append(results[i][0])
        if results[i][1] is False and not setted:
            index = i
            setted = True
    if index == 0:
        # plt.plot(range(len(results)), times, marker='s', mfc='g', color='black')
        plt.plot(range(len(results)), times, color='black')
        plt.scatter(range(len(results)), times, marker='s', color='g')
    else:
        plt.plot(range(len(results)), times, color='black')
        plt.scatter(range(index), times[:index], marker='s', color='g')
        plt.scatter(range(index, len(results)), times[index:], marker='s', color='r')
    plt.title(test_name + ' - "' + word + '"')
    plt.xlabel("Indice N")
    plt.ylabel("Tempi")
    if test_name == "Correzione ultimo carattere":
        plt.savefig("Grafici test/Ultimo carattere/" + test_name + " - " + word)
    elif test_name == "Correzione primo carattere":
        plt.savefig("Grafici test/Primo carattere/" + test_name + " - " + word)
    elif test_name == "Correzione carattere centrale":
        plt.savefig("Grafici test/Carattere centrale/" + test_name + " - " + word)
    else:
        plt.savefig("Grafici test/Carattere mancante/" + test_name + " - " + word)


def test_ed(to_return, edit_d, words_to_test, edit_distance_times):
    # print("EDIT DISTANCE")
    start = timer()
    result, index = edit_d.correction_word(words_to_test)
    end = timer()
    edit_distance_times.append(end - start)
    # print_result(result, index)
    # if result:
    #    corrects += 1
    # return corrects
    if result is not True and result is not False:
        to_return.append(len(result[index]))


def test_ed_ngram(to_return, edit_d, words_to_test, edit_distance_ngrams_times):
    # print("EDIT DISTANCE WITH NGRAM")
    start = timer()
    result, index = edit_d.correction_word_ngram(words_to_test)
    end = timer()
    edit_distance_ngrams_times.append(end - start)
    # print_result(result, index)
    # if result:
    #    corrects += 1
    # return corrects
    if result is not True and result is not False:
        to_return.append(len(result[index]))


def test_ed_multiple_ngrams(n, word_to_correct, correct_words):
    delete = 1
    insert = 1
    copy = 0
    replace = 1
    swap = 2
    edit_d = Edit(delete, insert, copy, replace, swap)
    start = timer()
    result, index = edit_d.correction_word_with_fixed_n(n, word_to_correct, correct_words)
    end = timer()
    return [end - start, result]


def print_result(result, index):
    if result is True:
        print("The word is correct")
    elif result is False:
        print("No corrections found")
    else:
        possible_corrections = "Possible corrections:\n"
        for j in range(len(result[index])):
            possible_corrections += result[index][j] + "\n"
        print(possible_corrections)
        print("The cost is: " + str(index))


def correct_words_test():
    print("TEST PAROLE CORRETTE")
    # preparazione parole corrette da testare dal file
    correct_words_to_test = []
    file_words = []
    with open("1160 parole italiane.txt", 'r', encoding='utf-8') as txt:
        for line in txt:
            if '\n' in line:
                line = line[:len(line) - 1]
            file_words.append(line)
    length = int(len(file_words) / 2)
    rand_numbers_used = []
    rand = randint(0, length)
    for i in range(length):
        while rand in rand_numbers_used:
            rand = randint(0, len(file_words) - 1)
        rand_numbers_used.append(rand)
        correct_words_to_test.append(file_words[rand])

    delete = 1
    insert = 1
    copy = 0
    replace = 1
    swap = 2
    # word = "ciao"
    edit_d = Edit(delete, insert, copy, replace, swap)
    # test e collezione tempi
    # PAROLE CORRETTE
    edit_distance_times = []
    edit_distance_ngrams_times = []
    ed_correct = 0
    ed_ngrams_correct = 0
    for i in range(len(correct_words_to_test)):
        # print("To correct: " + correct_words_to_test[i] + "\n")
        # ed_correct = test_ed(ed_correct, edit_d, correct_words_to_test, i, edit_distance_times)
        test_ed(ed_correct, edit_d, correct_words_to_test[i], edit_distance_times)
        # print()
        # ed_ngrams_correct = test_ed_ngram(ed_ngrams_correct, edit_d, correct_words_to_test, i, edit_distance_ngrams_times)
        test_ed_ngram(ed_ngrams_correct, edit_d, correct_words_to_test[i], edit_distance_ngrams_times)

    edit_distance_mean_time = mean(edit_distance_times)
    edit_distance_ngrams_mean_time = mean(edit_distance_ngrams_times)
    print("Tempo medio per parole corrette: " + "{:.2e}".format(edit_distance_mean_time))
    print("Tempo medio per parole corrette con N-Grams: " + "{:.2e}".format(edit_distance_ngrams_mean_time))

    """
    if ed_correct == len(correct_words_to_test):
        print("OK")

    if ed_ngrams_correct == len(correct_words_to_test):
        print("OK")
    """
    print()


def uncorrect_words_test():
    print("TEST PAROLE NON CORRETTE")
    file_words = []
    with open("1160 parole italiane.txt", 'r', encoding='utf-8') as txt:
        for line in txt:
            if '\n' in line:
                line = line[:len(line) - 1]
            file_words.append(line)
    uncorrect_words_last_character = []
    uncorrect_words_first_character = []
    uncorrect_words_middle_character = []
    uncorrect_words_no_character = []
    length = int(len(file_words) / 2)
    rand_numbers_used = []
    rand = randint(0, length)
    for i in range(length):
        while rand in rand_numbers_used:
            rand = randint(0, len(file_words) - 1)
        rand_numbers_used.append(rand)
        rand_char = random.choice(string.ascii_letters)
        uncorrect_words_last_character.append(file_words[rand] + rand_char)
        uncorrect_words_first_character.append(rand_char + file_words[rand])
        uncorrect_words_middle_character.append(file_words[rand][:int(len(file_words[rand]) / 2) + 1] + rand_char +
                                                file_words[rand][int(len(file_words[rand]) / 2) + 1:])
        """
        if len(file_words[rand]) == 0:
            uncorrect_words_no_character.append("")
        else:
            uncorrect_words_no_character.append(file_words[rand][:(rand % len(file_words[rand])) - 1] +
                                                file_words[rand][rand % len(file_words[rand]):])
        """
        # probabilmente va usato rand_char = rand % len(correct_words[rand])
        uncorrect_words_no_character.append(file_words[rand][:rand] + file_words[rand][rand + 1:])

    delete = 1
    insert = 1
    copy = 0
    replace = 1
    swap = 2
    edit_d = Edit(delete, insert, copy, replace, swap)
    # test e collezione tempi
    # PAROLE IN LESSICO SCORRETTE
    # tempi correzione con carattere aggiuntivo alla fine, inizio e metà e mancanza di carattere
    edit_distance_times_last_character = []
    edit_distance_times_first_character = []
    edit_distance_times_middle_character = []
    edit_distance_times_no_character = []

    # tempi correzione con ngrams con carattere aggiuntivo alla fine, inizio e metà e mancanza di carattere
    edit_distance_ngrams_times_last_character = []
    edit_distance_ngrams_times_first_character = []
    edit_distance_ngrams_times_middle_character = []
    edit_distance_ngrams_times_no_character = []

    # correzioni disponibili
    ed_corrections_found_last_character = []
    ed_corrections_found_first_character = []
    ed_corrections_found_middle_character = []
    ed_corrections_found_no_character = []

    # correzioni disponibili con ngrams
    ed_ngrams_corrections_found_last_character = []
    ed_ngrams_corrections_found_first_character = []
    ed_ngrams_corrections_found_middle_character = []
    ed_ngrams_corrections_found_no_character = []

    # magari modificare con for line in to_use e passare quindi line direttamente
    for i in range(len(uncorrect_words_last_character)):
        # print("To correct: " + correct_words_to_test[i] + "\n")
        test_ed(ed_corrections_found_last_character, edit_d, uncorrect_words_last_character[i],
                edit_distance_times_last_character)
        # print()
        test_ed_ngram(ed_ngrams_corrections_found_last_character, edit_d, uncorrect_words_last_character[i],
                      edit_distance_ngrams_times_last_character)

        test_ed(ed_corrections_found_first_character, edit_d, uncorrect_words_first_character[i],
                edit_distance_times_first_character)
        test_ed_ngram(ed_ngrams_corrections_found_first_character, edit_d, uncorrect_words_first_character[i],
                      edit_distance_ngrams_times_first_character)

        test_ed(ed_corrections_found_middle_character, edit_d, uncorrect_words_middle_character[i],
                edit_distance_times_middle_character)
        test_ed_ngram(ed_ngrams_corrections_found_middle_character, edit_d, uncorrect_words_middle_character[i],
                      edit_distance_ngrams_times_middle_character)

        test_ed(ed_corrections_found_no_character, edit_d, uncorrect_words_no_character[i],
                edit_distance_times_no_character)
        test_ed_ngram(ed_ngrams_corrections_found_no_character, edit_d, uncorrect_words_no_character[i],
                      edit_distance_ngrams_times_no_character)

    # tempi medi di correzioni con i vari errori con e senza ngrams
    edit_distance_mean_time_last_character = mean(edit_distance_times_last_character)
    edit_distance_ngrams_mean_time_last_character = mean(edit_distance_ngrams_times_last_character)
    print("Tempo medio correzione con errato ultimo carattere: " + "{:.2e}".format(
        edit_distance_mean_time_last_character))
    print("Tempo medio correzione con errato ultimo carattere con N-Grams: " + "{:.2e}".format(
        edit_distance_ngrams_mean_time_last_character))
    print()

    edit_distance_mean_time_first_character = mean(edit_distance_times_first_character)
    edit_distance_ngrams_mean_time_first_character = mean(edit_distance_ngrams_times_first_character)
    print("Tempo medio correzione con errato primo carattere: " + "{:.2e}".format(
        edit_distance_mean_time_first_character))
    print("Tempo medio correzione con errato primo carattere con N-Grams: " + "{:.2e}".format(
        edit_distance_ngrams_mean_time_first_character))
    print()

    edit_distance_mean_time_middle_character = mean(edit_distance_times_middle_character)
    edit_distance_ngrams_mean_time_middle_character = mean(edit_distance_ngrams_times_middle_character)
    print("Tempo medio correzione con errato carattere centrale: " + "{:.2e}".format(
        edit_distance_mean_time_middle_character))
    print("Tempo medio correzione con errato carattere centrale con N-Grams: " + "{:.2e}".format(
        edit_distance_ngrams_mean_time_middle_character))
    print()

    edit_distance_mean_time_no_character = mean(edit_distance_times_no_character)
    edit_distance_ngrams_mean_time_no_character = mean(edit_distance_ngrams_times_no_character)
    print("Tempo medio correzione senza un carattere: " + "{:.2e}".format(edit_distance_mean_time_no_character))
    print("Tempo medio correzione senza un carattere con N-Grams: " + "{:.2e}".format(
        edit_distance_ngrams_mean_time_no_character))
    print()

    # correzioni medie trovate con e senza ngrams
    edit_distance_mean_corrections_found_last_character = mean(ed_corrections_found_last_character)
    edit_distance_ngrams_mean_corrections_found_last_character = mean(ed_ngrams_corrections_found_last_character)
    print("Correzioni trovate in media per errore ultimo carattere: " + "{:.2e}".format(
        edit_distance_mean_corrections_found_last_character))
    print("Correzioni trovate in media per errore ultimo carattere con N-Grams: " + "{:.2e}".format(
        edit_distance_ngrams_mean_corrections_found_last_character))
    print()

    edit_distance_mean_corrections_found_first_character = mean(ed_corrections_found_first_character)
    edit_distance_ngrams_mean_corrections_found_first_character = mean(ed_ngrams_corrections_found_first_character)
    print("Correzioni trovate in media per errore primo carattere: " + "{:.2e}".format(
        edit_distance_mean_corrections_found_first_character))
    print("Correzioni trovate in media per errore primo carattere con N-Grams: " + "{:.2e}".format(
        edit_distance_ngrams_mean_corrections_found_first_character))
    print()

    edit_distance_mean_corrections_found_middle_character = mean(ed_corrections_found_middle_character)
    edit_distance_ngrams_mean_corrections_found_middle_character = mean(ed_ngrams_corrections_found_middle_character)
    print("Correzioni trovate in media per errore carattere centrale: " + "{:.2e}".format(
        edit_distance_mean_corrections_found_middle_character))
    print("Correzioni trovate in media per errore carattere centrale con N-Grams: " + "{:.2e}".format(
        edit_distance_ngrams_mean_corrections_found_middle_character))
    print()

    edit_distance_mean_corrections_found_no_character = mean(ed_corrections_found_no_character)
    edit_distance_ngrams_mean_corrections_found_no_character = mean(ed_ngrams_corrections_found_no_character)
    print("Correzioni trovate in media per senza carattere: " + "{:.2e}".format(
        edit_distance_mean_corrections_found_no_character))
    print("Correzioni trovate in media per senza carattere con N-Grams: " + "{:.2e}".format(
        edit_distance_ngrams_mean_corrections_found_no_character))
    print()


def not_in_words_test():
    print("TEST PAROLE NON IN LESSICO")
    file_words = []
    with open("9000 nomi propri.txt", 'r', encoding='utf-8') as txt:
        for line in txt:
            if '\n' in line:
                line = line[:len(line) - 1]
            file_words.append(line)
    to_use = []

    length = int(len(file_words) / 2)
    rand_numbers_used = []
    rand = randint(0, len(file_words) - 1)
    for i in range(length):
        while rand in rand_numbers_used:
            rand = randint(0, len(file_words) - 1)
        rand_numbers_used.append(rand)
        to_use.append(file_words[rand])

    delete = 1
    insert = 1
    copy = 0
    replace = 1
    swap = 2
    edit_d = Edit(delete, insert, copy, replace, swap)
    # test e collezione tempi
    # PAROLE NON IN LESSICO
    edit_distance_times = []
    edit_distance_ngrams_times = []
    ed_corrections_found = []
    ed_ngrams_corrections_found = []
    # magari modificare con for line in to_use e passare quindi line direttamente
    for i in range(len(to_use)):
        # print("To correct: " + correct_words_to_test[i] + "\n")
        test_ed(ed_corrections_found, edit_d, to_use[i], edit_distance_times)
        # print()
        test_ed_ngram(ed_ngrams_corrections_found, edit_d, to_use[i], edit_distance_ngrams_times)

    edit_distance_mean_time = mean(edit_distance_times)
    edit_distance_ngrams_mean_time = mean(edit_distance_ngrams_times)
    print("Tempo medio correzione: " + "{:.2e}".format(edit_distance_mean_time))
    print("Tempo medio correzione con N-Grams: " + "{:.2e}".format(edit_distance_ngrams_mean_time))
    print()
    edit_distance_mean_corrections_found = mean(ed_corrections_found)
    edit_distance_ngrams_mean_corrections_found = mean(ed_ngrams_corrections_found)
    print("Correzioni trovate in media: " + "{:.2e}".format(edit_distance_mean_corrections_found))
    print("Correzioni trovate in media con N-Grams: " + "{:.2e}".format(edit_distance_ngrams_mean_corrections_found))
    print()


def multiple_ngrams_test():
    correct_words = []
    with open("1160 parole italiane.txt", 'r', encoding='utf-8') as txt:
        for line in txt:
            if "\n" in line:
                line = line[: len(line) - 1]
            correct_words.append(line)
    to_use = []
    # testiamo i 4 tipi di errori sulle parole corrette selezionate
    uncorrect_words_last_character = []
    uncorrect_words_first_character = []
    uncorrect_words_middle_character = []
    uncorrect_words_no_character = []

    # prendiamo solo 4 parole
    rand_numbers_used = []
    rand = randint(0, len(correct_words) - 1)
    for i in range(4):
        while rand in rand_numbers_used:
            rand = randint(0, len(correct_words) - 1)
        rand_numbers_used.append(rand)
        to_use.append(correct_words[rand])
        rand_char = random.choice(string.ascii_letters)
        uncorrect_words_last_character.append(correct_words[rand] + rand_char)
        uncorrect_words_first_character.append(rand_char + correct_words[rand])
        uncorrect_words_middle_character.append(
            correct_words[rand][:int(len(correct_words[rand]) / 2) + 1] + rand_char +
            correct_words[rand][int(len(correct_words[rand]) / 2) + 1:])
        rand_char = rand % len(correct_words[rand])
        uncorrect_words_no_character.append(correct_words[rand][:rand_char] + correct_words[rand][rand_char + 1:])

    # in ogni posizione abbiamo il risultato della parola nella prima posizione di to_use, sarà una lista lunga quanto
    # l'n utilizzato e in ogni posizione c'è una lista con tempo e correzioni trovate se ci sono, se c'è vero la parola
    # è corretta, altrimenti non sono state trovate correzioni
    test_results = []

    for word in uncorrect_words_last_character:
        for n in range(ceil(len(word) / 3) + 1):
            test_results.append(test_ed_multiple_ngrams(n, word, to_use))
        draw_plot(test_results, "Correzione ultimo carattere", word)
        test_results.clear()

    for word in uncorrect_words_first_character:
        for n in range(ceil(len(word) / 3) + 1):
            test_results.append(test_ed_multiple_ngrams(n, word, to_use))
        draw_plot(test_results, "Correzione primo carattere", word)
        test_results.clear()

    for word in uncorrect_words_middle_character:
        for n in range(ceil(len(word) / 3) + 1):
            test_results.append(test_ed_multiple_ngrams(n, word, to_use))
        draw_plot(test_results, "Correzione carattere centrale", word)
        test_results.clear()

    for word in uncorrect_words_no_character:
        for n in range(ceil(len(word) / 3) + 1):
            test_results.append(test_ed_multiple_ngrams(n, word, to_use))
        draw_plot(test_results, "Correzione carattere mancante", word)
        test_results.clear()


if __name__ == '__main__':
    # sys.stdout = open('Results.txt', 'w')
    # print("Versione Python: " + sys.version)
    """
    x = "algori"
    y = "argom"
    delete = 1
    insert = 1
    copy = 0
    replace = 1
    swap = 2
    edit_d = Edit(delete, insert, copy, replace, swap)
    c, op = edit_d.edit_distance(x, y)
    print(c[len(x) - 1][len(y) - 1])
    print(c)
    edit_d.op_sequence(op, len(x), len(y))
    lista = []
    lista.append(1)
    insert_in_list(lista, 10, 3)
    insert_in_list(lista, 4, 2)
    print(lista)
    print(len(lista))
    insert_in_list(lista, 4, 5)
    print(lista)
    print(len(lista))
    """
    # main()
    # create_ngrams_from_file()

    """
    delete = 1
    insert = 1
    copy = 0
    replace = 1
    swap = 2
    word = "subuto"
    edit_d = Edit(delete, insert, copy, replace, swap)
    result, index = edit_d.correction_word(word)
    print_result(result, index)
    result, index = edit_d.correction_word_ngram(word)
    print_result(result, index)
    """

    # correct_words_test()
    # uncorrect_words_test()
    # not_in_words_test()
    # sys.stdout.close()
    multiple_ngrams_test()
