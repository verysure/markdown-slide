"""
markdown-slides: Command Line
=============================

Usage: markslide markslide [-h] [-s STYLE] [-l LAYOUT] [-w] <Markdown File> <Output File>

"""


import markslide
import argparse, os.path, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


## helpers
class MarkSlideEvent(FileSystemEventHandler):
    def __init__(self, filename, call_func, *args, **kwargs):
        self.filename = filename
        self.call_func = call_func
        FileSystemEventHandler.__init__(self, *args, **kwargs)

    def on_modified(self, event):
        if event.src_path == self.filename:
            self.call_func()

def parse_argument():

    # parser
    parser = argparse.ArgumentParser( description='Convert markdown files to pdf slides')
    parser.add_argument(
        'markdown', 
        metavar='<Markdown File>', 
        help = 'Markdown file to be converted',
        type=str,
    )
    parser.add_argument(
        'output', 
        metavar = '<Output File>', 
        help = 'Output file location, supported file types include pdf and html.',
        type=str,
    )

    # optional arguments
    parser.add_argument(
        '-s', '--style',
        help = 'Custom style',
    )
    parser.add_argument(
        '-l', '--layout',
        help = 'Custom layout',
    )
    parser.add_argument(
        '-w', '--watch',
        help = 'Watch for file change.',
        action = 'store_true',
    )

    return parser.parse_args()





# command line function

def run():

    args = parse_argument()
    ms = markslide.MarkSlide()

    if args.watch:
        # render function
        render_markdown = lambda: ms.from_file(args.markdown, args.output, style = args.style, layout = args.layout)

        path, filename = os.path.split(args.markdown)
        if path == '':
            path = '.'

        observer = Observer()
        event = MarkSlideEvent(os.path.join(path, filename), render_markdown)

        observer.schedule(event, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        
    else:
        ms.from_file(args.markdown, args.output, style = args.style, layout = args.layout)


if __name__ == '__main__':
    run()
    

