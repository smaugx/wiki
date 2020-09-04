# wiki
my personal wiki.

# how to build your personal wiki?
It's easy to build a wiki site from this repo. 

Follow me:

## create a repo for user-site
>if you already have one user-site, ignore this step.

attention: create repo in github.com, the repo name is:

```
yourname.github.io
```
for me, It's  `smaugx.github.io`.

for more information, check this: [https://docs.github.com/cn/github/working-with-github-pages/creating-a-github-pages-site](https://docs.github.com/cn/github/working-with-github-pages/creating-a-github-pages-site).

after everything done, you can access this url:

```
http://yourname.github.io
```

## create empty repo in github.com for wiki-site
>befor doing this step, make sure `http://yourname.github.io` is ok.

first you should create a empty repo in github.com, named whaterver you like.

for example:

```
https://github.com/yourname/your-wiki
```

## clone this repo

```
git clone https://github.com/smaugx/wiki.git
```

## change my remote url to your remote url

```
cd wiki
git remote rm origin
git remote add origin  https://github.com/yourname/your-wiki.git
```

## push to remote

```
git push -u origin master
```

Ok, now you will find `https://github.com/yourname/your-wiki.git` same as `https://github.com/smaugx/wiki`.

## Configuring a publishing source for your wiki site

1 on github, navigate to your-wiki repo

2 under your repository name, click **Settings**.

3 Under "**GiHub Pages**", use **master** branch and select `/docs` folder.

4 click save

Ok, you let's try:

```
http://your-name.github.io/your-wiki
```

for more information, check this: [https://docs.github.com/cn/github/working-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site](https://docs.github.com/cn/github/working-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

Good Luck!


# how to use(write and post)
> make sure your wiki site is ready: `http://your-name.github.io/your-wiki`

first, install mkdocs tools:

```
pip install mkdocs
```
	
second, begin to write markdown post, and put them in to **source** dir;

and third, just run command:

```
python run.py
```

this will build the site and push new change to remote repo.

maybe you should use your own config, please modify `mkdocs.yml`.

