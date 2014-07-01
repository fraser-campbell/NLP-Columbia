__author__ = 'frasercampbell'

import pprint

def grammar_rules(file):
    dictionary = {}
    l = open(file, "r")
    for lines in l:
        segments = lines.split(" ")
        if "BINARYRULE" in lines:
            if(segments[2] not in dictionary):
                dictionary[segments[2]] = []
            dictionary[segments[2]].append([segments[3], segments[4].strip('\n')])
    return dictionary

grammar_dictionary = grammar_rules("parse_train.counts.out")


def count_binary(X, Y_1, Y_2, file):
    l = open(file, "r")
    for lines in l:
        if "BINARYRULE" in lines:
            parse_line = lines.split(" ")
            count_int = parse_line[0]
            X_compare = parse_line[2]
            Y_1_compare = parse_line[3]
            Y_2_compare = parse_line[4].strip("\n")
            if(X_compare == X):
                if(Y_1_compare == Y_1 and Y_2_compare == Y_2):
                    count_numerator = float(count_int)
        if "NONTERMINAL" in lines:
            parse_line = lines.split(" ")
            count_int_again = parse_line[0]
            X_compare_again = parse_line[2].strip("\n")
            if(X_compare_again == X):
                count_denominator = float(count_int_again)

    return count_numerator/count_denominator


def count_unary(X, Y, file):
    l = open(file, "r")
    count_numerator = 0
    count_denominator = 0
    for lines in l:
        if "UNARYRULE" in lines:
            parse_line = lines.split(" ")
            count_int = parse_line[0]
            X_compare = parse_line[2]
            Y_compare = parse_line[3].strip("\n")
            if(X_compare == X):
                if(Y_compare == Y):
                    count_numerator = float(count_int)
        if "NONTERMINAL" in lines:
            parse_line = lines.split(" ")
            count_int_again = parse_line[0]
            X_compare_again = parse_line[2].strip("\n")
            if(X_compare_again == X):
                count_denominator = float(count_int_again)
    if (count_numerator == 0 or count_denominator == 0):
        return 0.0
    else:
        return count_numerator/count_denominator


# def CKY(i, j, X, file, vecs):
#     print ("i&j:" + str(i) + str(j))
#     if(i == j): #Base case
#         print "closed stack"
#         # print count_unary(X, vecs[i], file)
#         return count_unary(X, vecs[i], file)
#     elif X in grammar_dictionary:
#         for combo in grammar_dictionary[X]:
#             for s in range(i, j):
#                 print ("s: " + str(s)), i, j, range(i, j)
#                 CKY(i, s, combo[0], file, vecs) * CKY(s+1, j, combo[1], file, vecs) * count_binary(X, combo[0], combo[1], file)
#     else:
#         print ("i&j:" + str(i) + str(j))
#         return 0.0


def CKY(i, j, X, file, vecs, Y, Z):
    if(i == j): #Base case
        print "closed stack"
        return count_unary(X, vecs[i], file)
    else:
        for s in range(i, j):
            CKY(i, s, Y, file, vecs) * CKY(s+1, j, Z, file, vecs) * count_binary(X, Y, Z, file)

def wrapper_func(file):
    l = open(file, "r")
    grid = []
    for lines in l:
        sentence = []
        for elem in lines.split(" "):
            sentence.append([elem.strip('\n')])
        grid.append(sentence)

    # test_sentence = grid[0]
    test_sentence = [['What'], ['was'], ['the']]
    for X in grammar_dictionary.iterkeys():
        for combo in grammar_dictionary[X]:
    # for word in test_sentence:
    #     if (count_unary("WHNP+PRON", word[0], "parse_train.counts.out") is not 0):
    #         print count_unary("WHNP+PRON", word[0], "parse_train.counts.out")
    # print test_sentence
            CKY(0, len(test_sentence) - 1, "SBARQ", "parse_train.counts.out", test_sentence, combo[0], combo[1])



wrapper_func("parse_dev.dat")


# print count_binary("SBARQ", "SBARQ", ".", "parse_train.counts.out")
# print count_unary("ADJ", "famous", "parse_train.counts.out")