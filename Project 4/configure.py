# Omer Khan
# CS461 Project 4
# Brian Hare

import csv
from collections import Counter

def configure(oldFile, trainingData, testData, validationData):
    list_of_words = []
    with open(oldFile, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        list_of_reader = []
        for line in reader:
            list_of_reader.append(line)
            for word in line[2].split():
                list_of_words.append(word)
    total_length = len(list_of_reader)

    #creating list of top 100 words
    top_hundred = Counter(list_of_words)
    top_hundred = top_hundred.most_common(100)
    list_of_words.clear()
    for word in top_hundred:
        list_of_words.append(word[0])

    dict_of_words = {}
    for x in range(0, 100):
        dict_of_words[list_of_words[x]] = x

    brand = ''
    with open(oldFile, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            brand += line[1] + '\n'

    with open(oldFile, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        header.pop(0)

        header[1] = "V1"
        for i in range(99):
            header.insert(i + 2, "V" + str(i + 2))

        training_write = csv.writer(open(trainingData, 'w', encoding='utf-8'))
        test_write = csv.writer(open(testData, 'w', encoding='utf-8'))
        validation_write = csv.writer(open(validationData, 'w', encoding='utf-8'))

        training_write.writerow(header[:-1])
        test_write.writerow(header[:-1])
        validation_write.writerow(header[:-1])

    counter = 0
    with open(oldFile, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            counter += 1
            _list = list(line)

            if _list[5] == 'Stars' or _list[5] == 'Unrated':
                continue
            if brand.count(_list[1]) == 1:
                _list[1] = 'Other'

            _style = _list[3]
            _country = _list[4]
            _stars = float(_list[5])

            array = list([0.0] * 100)
            for word in line[2].split():
                if word in dict_of_words:
                    array[dict_of_words[word]] += 1.0
            _list[2:101] = array

            _list.extend([_style, _country, _stars])

            if (counter <= total_length * 0.8):
                training_write.writerow(_list[1:105])
            elif (counter <= total_length * 0.9):
                test_write.writerow(_list[1:105])
            else:
                validation_write.writerow(_list[1:105])