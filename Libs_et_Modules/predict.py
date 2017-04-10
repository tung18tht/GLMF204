import sys
import re
import collections


def clearLine(line):
    line = re.sub(r"[^\w\s]", ' ', line)
    line = re.sub(r'\s+', ' ', line)
    return line.lower()

def unigrams(infile, outfile='unigrams.txt'):
    print('Calcul des unigrammes...', end='', flush=True)
    unigrams = {}
    try:
        with open(infile, 'r') as fic:
            for line in fic:
                for word in clearLine(line).split(' '):
                    if word != '':
                        if word in unigrams:
                            unigrams[word] += 1
                        else:
                            unigrams[word] = 1
    except Exception as e:
        print('\nUne erreur est survenue lors de la lecture de', infile)
        print(e.strerror)
        exit(1)

    try:
        with open(outfile, 'w') as fic:
            unigrams = collections.OrderedDict(sorted(unigrams.items(), key=lambda t : t[1], reverse=True))
            for word in unigrams:
                fic.write(word + ' ' + str(unigrams[word]) + '\n')
    except Exception as e:
        print('\nUne erreur est survenue lors de l\'écriture dans', outfile)
        print(e.strerror)
        exit(1)

    print(' Ok')

def ngrams(infile, n, outfile=''):
    if n < 2:
        print('Fonction ngrams() : Valeur minimale de n : 2')
        exit(3)
    if outfile == '':
        outfile = str(n) + '_grams.txt'
    print('Calcul des {}-grammes...'.format(n), end='', flush=True)
    ngrams = {}
    try:
        with open(infile, 'r') as fic:
            for line in fic:
                words = clearLine(line).split(' ')
                words = [ elt for elt in words if elt != '' ]
                words = [ ' '.join(name) for name in zip(*[words[i:] for i in range(n)])]
                for word in words:
                    if word in ngrams:
                        ngrams[word] += 1
                    else:
                        ngrams[word] = 1
    except Exception as e:
        print('\nUne erreur est survenue lors de la lecture de', infile)
        print(e.strerror)
        exit(1)

    try:
        with open(outfile, 'w') as fic:
            ngrams = list(ngrams.items())
            ngrams.sort(key=lambda elt : elt[1], reverse=True)
            for word, val in ngrams:
                    fic.write(word + ' ' + str(val) + '\n')
    except Exception as e:
        print('\nUne erreur est survenue lors de l\'écriture dans', outfile)
        print(e.strerror)
        exit(1)

    print(' Ok')

def generate_stats(infile):
    print('Lecture du fichier des n-grammes...', end='', flush=True)
    ngrams = {}
    try:
        with open(infile, 'r') as fic:
            for line in fic:
                words = line.split(' ')
                value = int(words.pop())
                next_word = words.pop()
                key = ' '.join(words)
                if key in ngrams:
                    ngrams[key][next_word] = value 
                else:
                    ngrams[key] = { next_word : value }
    except Exception as e:
        print('\nUne erreur est survenue lors de la lecture de', infile)
        print(e.strerror)
        exit(1)

    for word in ngrams:
        n = 0
        for next_words in ngrams[word]:
            n += ngrams[word][next_words]
        ngrams[word] = [ (next_words, round(ngrams[word][next_words] / n, 3)) for next_words in ngrams[word]]
        ngrams[word].sort(key=lambda elt : elt[1], reverse=True)

    print(' Ok')
    return ngrams

def predict(stats, term, threshold):
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
        print('Syntax : predict <corpus_file.txt>')
        exit(2)
    ngrams(sys.argv[1], 2)
    ngrams = generate_stats('2_grams.txt')
    print(predict(ngrams, 'van', 0.1))
