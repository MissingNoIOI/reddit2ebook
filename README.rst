
Convert stories and comments from reddit into epubs

it doesn't require Pandoc any longer and is a pure Python program now

Requirements: PyYaml. pyprind, praw, mistune, ebooklib::

 Usage: reddit2ebook configfile output-directory

The configfile should be in the following format: ::

     bookname1:
         - url
         - url
         - url

     bookname2:
         - url
         - url
         - url

You can use regular links for the submissions and permalinks for comments
