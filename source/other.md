# goaccess 编译安装
```
autoreconf -fiv
./configure  --enable-utf8 --enable-geoip=legacy --prefix=/usr/local/goaccess  --with-openssl

make  && make install 
```

# mac ubuntu 共享文件
经常出现启动 Ubuntu 虚拟机进入共享目录是空的情况，但是共享目录明明已经挂载好了。

可以执行下面的命令，重新再挂载下：

```
cd /opt/VBoxGuestAdditions-*/init  
sudo ./vboxadd setup

sudo mount -t vboxsf centos-share /mnt/centos-share
```

# shadowsocks-ng-r8 自定义 pac 规则
```
$ cat ~/.ShadowsocksX-NG/user-rule.txt
! Put user rules line by line in this file.
! See https://adblockplus.org/en/filter-cheatsheet
||*.github.com
||*github.com
||github.com
||*.ipinfo.io
||*ipinfo.io
||ipinfo.io
||*.ip2location.com
||*ip2location.com
||ip2location.com
||*.rebootcat.com
||*rebootcat.com
||rebootcat.com
||*.stackoverflow.com
||*stackoverflow.com
||stackoverflow.com
||*.readthedocs.io
||*readthedocs.io
||readthedocs.io
```

上面针对的是  mac 平台，如果发现修改之后并没有生效的话，可以尝试:

**重启 ss 以及浏览器**

**重启 ss 以及浏览器**

**重启 ss 以及浏览器**


# mysql 命令行输入密码不能成功登陆
使用如下命令：

```
mysql -u root --password="12345"
```

碰到无法登陆的情况：

```
mysql: [Warning] Using a password on the command line interface can be insecure. ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
```

原来**罪魁祸首是密码当中的 `$` 字符，在命令行需要进行转移**：

```
mysql -u root -P3360 --password="xd89fjd\$fjd88"
```

加上转义之后，成功登陆。


# firewalld 启动失败
firewalld 是 centos 上的一个防火墙模块，但是有天碰到了这样的错误：

```
$ systemctl  start firewalld
Job for firewalld.service failed because the control process exited with error code. See "systemctl status firewalld.service" and "journalctl -xe" for details.


$ systemctl status firewalld.service -l

[0m firewalld.service - firewalld - dynamic firewall daemon
   Loaded: loaded (/usr/lib/systemd/system/firewalld.service; enabled; vendor preset: enabled)
   Active: failed (Result: timeout) since Wed 2017-07-26 10:12:43 CST; 54min ago
     Docs: man:firewalld(1)
  Process: 152761 ExecStart=/usr/sbin/firewalld --nofork --nopid $FIREWALLD_ARGS (code=exited, status=0/SUCCESS)
 Main PID: 152761 (code=exited, status=0/SUCCESS)


Jul 26 10:11:12 localhost.localdomain systemd[1]: Starting firewalld - dynamic firewall daemon...
Jul 26 10:12:42 localhost.localdomain systemd[1]: firewalld.service start operation timed out. Terminating.
Jul 26 10:12:43 localhost.localdomain systemd[1]: Failed to start firewalld - dynamic firewall daemon.
Jul 26 10:12:43 localhost.localdomain systemd[1]: Unit firewalld.service entered failed state.
Jul 26 10:12:43 localhost.localdomain systemd[1]: firewalld.service failed.
```

探索一番，解决办法如下：

1. 修改了 /lib64/libstdc++.so.6 指向其他版本 （比如你有多个版本）
2. 修改 /usr/sbin/firewalld 使用系统默认的 python2 版本


# valgrind segment fault  signal 11

