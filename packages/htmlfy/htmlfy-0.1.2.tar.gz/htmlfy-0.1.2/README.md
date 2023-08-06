# htmlfy
Python package for HTML minification.  

## Installation
```shell
python3 -mpip install htmlfy
```

## Usage

### Minifing HTML markup in variable

```python
>>> import htmlfy
>>> html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Hello</title>
      </head>
      <body>
        <p>hello, world!</p>
      </body>
    </html>"""
>>> htmlfy.minify_html(html)
'<!DOCTYPE html><html><head><title>Hello</title></head><body><p>hello, world!</p></body></html>'
```

### Minifing HTML file

```python
>>> import htmlfy
>>> src_path = 'my_file.html'
>>> dst_path = 'my_file.min.html'
>>> htmlfy.minify_html_file(src_path,dst_path)
```

### Arguments

```python
def htmlfy.minify_html(html,
                strict_spaces=True,
                no_space_between_tags=True,
                preserve=True,
                remove_comments=True,
                html5_min_attr=True,
                html5_emptytags=True
                )

def minify_html_file(source_path,minified_path,
                strict_spaces=True,
                no_space_between_tags=True,
                preserve=True,
                remove_comments=True,
                html5_min_attr=True,
                html5_emptytags=True
                )
```

* **strict_spaces** - strict all spaces(new lines, tabs and etc.) to single space. Except preserved blocks.
* **no_space_between_tags** - delete all spaces between tags.
* **preserve** - it will save all formating in `<pre>`,`<textarea>`,`<script>` tags. Also it will keep PHP expresions like `<?php ... ?>` and `<?=...?>`
* **remove_comments** - delete all types of comments from the code also from `<style>` and `<script>` like `<!-- ... -->`,`/* ... */` or `// comment`. You can save the comment using `<!--! ... -->` format. Expressions comments like `<!--[if gte IE 7]>...<![endif]-->` will be preserved also. 
* **html5_min_attr** - shrink `disabled="disabled"`,`checked="checked"`,`selected="selected"` to HTML5 notation `disabled`,`checked` and `selected` 
* **html5_emptytags** - removes tailing slash in empty tags like `<br />`,`<img ... />` or `<input ... />`

## License

Copyright (c) 2019, Alexey Schebelev

Distributed under [The BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause).
