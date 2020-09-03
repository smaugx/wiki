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


