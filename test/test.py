import sys
from os.path import join, dirname, abspath
sys.path.append(join(dirname(dirname(abspath(__file__))), 'src'))
from markslide import MarkSlide


if __name__ == '__main__':
    ms = MarkSlide()
    path = dirname(__file__)
    ms.from_file(
        join(path, 'test.md'), 
        join(path, 'test.pdf'), 
        )
