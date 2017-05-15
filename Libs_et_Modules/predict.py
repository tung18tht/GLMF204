import sys
import re
import collections


def clearLine(line):
    line = re.sub(r"[^\w\s]", ' ', line)
    line = re.sub(r'\s+', ' ', line)
    return line.lower()

def unigrams(infile, outfile='unigrams.txt'):
    print('Calculate the unigrams...', end='', flush=True)
    unigrams = {}
    try:
        with open(infile, 'r') as file:
            for line in file:
                for word in clearLine(line).split(' '):
                    if word != '':
                        if word in unigrams:
                            unigrams[word] += 1
                        else:
                            unigrams[word] = 1
    except Exception as e:
        print('\nAn error occurred while reading ', infile)
        print(e.strerror)
        exit(1)

    try:
        with open(outfile, 'w') as file:
            unigrams = collections.OrderedDict(sorted(unigrams.items(), key=lambda t : t[1], reverse=True))
            for word in unigrams:
                file.write(word + ' ' + str(unigrams[word]) + '\n')
    except Exception as e:
        print('\nAn error occurred while writing ', outfile)
        print(e.strerror)
        exit(1)

    print(' Ok')

def ngrams(infile, n, outfile=''):
    if n < 2:
        print('Function ngrams(): Minimum value of n: 2')
        exit(3)
    if outfile == '':
        outfile = str(n) + '_grams.txt'
    print('Calculate the {}-grams...'.format(n), end='', flush=True)
    ngrams = {}
    try:
        with open(infile, 'r') as file:
            for line in file:
                words = clearLine(line).split(' ')
                words = [ element for element in words if element != '' ]
                words = [ ' '.join(name) for name in zip(*[words[i:] for i in range(n)])]
                for word in words:
                    if word in ngrams:
                        ngrams[word] += 1
                    else:
                        ngrams[word] = 1
    except Exception as e:
        print('\nAn error occurred while reading ', infile)
        print(e.strerror)
        exit(1)

    try:
        with open(outfile, 'w') as file:
            ngrams = list(ngrams.items())
            ngrams.sort(key=lambda element: element[1], reverse=True)
            for word, val in ngrams:
                    file.write(word + ' ' + str(val) + '\n')
    except Exception as e:
        print('\nAn error occurred while writing ', outfile)
        print(e.strerror)
        exit(1)

    print(' Ok')

def generate_stats(infile):
    print('Reading n-grams file...', end='', flush=True)
    ngrams = {}
    try:
        with open(infile, 'r') as file:
            for line in file:
                words = line.split(' ')
                value = int(words.pop())
                next_word = words.pop()
                key = ' '.join(words)
                if key in ngrams:
                    ngrams[key][next_word] = value 
                else:
                    ngrams[key] = { next_word : value }
    except Exception as e:
        print('\nAn error occurred while reading ', infile)
        print(e.strerror)
        exit(1)

    for word in ngrams:
        n = 0
        for next_words in ngrams[word]:
            n += ngrams[word][next_words]
        ngrams[word] = [ (next_words, round(ngrams[word][next_words] / n, 3)) for next_words in ngrams[word]]
        ngrams[word].sort(key=lambda element : element[1], reverse=True)

    print(' Ok')
    return ngrams

def predict(stats, term, threshold = 0):
    result = []
    if term in stats:
        for words, value in stats[term]:
            if value > threshold:
                result.append((words, value))
    if result == []:
        return [('', 1)]
    else:
        return result

def high_predict(stats, threshold):
    result = []
    for term in stats:
        for words, value in stats[term]:
            if value > threshold:
                result.append((term, words, value))
    return result


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Syntax: predict <corpus_file.txt>')
        exit(2)

    # unigrams(sys.argv[1])
    # ngrams = generate_stats('unigrams.txt')
    # print(predict(ngrams, 'th'))

    ngrams(sys.argv[1], 2)
    ngrams = generate_stats('2_grams.txt')
    print(predict(ngrams, 'on'))

    # ngrams(sys.argv[1], 3)
    # ngrams = generate_stats('3_grams.txt')
    # print(predict(ngrams, 'one of'))