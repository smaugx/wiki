# rsync 的操作

## 本机目录同步
```
rsync  -rptgoDvH --delete --exclude "cbuild" --exclude "cbuild_release" --exclude "libs" /root/top/mux/ /mnt/centos-share/top/mux/
```

上面的命令会把 `/root/top/mux` 同步到 `/mnt/centos-share/top/mux`，并且忽略掉 `cbuild` `cbuild_release` `libs` 目录。

这个命令我经常会用，在本地 mac host 和 virtual-host centos 之间同步文件。

```
alias syncmac='rsync  -rptgoDvH --delete --exclude "cbuild" --exclude "cbuild_release" --exclude "libs" /root/top/mux/ /mnt/centos-share/top/mux/'
```

直接使用 `syncmac` 命令就行了。


## 远程机器同步

```
rsync  -avHe  "ssh -p 1022 -i /root/.ssh/xxxx.pem" root@8.8.8.8::dashdb /root/smaug/temp/
```

上面会把远程机器的  dashdb 目录同步到 temp 目录下。

