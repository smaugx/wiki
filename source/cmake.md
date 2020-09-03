---
title: cmake教程|cmake入门实战
date: 2020/04/11 11:23:58
tags: 
	- cmake
	- CMakeLists.txt
	- scons
	- c++
	- c
	- linux
	- compile
	- build
categories:
	- c++
comments: 
---

# 前言
我是一个 linux c++ 开发者，但是一直对 Makefile 的语法很是头痛，每次都记不住，所以每次写 Makefile 都很痛苦，Makefile 里需要你自己编写依赖和推导规则，这个过程能不能简单点呢？

对于编译一个 C++ 工程来说，也许需要的就是头文件路径、库路径、编译参数，剩下的东西基本也不重要，这三样足够去编译一个工程了。所以有没有一个工具能简单点的去实现 C++ 项目的构建呢？

答案是有的，上一篇博文 [scons构建C++项目](http://rebootcat.com/2020/08/24/scons_build_cplusplus/) 介绍了 使用 scons 来构建 C++ 项目，大大提高了编写构建脚本的效率，使用起来也极为方便，对于熟悉 python 的童鞋来说真的是大大的福音；但 scons 的问题就是在大型项目的时候构建起来可能会很慢（听说的）。那么有没有其他的工具呢？

当然有，cmake 就是这样的一个工具，既能满足跨平台的编译，并且屏蔽了 Makefile 蛋疼的语法，使用一种更加简单的语法编写构建脚本，用在大型项目也毫无压力。

当然，对于我个人来说，cmake 的使用还是有门槛的，刚接触 cmake 可能还是会被它的语法搞的头疼（cmake 的语法也还是挺折腾的）。但是别急，沉下心来，本篇博文就带你从 cmake 入门到编写一个复杂工程的实战。

# CMake
## 什么是 cmake
这里直接引用官网的解释：

>CMake is an open-source, cross-platform family of tools designed to build, test and package software. CMake is used to control the software compilation process using simple platform and compiler independent configuration files, and generate native makefiles and workspaces that can be used in the compiler environment of your choice. The suite of CMake tools were created by Kitware in response to the need for a powerful, cross-platform build environment for open-source projects such as ITK and VTK.

CMake 是一个开源你跨平台的构建工具，语法简单，编译独立，并且很多知名大型项目也在用 CMake,比如 KDE、Netflix 、ReactOS等。

![](https://cdn.jsdelivr.net/gh/smaugx/MyblogImgHosting_2/rebootcat/cmake/1.png)

<!-- more -->

OK，话不多说，如何使用呢？


## 安装 cmake

```
sudo yum install  cmake3.x86_64
```

现在最新版的 cmake 已经到 3.18.2 了。我使用的是 3.17.2 版本。

```
$ cmake --version
cmake version 3.17.2

CMake suite maintained and supported by Kitware (kitware.com/cmake).
```

## 初识 cmake
使用 cmake 来构建 C++ 项目，需要先编写 cmake 构建脚本，文件名为  CMakeLists.txt，项目顶层目录需要放一个 CMakeLists.txt，同时子目录可以根据需要放置 CMakeLists.txt。

那么先来看看 CMakeLists.txt 长啥样?

```
cmake_minimum_required(VERSION 3.8.0)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

project(MUX CXX C)

add_definitions(
    -DTEST1   # define marco
    -DTEST2   # define marco
)

# common compiling options
add_compile_options(
    -Wl,--no-as-needed
    -fno-strict-aliasing
    -fthreadsafe-statics
    -pthread
    #-fstack-protector-strong
    -fno-short-enums
    -fPIC
)

option(XENABLE_TEST3  "enable test3 marco" OFF)

set(EXECUTABLE_OUTPUT_PATH ${MUX_BINARY_DIR}/bin)
set(LIBRARY_OUTPUT_PATH ${MUX_BINARY_DIR}/lib)

if (XENABLE_TEST3)
    add_definitions(-DTEST3)
endif()

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()


message(STATUS "CMAKE_BUILD_TYPE:" ${CMAKE_BUILD_TYPE})
message(STATUS "CMAKE_SYSTEM_NAME:" ${CMAKE_SYSTEM_NAME})
message(STATUS "XENABLE_TEST3:" ${XENABLE_TEST3})

find_package(Threads REQUIRED)

# include header dirs
include_directories(${CMAKE_SOURCE_DIR})   # project dir
include_directories(${CMAKE_SOURCE_DIR}/third-party/include)   # project dir
include_directories(${CMAKE_CURRENT_BINARY_DIR})  # current CMakeLists.txt dir (including sub dir)

# link lib dirs
link_directories(${CMAKE_SOURCE_DIR}/third-party/lib)
link_directories(${LIBRARY_OUTPUT_PATH})  # generate in building

add_subdirectory(demo/bench)
add_subdirectory(demo/echo)
add_subdirectory(epoll)
add_subdirectory(mbase)
add_subdirectory(message_handle)
add_subdirectory(transport)
```

完整的 CMakeLists.txt 见 [我的github](https://github.com/smaugx/mux/blob/master/CMakeLists.txt)，同时我也会以我的github项目 [mux](https://github.com/smaugx/mux) 为例，介绍 cmake 的使用。


上面的 CMakeLists.txt 乍一看，好多内容，但是别慌，我们来一个个说。

## 详解 cmake

注意：**cmake 的语法可以分为命令(函数）和参数。 命令不缺分大小写，参数区分大小写**。

注意：**cmake 的语法可以分为命令(函数）和参数。 命令不缺分大小写，参数区分大小写**。

### 设置 cmake 版本的要求

```
cmake_minimum_required(VERSION 3.8.0)
```

### 在 cmake 中设置 c++ 标准，启用 c++11 或以上(根据项目的需求来）

```
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

```

### 设置项目名以及项目语言

```
project(MUX CXX C)
```

设置完项目名称之后，会自动创建两个变量 `<PROJECT-NAME>_SOURCE_DIR` 和 `<PROJECT-NAME>_BINARY_DIR`，对于 [mux](https://github.com/smaugx/mux) 这个项目来说，也就是 `MUX_SOURCE_DIR` 和 `MUX_BINARY_DIR`。

`MUX_SOURCE_DIR` 表示工程顶层目录； `MUX_BINARY_DIR` 表示 cmake 构建发生的目录。

因为你一定熟悉或者用过下面的命令或步骤：

```
mkdir cbuild
cd cbuild
cmake ..
make
make test
make install
```

通常我们会单独新建一个  cbuild 目录，用来构建项目，并且存放过程中产生的文件。那么 cbuild 目录就是 `MUX_BINARY_DIR` 表示的目录，cbuild 的上一级目录也就是项目顶层目录就是 `MUX_SOURCE_DIR` 表示的目录。

> 如果你没有单独新建 `cbuild` 目录，而是直接在项目顶层目录使用 `cmake ..` ，那么上面两个变量均指项目顶层目录。


详见 [https://cmake.org/cmake/help/latest/command/project.html](https://cmake.org/cmake/help/latest/command/project.html)

### 添加编译宏

```
add_definitions(
    -DTEST1   # define marco
    -DTEST2   # define marco
)

```

上面是我随便写的两个宏 `TEST1` 和 `TEST2`，那么在c++代码中通常是这样的：

```
#ifdef TEST1
    // do something about test1
#endif


#ifdef TEST2
   // do something about test2
#endif
```

当然要开启这个宏也可以不用写在 CMakeLists.txt 文件中，可以直接这样使用：

```
mkdir cbuild && cd cbuild 
cmake .. -DTEST1
```

这个根据你的项目需求来操作。


### 定义一些用户自定义的可选项

```
option(XENABLE_TEST3  "enable test3 marco" OFF)

if (XENABLE_TEST3)
    add_definitions(-DTEST3)
endif()

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()
```

使用 option 命令可以自定义一些变量的值，作为一些条件判断的开关很方便。

详见 [https://cmake.org/cmake/help/latest/command/option.html](https://cmake.org/cmake/help/latest/command/option.html)


### 添加编译选项

```
# common compiling options
add_compile_options(
    -Wl,--no-as-needed
    -fno-strict-aliasing
    -fthreadsafe-statics
    -pthread
    #-fstack-protector-strong
    -fno-short-enums
    -fPIC
)
```

这里就是一些编译选项，根据自己的项目需求修改。

### 设置编译二进制(binary-executable 和 binary-lib）存放路径

```
set(EXECUTABLE_OUTPUT_PATH ${MUX_BINARY_DIR}/bin)
set(LIBRARY_OUTPUT_PATH ${MUX_BINARY_DIR}/lib)
```
可以看到上面用到了 `MUX_BINARY_DIR` 这个变量，也就是说最终编译出来的二进制程序和lib 库会存放在 `cbuild/bin` 和 `cbuild/lib` 中。

### 打印一些信息到终端

```
message(STATUS "CMAKE_BUILD_TYPE:" ${CMAKE_BUILD_TYPE})
message(STATUS "CMAKE_SYSTEM_NAME:" ${CMAKE_SYSTEM_NAME})
message(STATUS "XENABLE_TEST3:" ${XENABLE_TEST3})
```

打印一些调试信息，或者编译信息到终端，使用的是 message 命令。

详见 [https://cmake.org/cmake/help/latest/command/message.html](https://cmake.org/cmake/help/latest/command/message.html)。

### 设置头文件路径

```
# include header dirs
include_directories(${CMAKE_SOURCE_DIR})   # project dir
include_directories(${CMAKE_SOURCE_DIR}/third-party/include)   # project dir
include_directories(${CMAKE_CURRENT_BINARY_DIR})  # current CMakeLists.txt dir (including sub dir)
```

分别解释一下：

`CMAKE_SOURCE_DIR` 表示工程顶层目录，也就是 `MUX_SOURCE_DIR`；

`CMAKE_CURRENT_BINARY_DIR` 表示当前处理的 CMakeLists.txt 所在的目录，对于子目录中的 CMakeLists.txt 来说，即表示这个子目录。

通常这两个是常用的，必须的。然后使用 `include_directories` 命令包含其他的一些头文件路径。


### 设置依赖库的路径

```
# link lib dirs
link_directories(${CMAKE_SOURCE_DIR}/third-party/lib)
link_directories(${LIBRARY_OUTPUT_PATH})  # generate in building
```

`LIBRARY_OUTPUT_PATH` 就是上面设置的编译目标二进制库的存放路径，因为实际项目中，子模块之间可能会有一些依赖，子模块单独编译成一个库，然后让其他模块链接。这个目录也就是 `cbuild/lib` 目录。


### 引入子模块(子目录）

```
add_subdirectory(demo/bench)
add_subdirectory(demo/echo)
add_subdirectory(epoll)
add_subdirectory(mbase)
add_subdirectory(message_handle)
add_subdirectory(transport)
```

使用 `add_subdirectory` 命令把子模块包含进来，必须确保每个子目录下面有一个 CMakeLists.txt 文件，不然会报错。

**以上就是工程顶层目录的 CMakeLists.txt 的内容，分析下来是不是很清楚呢**？


那么工程顶层目录的 CMakeLists.txt 其实做的事情就是设置一些基本的变量，宏开关，编译参数，头文件路径，依赖库路径，编译目标保存路径等等，子目录中的 CMakeLists.txt 才是真正产生编译目标的（exe和lib)。


### 生成静态库/动态库

```
# keep all cpp files in varibale ${epoll_src}
aux_source_directory(./src epoll_src)

add_library(epoll STATIC ${epoll_src})

add_dependencies(epoll mbase )
target_link_libraries(epoll mbase pthread)
```

源文件在这：[戳我](https://github.com/smaugx/mux/blob/master/epoll/CMakeLists.txt)

使用 `aux_source_directory` 添加源文件，相当于把 src 目录下的所有 c++ 文件保存到 `epoll_src` 这个变量中；

使用 `add_library` 生成目标库（根据需要可以生成静态库和动态库，分别使用 STATIC 和 SHARED)

然后就是添加这个模块需要依赖到的其他模块，以及链接参数。

上面的代码最终就会在 `cbuild/lib` 目录下生成一个 `libepoll.a` 文件。

### 生成二进制可执行文件

```
# build target echo_server
add_executable(echo_server echo_server.cc)
add_dependencies(echo_server transport msghandler mbase)
target_link_libraries(echo_server transport msghandler mbase)


# build target echo_client
add_executable(echo_client client.cc)
add_dependencies(echo_client transport msghandler mbase)
target_link_libraries(echo_client transport msghandler mbase)
```

源文件在这：[戳我](https://github.com/smaugx/mux/blob/master/demo/echo/CMakeLists.txt)

和生成库大体是类似的，区别是使用的是 `add_executable` 这个命令。


其他子模块的 CMakeLists.txt 见[我的github](https://github.com/smaugx/mux).



## cmake 编译构建

上面详细的介绍了 CMakeLists.txt 的写法，如果仿照本文，应该也能写出适合你项目的构建脚本，但是可能还不够，其他语法自行 google 学习。

上面其实是以我的项目 []() 进行的演示，有必要解读一下这个项目的结构层次：


```
$ tree mux -d
mux
├── demo
│   ├── bench
│   └── echo
├── epoll
│   ├── include
│   └── src
├── mbase
│   └── src
├── message_handle
│   ├── include
│   └── src
├── third-party
│   ├── include
│   │   ├── nlohmann
│   │   └── spdlog
│   │       ├── cfg
│   │       ├── details
│   │       ├── fmt
│   │       │   └── bundled
│   │       └── sinks
│   └── lib
└── transport
    ├── include
    └── src

24 directories
```

mux 是工程顶层目录，下面包含的 `epoll`、`mbase`、`message_handle`、`transport` 这几个目录，均打包成一个静态库； `demo` 目录下分别包含 `bench` 和 `echo` 两个目录，这两个目录下需要构建可执行程序。

所以首先是`epoll`、`mbase`、`message_handle`、`transport` 这几个目录生成静态库，然后 `bench` 和 `echo` 下的代码依赖于前面的几个模块，生成可执行程序。

前面其实已经提到了，基本的构建命令如下：

```
mkdir cbuild
cd cbuild
cmake ..
make -j4
```

其中注意，如果你没有单独构建 cbuild 目录的话，可能会生成一些中间临时文件污染了目录。并且注意，cmake 后面的 `..` 表示的是工程顶层的 CMakeLists.txt 的目录。所以如果直接使用的是工程顶层目录构建的话，就应该是 `cmake .`



```
$ cmake ..
-- The CXX compiler identification is GNU 4.8.5
-- The C compiler identification is GNU 4.8.5
-- Check for working CXX compiler: /usr/local/bin/c++
-- Check for working CXX compiler: /usr/local/bin/c++ - works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Check for working C compiler: /usr/local/bin/gcc
-- Check for working C compiler: /usr/local/bin/gcc - works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- CMAKE_BUILD_TYPE:Debug
-- CMAKE_SYSTEM_NAME:Linux
-- XENABLE_TEST3:OFF
-- Looking for pthread.h
-- Looking for pthread.h - found
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Failed
-- Looking for pthread_create in pthreads
-- Looking for pthread_create in pthreads - not found
-- Looking for pthread_create in pthread
-- Looking for pthread_create in pthread - found
-- Found Threads: TRUE
-- Configuring done
-- Generating done
-- Build files have been written to: /mnt/centos-share/workspace/mux/cbuild



$ make -j4
Scanning dependencies of target mbase
[  5%] Building CXX object mbase/CMakeFiles/mbase.dir/src/packet.cc.o
[ 11%] Linking CXX static library ../lib/libmbase.a
[ 11%] Built target mbase
Scanning dependencies of target msghandler
Scanning dependencies of target epoll
[ 17%] Building CXX object message_handle/CMakeFiles/msghandler.dir/src/message_handler.cc.o
[ 23%] Building CXX object epoll/CMakeFiles/epoll.dir/src/epoll_tcp_client.cc.o
[ 29%] Building CXX object epoll/CMakeFiles/epoll.dir/src/epoll_tcp_server.cc.o
[ 35%] Linking CXX static library ../lib/libepoll.a
[ 41%] Linking CXX static library ../lib/libmsghandler.a
[ 41%] Built target msghandler
[ 41%] Built target epoll
Scanning dependencies of target transport
[ 47%] Building CXX object transport/CMakeFiles/transport.dir/src/tcp_transport.cc.o
[ 52%] Linking CXX static library ../lib/libtransport.a
[ 52%] Built target transport
Scanning dependencies of target echo_client
Scanning dependencies of target echo_server
Scanning dependencies of target bench_client
Scanning dependencies of target bench_server
[ 58%] Building CXX object demo/echo/CMakeFiles/echo_client.dir/client.cc.o
[ 64%] Building CXX object demo/bench/CMakeFiles/bench_client.dir/client.cc.o
[ 70%] Building CXX object demo/echo/CMakeFiles/echo_server.dir/echo_server.cc.o
[ 76%] Building CXX object demo/bench/CMakeFiles/bench_server.dir/bench_server.cc.o
[ 82%] Linking CXX executable ../../bin/echo_client
[ 88%] Linking CXX executable ../../bin/echo_server
[ 94%] Linking CXX executable ../../bin/bench_server
[100%] Linking CXX executable ../../bin/bench_client
[100%] Built target echo_client
[100%] Built target echo_server
[100%] Built target bench_client
[100%] Built target bench_server
```

看看生成了啥：

```
$ ls cbuild/bin/
bench_client  bench_server  echo_client  echo_server

$ ls cbuild/lib/
libepoll.a  libmbase.a  libmsghandler.a  libtransport.a
```


Over!


# 写在最后
cmake 的构建其实认真熟悉之后，也还是能快速上手的，不要产生排斥心理，不然学起来就很慢很费劲。所以建议第一次接触 cmake 的或者以前一直抵触 cmake 的童鞋，静下心来，认认真真的看完本文或者其他的入门例子，那么你也能快速写一个多目录，多层次结构的 cmake 工程。

cmake 中其他的一些用法，建议随时查看官方的 [cook book](https://cmake.org/cmake/help/latest/index.html).

加油，少年，别怕！


# 参考
[CMake 教程 | CMake 从入门到应用](https://aiden-dong.github.io/2019/07/20/CMake%E6%95%99%E7%A8%8B%E4%B9%8BCMake%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E5%BA%94%E7%94%A8/)

[cmake使用教程](https://juejin.im/post/6844903558861553672)




Blog:
 
+ [rebootcat.com](http://rebootcat.com)

+ email: <linuxcode2niki@gmail.com>

2020-04-11 于杭州   
*By  [史矛革](https://github.com/smaugx)*
