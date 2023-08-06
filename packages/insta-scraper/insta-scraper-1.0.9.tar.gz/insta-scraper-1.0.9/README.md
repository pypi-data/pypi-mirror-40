# Instagram Photos/Videos/Stories downloader

A python tool to download instagram user's photos/videos/stories.

## Usage

For a single user's media
```
insta-scraper -u YOUR_INSTAGRAM_USERNAME -t FRIEND'S_USERNAME
```

To download multiple users media
```
insta-scraper -u YOUR_INSTAGRAM_USERNAME -t FRIEND'S_USERNAME FRIEND'S_USERNAME1
```

or you can specify a file that contains target usernames seperated by newline.
```
insta-scraper -u YOUR_INSTAGRAM_USERNAME -f users.txt
```



Here are the helpful arguments.

```
-u/--user		Instagram username which is will be used for login

-t/--target-users	To specify one or more users followed by a space (optional)

-f/--filename		Filename containing instagram usernames followed by newline (optional)

-o/--output-dir		Output directory to store user's media.	(optional)

Note: Use a particular argument when specifying target usernames either -t or -f but not both.
      If you specify both arguments then it will only takes -t as target.
```
