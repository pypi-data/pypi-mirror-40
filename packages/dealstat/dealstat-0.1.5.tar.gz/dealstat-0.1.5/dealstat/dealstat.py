# -*- coding: utf-8 -*-

"""Main module."""

import random, string, tarfile

def unique_id(length=25):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def compare_figures(figure1, figure2, thresh = 0.99):
    if figure1 == figure2:
        return True
    elif figure1 >= figure2 and figure1 * thresh <= figure2:
        return True
    elif figure2 >= figure1 and figure2 * thresh <= figure1:
        return True
    else:
        return False


def compress_dir(folder_location):
	compress_name = folder_location.split('/')[-1] + '.tar.gz'
	tar = tarfile.open(compress_name, 'w:gz')
	tar.add(folder_location, arcname='TarName')
	tar.close()
	return compress_name


if __name__ == '__main__':
	compress_dir('/Users/ecatkins/Downloads/Sample_Deeds')
