"""
markdown-slides: Markdown to PDF Slides
=======================================

A package for using John Gruber's [Markdown](https://daringfireball.net/projects/markdown/) syntax to create pdf slides. 
It is intended for quick notes/reports.
"""


from markdown import markdown
from scss import Scss
import pdfkit
import xml.etree.ElementTree as et
import os.path


# helper functions
def _read_file(filename):
    with open(filename, 'r') as f:
        text = f.read()
    return text


class MarkSlide(object):
    "Object for converting markdown text/files to pdf."

    _options = {
        'page-height'   : '7.5in',
        'page-width'    : '10in',
        'margin-top'    : '0in',
        'margin-bottom' : '0in',
        'margin-right'  : '0in',
        'margin-left'   : '0in',
    }

    _header_class = {
        'h1': 'cover',
        'h2': 'text',
        'h3': 'section',
        'h4': 'blank',
        'h5': 'full',
        'h6': 'full',
    }

    _custom_style = ''
    _custom_layout = ''

    def __init__(self, **kwargs):
        style_path = os.path.join(os.path.dirname(__file__), '..', 'styles')
        self._default_style  = _read_file(os.path.join(style_path, 'light.scss'))
        self._default_layout = _read_file(os.path.join(style_path, 'default_layout.scss'))

        self.load_custom_settings(**kwargs)

    def load_custom_settings(self, **kwargs):

        # get custom styles
        style  = kwargs.get('style', None)
        layout = kwargs.get('layout', None)
        if style:
            self._custom_style = _read_file(style)
        if layout:
            self._custom_layout = _read_file(layout)

        # options for pdf
        options = kwargs.get('options', {})
        for k in options:
            self._options[k] = options[k]


    # core  function
    def html_from_string(self, markdown_text, **kwargs):
        "Core function, parsing Markdown Text to html."

        self.load_custom_settings(**kwargs)

        ## load markdown and parse into xml tree
        mark_root = et.fromstring('<html>\n' + markdown(markdown_text, output_format='xhtml5') + '\n</html>')

        ## restructure pdf html tags
        pdf_root = et.Element('html')
        pdf_root.extend([
            et.Element('head'),
            et.Element('body'),
        ])

        # insert slide style
        css = Scss().compile(self._default_style + self._custom_style + self._default_layout + self._custom_layout )
        pdf_root[0].append(et.Element('head'))
        pdf_root[0][0].append(et.Element('style'))
        pdf_root[0][0][0].text = css

        # insert head + slide body
        slides_root = pdf_root[1]

        # page break
        page_break = et.Element('p', {'class': 'pagebreak'})
        page_break.text = ' '

        # parse slides
        slide = None
        for children in mark_root:
            # append slide and create new slide if encounter new header
            if children.tag in self._header_class.keys():
                if slide is not None:
                    slides_root.append(slide)
                    slides_root.append(page_break)

                slide = et.Element('div', {'class': 'slide ' + self._header_class[children.tag]})
                slide.extend([
                    et.Element('div', {'class': 'title'}),
                    et.Element('div', {'class': 'content'}),
                ])

                slide[0].text = ' '
                slide[0].append(children)
                slide[-1].text = ' '

            # append the children slide
            else:
                slide[-1].append(children)

        slides_root.append(slide)

        # substitute img tag
        for img_element in pdf_root.findall('.//img'):
            img_src = os.path.abspath(img_element.get('src'))

            # create outer div
            img_element.clear()
            img_element.tag = 'div'
            img_element.set('class', 'imgouter')

            img_element.append(et.Element('div', {
                'class': 'imginner',
                'style': 'background-image: url({:s});'.format(img_src)
            }))
            img_element[0].text = ' '

        return et.tostring(pdf_root)

    def html_from_file(self, markdown_file, **kwargs):
        "Loads markdown txt from file"
        with open(markdown_file, 'r') as f:
            markdown_text = f.read()
        return self.html_from_string(markdown_text, **kwargs)
        

    # --- Create PDF ---

    def from_string(self, markdown_text, output_filename, **kwargs):
        "Generates pdf from markdown text"
        html_text = self.html_from_string(markdown_text, **kwargs)
        self._html_to_pdf(html_text, output_filename)

    def from_file(self, markdown_file, output_filename, **kwargs):
        "Generates pdf from markdown text"
        html_text = self.html_from_file(markdown_file, **kwargs)
        self._html_to_pdf(html_text, output_filename)

    def _html_to_pdf(self, html_text, output_filename):
        ## generate pdf
        pdfkit.from_string(
            html_text, 
            output_filename, 
            options = self._options
        )



if __name__ == '__main__':
    ms = MarkSlide()
    path = os.path.dirname(__file__)
    ms.from_file(
        os.path.join(path, '..', 'test', 'test.md'), 
        os.path.join(path, '..', 'test', 'test.pdf'), 
        )





