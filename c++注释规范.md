###  c++ 注释风格以及文档生成

为了使用脚本来自动生成文档，特进行一下约定。
- 文件统一使用utf-8 编码
- 对外文件统一使用中文注释，避免生成的文档需要翻译
- 针对指针，引用等类型，一律使用左对齐原则。如下所示
```
    float& a;
    int* b;
```
而不是
```
    float &a;
    float *b;
```

1. 文件头（包括 头文件 .h 和 源文件 .cpp）

    主要用于版权声明，描述本文件的功能，以及作者、版本信息等。

2. 类的定义

    主要用于描述类的功能，同时也可以包含使用方法、注意事项的 brief description。

3. 类的成员变量定义

    对该成员变量进行 brief description。

4. 类的成员函数定义

    对该成员函数的功能进行 brief description。

5. 函数实现

    对函数的功能、参数、返回值、需要注意的问题、相关说明等进行 detailed description。


C++ Comment Style

在写 C++ 代码时，我们应该遵守 C++ 的行注释风格，所谓行注释风格，是指一般 C++ 程序员避免使用 C 风格的注释符号 /* */，而是使用 3 个连续的 / 作为注释的开头。
注释应该紧贴代码。避免跨度较大。比方说

```c++
/// \brief A brief description

class Test;
```

针对不同函数，枚举，结构体等代码。请注意间隔。避免

```
/// \brief test1 desc
void test1();
/// \brief test2 desc
void test2();
```

为了脚本能够正确识别注释和代码。特约定如下

- 一个对象的 brief description 用单行的 /// 开始，并且写在代码前面。一般 brief 写在头文件中，对象的声明之前。


```
    /// \brief A brief description.
    ///
    class Test;
```


File header
文件注释应该包含版权权公告.法律公告和作者信息，以及修改时间
```
/// Copyright(c) Intellif, All right reserved.
///
/// This file is Intellif's property. It contains Intellif's trade secret, proprietary
/// and confidential information.
///
/// DO NOT DISTRIBUTE, DO NOT DUPLICATE OR TRANSMIT IN ANY FORM WITHOUT PROPER
/// AUTHORIZATION.
///
/// If you are not an intended recipient of this file, you must not copy,
/// distribute, modify, or take any action in reliance on it.
///
/// If you have received this file in error, please immediately notify Intellif and
/// permanently delete the original and any copy of any file and any printout
/// thereof.
///
/// \author author_name
/// \version version_number
/// \date xxxx-xx-xx

```

Namespace

namespace 的注释方式：

```
/// \brief A brief namespace description.
///
namespace test
{

}
```


Class

class 的注释方式：

```
/// \brief A brief class description.
///
class test
{

}
```


member function

对于成员函数，请参考function

member variable

对于成员变量，在行末使用 ///<， 请注意不要分开 /// <。


Function

brief:

单行的 /// 注释以及一些结构化的命令，比方有 \param, \return, \tparam 等.以及符合 *\-* 的使用。 *\-* 作为key,value的分隔符。

```
/// \brief function description.
/// \param a - 变量1
/// \param b - 变量2
/// \return 变量1和变量2之和
int add(int a, int b);
```

```
/// \brief template function description
/// \tparam a - 变量1
/// \tparam b - 变量2
/// \return 变量1和变量2之和
template<typename T> 
int add(T a, T b);
```

Variable

变量一般使用 ///< 方式即可：
```
int m_a; ///< brief description for variable m_a
double m_b;  ///< brief description for variable m_b
```


Enum & Struct
为了保持定义统一，统一使用如下格式

类似于 Variable 的注释方式：
```
/// \brief A brief description.
/// 
typedef enum  {
    em_1; ///< enum value em_1
    em_2; ///< enum value em_2
    em_3; ///< enum value em_3
}emVar;
```

避免使用

```
/// \brief A brief description.
/// 
enum  emVar{
    em_1; ///< enum value em_1
    em_2; ///< enum value em_2
    em_3; ///< enum value em_3
};
```

Others

TODO 命令：

```
/// \todo Task1 to do
/// \todo Task2 to do
```

BUG 命令：

```
/// \bug Bug1 to be fixed
/// \bug Bug2 to be fixed
```



代码示例：

```
    ///////////////////////////////////////////////////////////////////////
    ///
    /// Copyright (C), 2014-2020, ***** Tech.Co.Ltd.
    /// All rights reserved.
    /// \author 作者
    /// \version 版本号
    /// \date 日期
    /// \brief 头文件概述
    ///
    /// 开始文件详细概述
    /// Description:    用于详细说明此程序文件完成的主要功能.
    /// History:        修改历史记录列表,每条修改记录应包括修改日期、修改
    ///                 者及修改内容简述.
    ///        <author>  <time>   <version >   <desc>
    ///        David    96 / 10 / 12     1.0     build this moudle
    ///
    ///////////////////////////////////////////////////////////////////////
     
    #pragma once  
    /// \brief 命名空间的简单概述   
    ///   
    namespace text
    {
     
    }
     
    /// \brief 类的简单概述
    ///  
    class Text
    {
    public:
    
    	Text(void);

    	~Text(void);
    	
    	/// \brief 函数简要说明-测试函数 1 
    	/// \param n1 参数1说明  
    	/// \param c2 参数2说明  
    	/// \return 返回说明  
    	bool text1(int n1, Text c2);

    	/// \brief 函数简要说明-测试函数  2
    	/// \param n1 参数1说明  
    	/// \param c2 参数2说明  
    	/// \return 返回说明  
    	bool text2(int n1, Text c2);

    	///  \brief 函数简要说明-测试函数  3
    	/// \param n1 参数1说明  
    	/// \param c2 参数2说明  
    	/// \return 返回说明  
    	bool text3(int n1, Text c2);

    	/// \brief 函数说明-测试函数 4  
    	/// \param n1 参数1说明  
    	/// \param c2 参数2说明  
    	/// \return 返回说明  
    	bool text4(int n1, Text c2);

     
    	int ma;     ///< 成员变量1ma说明  
    	double mb; ///< 成员变量2mb说明  
     
  
    };

    /// \brief xxx枚举变量的简要说明  
    ///  
    typedef enum 
    {
    	EM_1,///< 枚举值1的说明  
    	EM_2,///< 枚举值2的说明  
    	EM_3 ///< 枚举值3的说明  
    }UrlTableErrors;

    /// \brief xxx的简要说明  
    /// 
    typedef struct 
    {
    	d1,///< 变量1的说明  
    	d2,///< 变量2的说明  
    	d3 ///< 变量3的说明  
    }TestData;

     

```