```
==5004== Process terminating with default action of signal 11 (SIGSEGV): dumping core
==5004==  Access not within mapped region at address 0xFFFFFFFF00000000
==5004==    at 0x5758B20: std::basic_string<char, std::char_traits<char>, std::allocator<char> >::~basic_string() (in /usr/lib64/libstdc++.so.6.0.19)
==5004==    by 0x12CC548F: ???
==5004==    by 0x68F875: top::transport::protobuf::GossipParams::SharedDtor() (transport.pb.cc:1498)
==5004==    by 0x68F7B7: top::transport::protobuf::GossipParams::~GossipParams() (transport.pb.cc:1492)
==5004==    by 0x68F813: top::transport::protobuf::GossipParams::~GossipParams() (transport.pb.cc:1493)
==5004==    by 0x693C09: top::transport::protobuf::RoutingMessage::SharedDtor() (transport.pb.cc:2870)
==5004==    by 0x693A25: top::transport::protobuf::RoutingMessage::~RoutingMessage() (transport.pb.cc:2858)
==5004==    by 0x674881: top::transport::ThreadHandler::on_databox_open(top::base::xpacket_t&, int, unsigned long) (multi_message_handler.cc:98)
==5004==    by 0x14B2450: top::base::xdatabox_t::process_packets(int, unsigned int, int, unsigned long) (xmailbox.cpp:541)
==5004==    by 0x14B219F: top::base::xdatabox_t::on_signal_up(int, int, unsigned long) (xmailbox.cpp:499)
==5004==    by 0x14AF9DC: top::base::xiosignaler_t::on_iohandle_read(int, unsigned int&, int, unsigned long) (xsignaler.cpp:543)
==5004==    by 0x14CEAC3: top::base::xuvpoll_t::on_iohandle_read(unsigned int&, int, unsigned long) (xuvimpl.cpp:492)
==5004==    by 0x14CD8CB: top::base::xuvpoll_t::static_uvpoll_on_poll_io_callback(uv_poll_s*, int, int) (xuvimpl.cpp:332)
==5004==    by 0x14E38B7: uv__io_poll (linux-core.c:401)
==5004==    by 0x14D9C37: uv_run (core.c:370)
==5004==    by 0x14D0250: top::base::xuvthread_t::loop() (xuvimpl.cpp:782)
==5004==    by 0x14B631B: top::base::xthread_t::on_thread_run() (xthread.cpp:109)
==5004==    by 0x14B5D8C: top::base::xthread_t::static_thread_entry(void*) (xthread.cpp:29)
==5004==    by 0x527EEA4: start_thread (in /usr/lib64/libpthread-2.17.so)
==5004==    by 0x5FB88DC: clone (in /usr/lib64/libc-2.17.so)
==5004==  If you believe this happened as a result of a stack
==5004==  overflow in your program's main thread (unlikely but
==5004==  possible), you can try to increase the size of the
==5004==  main thread stack using the --main-stacksize= flag.
==5004==  The main thread stack size used in this run was 8388608.
```

上面最后几句话建议可以使用  `--main-stacksize` 参数，并且增大这个参数的值：

```
--main-stacksize=<number> [default: use current 'ulimit' value]
Specifies the size of the main thread's stack.
To simplify its memory management, Valgrind reserves all required space for the main thread's stack at startup. That means it needs to know the required stack size at startup.

By default, Valgrind uses the current "ulimit" value for the stack size, or 16 MB, whichever is lower. In many cases this gives a stack size in the range 8 to 16 MB, which almost never overflows for most applications.

If you need a larger total stack size, use --main-stacksize to specify it. Only set it as high as you need, since reserving far more space than you need (that is, hundreds of megabytes more than you need) constrains Valgrind's memory allocators and may reduce the total amount of memory that Valgrind can use. This is only really of significance on 32-bit machines.

On Linux, you may request a stack of size up to 2GB. Valgrind will stop with a diagnostic message if the stack cannot be allocated.

--main-stacksize only affects the stack size for the program's initial thread. It has no bearing on the size of thread stacks, as Valgrind does not allocate those.

You may need to use both --main-stacksize and --max-stackframe together. It is important to understand that --main-stacksize sets the maximum total stack size, whilst --max-stackframe specifies the largest size of any one stack frame. You will have to work out the --main-stacksize value for yourself (usually, if your applications segfaults). But Valgrind will tell you the needed --max-stackframe size, if necessary.

As discussed further in the description of --max-stackframe, a requirement for a large stack is a sign of potential portability problems. You are best advised to place all large data in heap-allocated memory.
```

