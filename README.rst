
Convert stories and comments from reddit into epubs

It doesn't require Pandoc any longer and is a pure Python program now
ebooklib currently has a bug, so I'm shipping out a patched version
until it gets fixed

Requirements: PyYaml. pyprind, praw, mistune::

 Usage: reddit2ebook configfile output-directory

The configfile should be in the following format: ::

     AssortedWorks:
         author: /u/GallowB00b
         title: Assorted Works
         cover: Gallow.jpg
         lang: en
         links:
             - url
             - url
             - url

     MissingKeys:
         author: /u/airz24
         title: The Missing Keys
         cover: keyboard.jpg
         lang: en
         links:
             - url
             - url
             - url

author, title cover and lang are all optional

The older format is also supported: ::

     bookname:
         - url
         - url
         - url



You can use regular links for the submissions and permalinks for comments
If the link has a trailing slash its a submission, if not a comment. This
is the default behaviour when copy-pasting the links from the browser,
but sometimes people link to the comment section instead of the submission,
simply adding a trailing slash will give you the submission text then
