---
title: Scons构建C++项目
date: 2020/04/11 11:23:58
tags: 
	- blockchain
	- attack
	- bitcoin
categories:
	- blockchain
comments: 
---

# 前言
我是一个 linux c++ 开发者，但是一直对 Makefile 的语法很是头痛，每次都记不住，所以每次写 Makefile 都很痛苦，Makefile 里需要你自己编写依赖和推导规则，这个过程能不能简单点呢？

对于编译一个 C++ 工程来说，也许需要的就是头文件路径、库路径、编译参数，剩下的东西基本也不重要，这三样足够去编译一个工程了。所以有没有一个工具能简单点的去实现 C++ 项目的构建呢？

答案是有的，Scons 就是答案。

# Scons 
## 什么是 scons
这里直接引用官网的解释：

>What is SCons?
>>SCons is an Open Source software construction tool—that is, a next-generation build tool. Think of SCons as an improved, cross-platform substitute for the classic Make utility with integrated functionality similar to autoconf/automake and compiler caches such as ccache. In short, SCons is an easier, more reliable and faster way to build software.


>What makes SCons better?

>>
+ Configuration files are Python scripts--use the power of a real programming language to solve build problems.
+ Reliable, automatic dependency analysis built-in for C, C++ and Fortran--no more "make depend" or "make clean" to get all of the dependencies. Dependency analysis is easily extensible through user-defined dependency Scanners for other languages or file types.
+ Built-in support for C, C++, D, Java, Fortran, Yacc, Lex, Qt and SWIG, and building TeX and LaTeX documents. Easily extensible through user-defined Builders for other languages or file types.
+ Building from central repositories of source code and/or pre-built targets.
+ Built-in support for fetching source files from SCCS, RCS, CVS, BitKeeper and Perforce.
+ Built-in support for Microsoft Visual Studio .NET and past Visual Studio versions, including generation of .dsp, .dsw, .sln and .vcproj files.
+ Reliable detection of build changes using MD5 signatures; optional, configurable support for traditional timestamps.
+ Improved support for parallel builds--like make -j but keeps N jobs running simultaneously regardless of directory hierarchy.
+ Integrated Autoconf-like support for finding #include files, libraries, functions and typedefs.
+ Global view of all dependencies--no more multiple build passes or reordering targets to build everything.
+ Ability to share built files in a cache to speed up multiple builds--like ccache but for any type of target file, not just C/C++ compilation.
+ Designed from the ground up for cross-platform builds, and known to work on Linux, other POSIX systems (including AIX, BSD systems, HP/UX, IRIX and Solaris), Windows NT, Mac OS X, and OS/2.