# udp 重放攻击

```
tcpdump  -i lo udp and dst port 9000 and src port 9002 -v -s 0  -w rec2_to_re1.pcap


tcprewrite   --infile=rec2_to_re1.pcap  --outfile=rec2_to_rec12.pcap —fixcsum


tcpreplay -v -i lo -l 100 -p 1000 rec2_to_rec12.pcap
```

# beyond compare 永久试用
亲测可用

一、原理

Beyond Compare每次启动后会先检查注册信息，试用期到期后就不能继续使用。解决方法是在启动前，先删除注册信息，然后再启动，这样就可以永久免费试用了。

二、下载

首先下载Beyond Compare最新版本，链接如下：https://www.scootersoftware.com/download.php

三、安装

下载完成后，直接安装。

四、创建BCompare文件

1 进入Mac应用程序目录下，找到刚刚安装好的Beyond Compare，路径如下/Applications/Beyond Compare.app/Contents/MacOS

2 修改启动程序文件BCompare为BCompare.real

3 在当前目录下新建一个文件BCompare，文件内容如下： 

```
#!/bin/bash

rm "/Users/$(whoami)/Library/Application Support/Beyond Compare/registry.dat"
"`dirname "$0"`"/BCompare.real $@ 
```

4 保存BCompare文件

5 修改文件的权限：

```
chmod a+x /Applications/Beyond\ Compare.app/Contents/MacOS/BCompare
```

6 以上步骤完成后，再次打开Beyond Compare就可以正常使用了，enjoy it。

