# -*- coding: utf-8 -*-


class AfinnReader(object):
    def __init__(self, path):
        self.base_url = path + '/docs/AFINN-111.txt'
        self.word_collection = dict()

    def load(self):
        # Read file (per line)
        with open(self.base_url, 'rb') as input_file:
            for line in input_file:
                # Cleanup string
                line = self.cleanup(line).split('\t')
                self.word_collection[line[0]] = int(line[1])

        return self.word_collection

    @staticmethod
    def cleanup(text):
        return text.replace('\n', '')