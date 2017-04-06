
markdown-slides: Markdown to PDF Slides
=======================================

A package for using John Gruber's [Markdown](https://daringfireball.net/projects/markdown/) syntax to create pdf slides. 
It is intended for quick notes/reports.


Installation
------------

1. Download:

        git clone

2. Install:

        python setup.py install

3. Install wkhtmltopdf (Debian/Ubuntu)

        sudo apt-get install wkhtmltopdf

    The package depends on [pdfkit][1] which requires [wkhtmltopdf][2]. 
    For other os and distributions, please download from the [website][3]. 
    (Note: other os are not tested, please issue merge requests if you found issues or have a solution for other os.)

[1]: https://github.com/JazzCore/python-pdfkit
[2]: https://wkhtmltopdf.org/
[3]: https://wkhtmltopdf.org/downloads.html




Usage
-----

### Command Line ###

The package provides command line scripts. `markslide -h` for more info.


### API ###

The python package maybe used as API. Simple example:

    from markslide import MarkSlide
    MarkSlide().from_file('input.md', 'output.pdf', style='custom.scss', layout = 'layout.scss')


### Configuration ###

You may define your own stylesheet. An example stylesheet is in `styles/dark.scss`. 
Stylesheets are loaded in order: `light.scss`, `custom_style.scss`, `default_layout.scss`, `custom_layout.scss`.


License
-------

MIT License