转自：[https://blog.csdn.net/wu__di/article/details/82390196](https://blog.csdn.net/wu__di/article/details/82390196)

# scons warning:Two different environments...

使用 scons 进行编译的时候，碰到一个告警：

```
scons: warning: Two different environments were specified for target /mnt/centos-share/workspace/mux/epoll/epoll_tcp_client.o,
```

解决办法是不要使用 clone env，而使用同一个 env, 解释如下：

```
--warn=no-duplicate-environment


Scons is complaining that you are specifying to build Util.o with two environments. Note that you are cloning the environment inside the test SConscript. SCons does not care that you are building Util.c from different scripts it is just that you are building the same Util.o from two environments.


So, if your test and main program environments are the same just delete the clone inside test SConscript. Basically, SCons will do what you were suggesting with passing nodes.


Otherwise, things get a little complicated and you have to build two Util.o, one for the main program and one for the test program. Then you have to dabble into build_dir option of the SConscript() function
```

关于 scons 的使用可以参考我的博文： [Scons构建C++项目](http://rebootcat.com/2020/08/30/scons/)

# ddos 和 cc 攻击区别

## ddos

DDoS全称:分布式拒绝服务(DDoS:Distributed Denial of Service)。信息安全的三要素——“保密性”、“完整性”和“可用性”中，拒绝服务攻击，针对的目标正是“可用性”。该攻击方式利用目标系统网络服务功能缺陷或者直接消耗其系统资源，使得该目标系统无法提供正常的服务。拒绝服务攻击问题一直得不到合理的解决，目前还是世界性难题，究其原因是因为这是由于网络协议本身的安全缺陷造成的，（这里不细说，详情自行百度）从而拒绝服务攻击也成为了攻击者的终极手法。攻击者进行拒绝服务攻击，实际上让服务器实现两种效果：一是迫使服务器的缓冲区满，不接收新的请求；二是使用IP欺骗，迫使服务器把合法用户的连接复位，影响合法用户的连接。
在这里补充两点：第一就是DDOS攻击不仅能攻击计算机，还能攻击路由器，因为路由器是一台特殊类型的计算机；第二是网速决定攻击的好和快，比如说，如果你一个被限制网速的环境下，它们的攻击效果不是很明显，但是快的网速相比之下更加具有攻击效果。

## cc
CC攻击全称Challenge Collapsar，中文意思是挑战黑洞，因为以前的抵抗DDoS攻击的安全设备叫黑洞，顾名思义挑战黑洞就是说黑洞拿这种攻击没办法，新一代的抗DDoS设备已经改名为ADS(Anti-DDoS System)，基本上已经可以完美的抵御CC攻击了。CC攻击的原理是通过代理服务器或者大量肉鸡模拟多个用户访问目标网站的动态页面，制造大量的后台数据库查询动作，消耗目标CPU资源，造成拒绝服务。CC不像DDoS可以用硬件防火墙来过滤攻击，CC攻击本身的请求就是正常的请求。我们都知道网站的页面有静态和动态之分，动态网页是需要与后台数据库进行交互的，比如一些论坛用户登录的时候需要去数据库查询你的等级、权限等等，当你留言的时候又需要查询权限、同步数据等等，这就消耗很多CPU资源，造成静态网页能打开，但是需要和数据库交互的动态网页打开慢或者无法打开的现象。这种攻击方式相对于前两种实现要相对复杂一些，但是防御起来要简单的多，提供服务的企业只要尽量少用动态网页并且让一些操作提供验证码就能抵御一般的CC攻击。
CC攻击的种类有三种，直接攻击，代理攻击，僵尸网络攻击，直接攻击主要针对有重要缺陷的 WEB 应用程序，一般说来是程序写的有问题的时候才会出现这种情况，比较少见。僵尸网络攻击有点类似于 DDOS 攻击了，从 WEB 应用程序层面上已经无法防御，所以代理攻击是CC 攻击者一般会操作一批代理服务器，比方说 100 个代理，然后每个代理同时发出 10 个请求，这样 WEB 服务器同时收到 1000 个并发请求的，并且在发出请求后，立刻断掉与代理的连接，避免代理返回的数据将本身的带宽堵死，而不能发动再次请求，这时 WEB 服务器会将响应这些请求的进程进行队列，数据库服务器也同样如此，这样一来，正常请求将会被排在很后被处理，就象本来你去食堂吃饭时，一般只有不到十个人在排队，今天前面却插了一千个人，那么轮到你的机会就很小很小了，这时就出现页面打开极其缓慢或者白屏。

## ddos 和 cc 的区别
DDoS攻击打的是网站的服务器，而CC攻击是针对网站的页面攻击的，用术语来说就是，一个是WEB网络层拒绝服务攻击（DDoS），一个是WEB应用层拒绝服务攻击（CC），网络层就是利用肉鸡的流量去攻击目标网站的服务器，针对比较本源的东西去攻击，服务器瘫痪了，那么运行在服务器上的网站肯定也不能正常访问了。而应用层就是我们用户看得到的东西，就比如说网页，CC攻击就是针对网页来攻击的，CC攻击本身是正常请求，网站动态页面的正常请求也会和数据库进行交互的，当这种"正常请求"达到一种程度的时候，服务器就会响应不过来，从而崩溃。

**DDoS是针对IP的攻击，而CC攻击的是服务器资源**。

# awk/sort/uniq 配合使用
awk 用来分割字符串，sort 用来排序， uniq 用来去重：

```
$  awk -F'[()]' '{print $2}' xtop*log|sort | uniq -c | sort -k1,1nr | head -30
 353145 on_block:35
  65179 set_object:1502
  62750 elect_vhost.cc: HandleRumorMessage:381
  62750 on_msg:170
  54523 
  51908 adapt_address_imp:68
  30855 on_block_to_db_event:198
  30855 on_unit_to_db:84
```