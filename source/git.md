# git 操作备忘

## git 仓库迁移、镜像、复制

```
1. create empty new-repo in github.com
2. cd old_repo (maybe you need clone the old_repo first)
3. git push --mirror git@github.com:username/new_repo.git
```

这样就可以完整的镜像一个仓库，包括所有的 commits 信息。

## git 删除远程不存在的分支
远程分支删除之后，使用 `git branch -a` 命令依然可以看得到被删除的分支，那么如何在本地删除远程不存在的分支：

```
git remote prune origin
```


## git 重写/修改 remote commits

这个需求的来源于我想修改某个仓库当中历史提交的 commits 信息，比如日期，提交邮箱，甚至提交信息。

但是这些 commits 已经是被提交到远程仓库了，那么如何修改呢？

要求是不要产生新的 commit，而直接修改原有的 commit 信息。

这就要用到 git 的**大杀器了，原子弹级别的大杀器**：

```
#!/bin/sh

git filter-branch --env-filter '

OLD_EMAIL="smaug@gmail.com"
CORRECT_NAME="smaugx"
CORRECT_EMAIL="linuxcode2niki@gmail.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' -f  --  --all
```

上面这段直接来自：[https://docs.github.com/en/github/using-git/changing-author-info](https://docs.github.com/en/github/using-git/changing-author-info)。


如果要修改某个 commit 的信息呢？

```
git filter-branch --env-filter \
    'if [ $GIT_COMMIT = 66674eec777a783320290f490a96335a6e73feac ]
     then
         export GIT_AUTHOR_DATE="Thu Aug 21 10:55:23 2020 +0800"
         export GIT_COMMITTER_DATE="Thu Aug 21 10:55:23 2020 +0800"
     fi'
```

这个命令真是太屌了！！


## git 回滚
### 代码回退
默认参数 --soft，所有 commit 的修改都会退回到 git 缓冲区

参数 --hard，所有 commit 的修改直接丢弃

```
git reest --hard HEAD^           # 回退到上个版本
git reset --hard commit_id        # 退到/进到 指定的 commit_id
```

### 推送到远程

```
git push origin HEAD --force
```

## git 合并多个 commit

使用的就是 git rebase 命令，本质就是变基操作。

参考： [「Git」合并多个 Commit](https://www.jianshu.com/p/964de879904a)

## git 颜色配置
```
git config --global color.status auto
git config --global color.diff auto
git config --global color.branch auto
git config --global color.interactive auto
```

## git 浅克隆（空克隆）
只需要在 clone 的时候加上 --bare 参数即可

```
git clone https://github.com/smaugx/mux --bare
```