最大特点就是使用 Python 语法来编写编译构建脚本，并且支持依赖自动推导，支持编译 C/C++/D/Java/Fortran等项目，并且是跨平台的(因为 python 是跨平台的）。

<!-- more -->

所以如果你对 python 熟悉的话，而且你和我对 C++  Makefile 有一样的烦恼，那么这对你将是一个好消息。 你将可以用 python 来编写构建脚本，而且会很简单，对于复杂的大型项目也能快速构建好。（也许只要 30 分钟）


## 安装 scons

因为 scons 是基于 python 来构建的，所以毋容置疑，首先是需要准备好 python 环境，然后使用下述命令安装 scons 工具。

```
pip install scons
```

## scons 使用语法
scons 构建脚本由一个 SConstruct 文件和多个 SConscript 文件构成。


SConstruct 通常位于项目顶层目录，然后 SConscript 通常位于子目录（子模块）。

那么来看一下 SConstruct 脚本长啥样?

### SConstruct

```
#!/usr/bin/env python
#-*- coding:utf-8 -*-


import sys
import os
import platform
import re

env = Environment()
abs_path = os.getcwd()
print('workspace path:{0}'.format(abs_path))

sbuild_dir = 'sbuild'

headers = ['.', 'third-party/include']
libs = ['./third-party/lib']

abs_headers = []
abs_libs = []

for item in headers:
    abs_item = os.path.join(abs_path, item)
    abs_headers.append(abs_item)


for item in libs:
    abs_item = os.path.join(abs_path, item)
    abs_libs.append(abs_item)

build_dir = os.path.join(abs_path, sbuild_dir)
abs_libs.append(os.path.join(build_dir, 'lib'))

CCFLAGS = '-ggdb -std=c++11'

print('\nheaders path:')
print(abs_headers)
print('\n')

print('libs path:')
print(abs_libs)
print('\n')

print("begin load SConscript")

env["headers"] = abs_headers
env["libs"]    = abs_libs
env["MUX_DIR"] = abs_path
env['ccflags'] = CCFLAGS
env['build_dir'] = build_dir

Export('env')

SConscript(['./mbase/SConscript'])
SConscript(['./message_handle/SConscript'])
SConscript(['./epoll/SConscript'])
SConscript(['./transport/SConscript'])
SConscript(['./demo/bench/SConscript'])
SConscript(['./demo/echo/SConscript'])

print("\n All Done, Please Check {0}".format(env['build_dir']))

```

来分析一下这个文件，源文件可以直接在 [我的github](https://github.com/smaugx/mux/blob/master/SConstruct)下载。

SConstruct 文件主要做了两件事：

+ env 环境变量的构造，主要是头文件路径，库路径，编译参数，自定义的一些变量等
+ 使用 SConscript 函数解析执行子模块的 SConscript 文件 

需要注意的是 SConstruct 和 SConscript 共享变量使用的就是 env 这个变量，你可以看到上面有一句：


```
Export('env')
```

这句很重要。


### SConscript

那么位于子模块或者子目录的 SConscript 文件长啥样呢？

```
#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys

Import('env')
project_dir  = env['MUX_DIR']

epoll_lib  = 'epoll'

epoll_src_path = os.path.join(project_dir, 'epoll/src')
epoll_sources = []
for item in os.listdir(epoll_src_path):
    if item.endswith('.cc') or item.endswith('.cpp') or item.endswith('.cxx'):
        abs_item = os.path.join(epoll_src_path, item)
        epoll_sources.append(abs_item)

print('\nbuild target:lib{0}.a'.format(epoll_lib))
print(epoll_sources)

lib_dir = os.path.join(env['build_dir'], 'lib')

link_libraries = ['mbase']
for lib_name in link_libraries:
    lib_name = "{0}{1}{2}".format(env['LIBPREFIX'], lib_name, env['LIBSUFFIX'])
    abs_lib_name = os.path.join(lib_dir, lib_name)
    epoll_sources.append(abs_lib_name)

env.StaticLibrary(target = os.path.join(lib_dir, epoll_lib),
        source  = epoll_sources,
        CPPPATH = env['headers'], # include
        LIBPATH = env['libs'],    # lib path
        LIBS    = ['pthread'],    # link lib
        CCFLAGS = env['ccflags']
        )
        
```

来分析一下这个文件，源文件可以直接在 [我的github](https://github.com/smaugx/mux/blob/master/epoll/SConscript)下载。

SConscript 主要做了两件事：

+ 构造一个源文件列表（用来构建 target 所需要使用的源文件）
+ 根据需要构建 static_lib/dynamic_lib/binary


当然，还有一点很重要，上面其实提到了，SConscript 和 SConstruct 用来共享变量使用的是 env 这个变量，所以你可以看到一句很重要的：

```
Import('env')
```

构造源文件列表，对于 Python 来说，简直是小菜一碟，太简单了；

然后如何生成目标文件呢？


1 生成二进制文件

```
env.Program(target = os.path.join(bin_dir, echo_server_bin),
        source  = echo_server_sources,
        CPPPATH = env['headers'],
        LIBPATH = env['libs'],
        LIBS    = ['transport','msghandler','epoll', 'mbase', 'pthread'],
        CCFLAGS = env['ccflags']
        )
```

2  生成静态库

```
env.StaticLibrary(target = os.path.join(lib_dir, epoll_lib),
        source  = epoll_sources,
        CPPPATH = env['headers'], # include
        LIBPATH = env['libs'],    # lib path
        LIBS    = ['pthread'],    # link lib
        CCFLAGS = env['ccflags']
        )
```

3 生成动态库

```
env.SharedLibrary(target = os.path.join(lib_dir, epoll_lib),
        source  = epoll_sources,
        CPPPATH = env['headers'], # include
        LIBPATH = env['libs'],    # lib path
        LIBS    = ['pthread'],    # link lib
        CCFLAGS = env['ccflags']
        )

```

上面 3 个函数的参数都是类似的：

+ target: 指定需要生成的目标文件，通常我自己会写一个绝对路径；对于 lib 来说只需要写名字就行，前缀和后缀不需要写。(eg. target = '/root/scons\_repo/sbuild/lib/test' ，会生成 /root/scons\_repo/sbuild/lib/libtest.a)
+ source: 编译目标文件需要的源文件列表
+ CPPPATH: 通常就是需要 Include 的头文件路径
+ LIBPATH: 通常就是需要链接的库路径
+ LIBS: 需要链接的库列表
+ CCFLAGS: 编译参数


**attention:**

**上面有一个坑我自己碰到的，当我构建目标生成一个静态库的时候，需要链接其他的静态库，如果使用 $LIBPATH 和 $LIBS 指定链接库的话，scons 并没有链接这些库。尝试了很多方法，搜索了很多，也没有解决这个问题**。

**最后是这样解决的。把需要链接的静态库添加到 source 参数中，和其他 cc/cpp 源文件一样放在一起，并且这些库需要使用绝对路径**。

通常为了跨平台的方便，需要考虑lib 的前后缀，可以这样写：

```
link_libraries = ['test1', 'test2']
for lib_name in link_libraries:
    lib_name = "{0}{1}{2}".format(env['LIBPREFIX'], lib_name, env['LIBSUFFIX'])
    abs_lib_name = os.path.join(lib_dir, lib_name)
    sources.append(abs_lib_name)
```


## scons 命令
上面详细讲解了如何使用 python 编写构建脚本，那么写好之后怎么用呢？

常用的几个命令：

**编译**：

```
scons
```

如果需要并行编译：

```
scons -j4
```

**清理**：

```
scons -c
```

然后就会按照你脚本里写的方式去构建目标了。

这里贴一下 [我的项目](https://github.com/smaugx/mux) 编译的输出：


```
$ scons
scons: Reading SConscript files ...
workspace path:/mnt/centos-share/workspace/mux

headers path:
['/mnt/centos-share/workspace/mux/.', '/mnt/centos-share/workspace/mux/third-party/include']


libs path:
['/mnt/centos-share/workspace/mux/./third-party/lib', '/mnt/centos-share/workspace/mux/sbuild/lib']


begin load SConscript

build target:libmbase.a
['/mnt/centos-share/workspace/mux/mbase/src/packet.cc']

build target:libmsghandler.a
['/mnt/centos-share/workspace/mux/message_handle/src/message_handler.cc']

build target:libepoll.a
['/mnt/centos-share/workspace/mux/epoll/src/epoll_tcp_client.cc', '/mnt/centos-share/workspace/mux/epoll/src/epoll_tcp_server.cc']

build target:libtransport.a
['/mnt/centos-share/workspace/mux/transport/src/tcp_transport.cc']

build target:bench_server
['bench_server.cc']

build target:bench_client
['client.cc']

build target:echo_server
['echo_server.cc']

build target:echo_client
['client.cc']

 All Done, Please Check /mnt/centos-share/workspace/mux/sbuild
scons: done reading SConscript files.
scons: Building targets ...
g++ -o demo/bench/bench_server.o -c -ggdb -std=c++11 -I. -Ithird-party/include demo/bench/bench_server.cc
g++ -o demo/bench/client.o -c -ggdb -std=c++11 -I. -Ithird-party/include demo/bench/client.cc
g++ -o demo/echo/client.o -c -ggdb -std=c++11 -I. -Ithird-party/include demo/echo/client.cc
g++ -o demo/echo/echo_server.o -c -ggdb -std=c++11 -I. -Ithird-party/include demo/echo/echo_server.cc
g++ -o epoll/src/epoll_tcp_client.o -c -ggdb -std=c++11 -I. -Ithird-party/include epoll/src/epoll_tcp_client.cc
g++ -o epoll/src/epoll_tcp_server.o -c -ggdb -std=c++11 -I. -Ithird-party/include epoll/src/epoll_tcp_server.cc
g++ -o mbase/src/packet.o -c -ggdb -std=c++11 -I. -Ithird-party/include mbase/src/packet.cc
g++ -o message_handle/src/message_handler.o -c -ggdb -std=c++11 -I. -Ithird-party/include message_handle/src/message_handler.cc
g++ -o transport/src/tcp_transport.o -c -ggdb -std=c++11 -I. -Ithird-party/include transport/src/tcp_transport.cc
ar rc sbuild/lib/libmbase.a mbase/src/packet.o
ranlib sbuild/lib/libmbase.a
ar rc sbuild/lib/libepoll.a epoll/src/epoll_tcp_client.o epoll/src/epoll_tcp_server.o sbuild/lib/libmbase.a
ranlib sbuild/lib/libepoll.a
ar rc sbuild/lib/libtransport.a transport/src/tcp_transport.o sbuild/lib/libepoll.a sbuild/lib/libmbase.a
ranlib sbuild/lib/libtransport.a
ar rc sbuild/lib/libmsghandler.a message_handle/src/message_handler.o sbuild/lib/libmbase.a
ranlib sbuild/lib/libmsghandler.a
g++ -o sbuild/bin/bench_client demo/bench/client.o -Lthird-party/lib -Lsbuild/lib -ltransport -lmsghandler -lepoll -lmbase -lpthread
g++ -o sbuild/bin/bench_server demo/bench/bench_server.o -Lthird-party/lib -Lsbuild/lib -ltransport -lmsghandler -lepoll -lmbase -lpthread
g++ -o sbuild/bin/echo_client demo/echo/client.o -Lthird-party/lib -Lsbuild/lib -ltransport -lmsghandler -lepoll -lmbase -lpthread
g++ -o sbuild/bin/echo_server demo/echo/echo_server.o -Lthird-party/lib -Lsbuild/lib -ltransport -lmsghandler -lepoll -lmbase -lpthread
scons: done building targets.
```


```
$ scons -c
scons: Reading SConscript files ...
workspace path:/mnt/centos-share/workspace/mux

headers path:
['/mnt/centos-share/workspace/mux/.', '/mnt/centos-share/workspace/mux/third-party/include']


libs path:
['/mnt/centos-share/workspace/mux/./third-party/lib', '/mnt/centos-share/workspace/mux/sbuild/lib']


begin load SConscript

build target:libmbase.a
['/mnt/centos-share/workspace/mux/mbase/src/packet.cc']

build target:libmsghandler.a
['/mnt/centos-share/workspace/mux/message_handle/src/message_handler.cc']

build target:libepoll.a
['/mnt/centos-share/workspace/mux/epoll/src/epoll_tcp_client.cc', '/mnt/centos-share/workspace/mux/epoll/src/epoll_tcp_server.cc']

build target:libtransport.a
['/mnt/centos-share/workspace/mux/transport/src/tcp_transport.cc']

build target:bench_server
['bench_server.cc']

build target:bench_client
['client.cc']

build target:echo_server
['echo_server.cc']

build target:echo_client
['client.cc']

 All Done, Please Check /mnt/centos-share/workspace/mux/sbuild
scons: done reading SConscript files.
scons: Cleaning targets ...
Removed demo/bench/bench_server.o
Removed demo/bench/client.o
Removed demo/echo/client.o
Removed demo/echo/echo_server.o
Removed epoll/src/epoll_tcp_client.o
Removed epoll/src/epoll_tcp_server.o
Removed mbase/src/packet.o
Removed message_handle/src/message_handler.o
Removed transport/src/tcp_transport.o
Removed sbuild/lib/libmbase.a
Removed sbuild/lib/libepoll.a
Removed sbuild/lib/libtransport.a
Removed sbuild/lib/libmsghandler.a
Removed sbuild/bin/bench_client
Removed sbuild/bin/bench_server
Removed sbuild/bin/echo_client
Removed sbuild/bin/echo_server
scons: done cleaning targets.
```


# 写在最后
scons 使用 python 脚本来构建项目，如果对 python 熟悉的话，那么编写编译构建脚本将会大大提高效率，再也不用局限在 Makefile 的蛋疼语法里面了。

当然 scons 的缺点也有，据说在大型项目的时候，可能会很慢。这个我还没碰到过，因为没有用到大型项目中。

下一篇，分享下 cmake 构建 C++ 项目的一些语法和步骤。




Blog:
 
+ [rebootcat.com](http://rebootcat.com)

+ email: <linuxcode2niki@gmail.com>

2020-04-11 于杭州   
*By  [史矛革](https://github.com/smaugx)*