
Convert stories and comments from reddit into epubs using pandoc

Requirements: PyYaml. pypandoc and praw::

 Usage: reddit2ebook initfile output-directory

The initfile should be in the following format: ::

     bookname1:
         - url
         - url
         - url

     bookname2:
         - url
         - url
         - url

You can use regular links for the submissions and permalinks for comments