import torch

class Dictionary(object):
    def __init__(self):
        self.word2idx = {}
        self.idx2word = []

    def add_word(self, word):
        if word not in self.word2idx:
            self.idx2word.append(word)
            self.word2idx[word] = len(self.idx2word) - 1
        return self.word2idx[word]

    def __len__(self):
        return len(self.idx2word)


class Corpus(object):
    def __init__(self, train, valid, test):
        self.dictionary = Dictionary()
        self.train = self.tokenize(train)
        self.valid = self.tokenize(valid)
        self.test = self.tokenize(test)

    def tokenize(self, corpus):
        """Tokenizes a random sample of trouble."""
        # Add words to the dictionary
        tokens = 0

        with open(path, 'r') as f:
            trouble_corpus = f.read()

        for line in trouble_corpus.split():
            words = line.split()
            tokens += len(words)
            for word in words:
                self.dictionary.add_word(word)

        # Tokenize file content
        ids = torch.LongTensor(tokens)
        token = 0
        for line in corpus.split():
            words = line.split()
            for word in words:
                ids[token] = self.dictionary.word2idx[word]
                token += 1

        return ids
