from spacy_conll import Spacy2ConllParser

prsr = Spacy2ConllParser()

prsr.parseprint(input_file='input.txt', output_file='output.txt', output_encoding='utf-8', include_headers=True)