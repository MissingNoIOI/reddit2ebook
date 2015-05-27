# reddit2ebook
--------
### Convert stories and comments from reddit into epubs using pandoc

Requirements: PyYaml. pypandoc and praw


```
 Usage: reddit2ebook initfile directory
```

 The initfile should be in the following format:

```
 bookname:
     - url
     - url
     - url
```

It can be installed via pip:

```
pip install reddit2ebook
```

Attendtion: Due to a bug in pypandoc this script currently doesn't work on Windows
