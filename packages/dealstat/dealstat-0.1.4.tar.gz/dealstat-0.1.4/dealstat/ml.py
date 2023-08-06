import subprocess, os

import numpy as np

class Embeddings:

	def __init__(self):
		pass

	def download_embeddings(self, to_dir=None):
		if to_dir:
			subprocess.call(['wget', '-O', os.path.join(to_dir, 'glove.6B.zip'), 'http://nlp.stanford.edu/data/glove.6B.zip'])
		else:
			subprocess.call(['wget', 'http://nlp.stanford.edu/data/glove.6B.zip'])

	def extract_embeddings(self, to_dir=None):
		if to_dir:
			subprocess.call(['unzip', os.path.join(to_dir, 'glove.6B.zip'), '-d', to_dir])
		else:
			subprocess.call(['unzip','glove.6B.zip'])

	def generate(self, loc, dim):
	    embeddings_index = {}

	    path = os.path.join(loc, 'glove.6B.{}d.txt'.format(dim))

	    f = open(path)
	    for line in f:
	        values = line.split()
	        word = values[0]
	        coefs = np.asarray(values[1:], dtype='float32')
	        embeddings_index[word] = coefs
	    f.close()

	    return embeddings_index






if __name__ == '__main__':

	e = Embeddings()
	# e.download_embeddings('/Users/ecatkins/Documents')
	# e.extract_embeddings('/Users/ecatkins/Documents/')
	e.generate('/Users/ecatkins/Documents', 200)



