# 搜索引擎

浙江大学 2021 年春夏学期 **信息检索与WEB搜索** 课程大作业

GitHub [链接](https://github.com/cuteyyt/searchEngine.git)

**分工**

- 尹幽潭：倒排索引、向量空间模型、索引压缩、使用词典索引
- 付冰洋：布尔查询、通配查询、拼写矫正
- 黄家伟：基于快速评分的Top K查询、短语查询、同义词扩展
- 展示和报告：三人协作，各自完成自己代码对应部分

[TOC]

## 改进

1. 我们借鉴了第二组使用 gzip 对词典等文件进行压缩的做法，文件存储空间确实变小了，下图是未压缩前的文件大小：

   ![before_compress](.\images\before_compress.PNG)

   下图为压缩后的文件大小：

   ![after_compress](.\images\after_compress.PNG)

   可以发现，文件大小可以压缩到原来的四分之一乃至更多。需要注意的是，由于python语言自身的局限（操作 byte 类型的困难性），我们虽然对文档 id 的间隔进行了 vb 编码或 gamma 编码，但可能加载到内存中的词典或是倒排索引大小并没有实际缩小。

2. 优化了拼写矫正的效果，如下图所示：gurantee 被成功矫正为 guarantee 进行查询。

   ![](.\images\gurantee.png)



## 使用

### 文件组织

我们提交的压缩包的文件组织如下图所示：

```shell
group1
├── report.pdf # 这是我们的报告
├── 第一组展示.ppt # 这是我们的展示PPT
├── nltk_data # python nltk 库的依赖文件
└── searchEngine # GitHub 对应 repo，包含代码、报告md源文件、词典文件等
	├── engine # 默认生成的词典文件存放路径，不包含在 git 中
		└── example # 这个文件夹下包含我们所有索引构建方法生成的文件
		├── presentation # 这个文件夹下仅包含一个只含有词项词典和倒排索引的文件
		├── 2021_06_27_23_58_59 # 这个文件夹下是我们默认使用的搜索引擎，可以取得最好效果
		├── 2021_06_28_00_43_27 # 这个文件夹下是更细粒度分词的搜索引擎，但实际效果不好
	├── images # 报告 md 文件用图，包含在 git 中
	├── miniSearchEngine # 代码文件夹，包含在 git 中
	├── miniSearchEngine.egg-info # pip 安装生成的文件夹，不包含在 git 中
	├── Reuters # 数据集，不包含在 git 中
	├── .gitignore
	├── LICENSE
	├── config.json # 记录词典等文件的存储路径，用户可自己修改，包含在 git 中
	├── README.md # 报告 pdf 源文件
	├── setup.cfg
	└── setup.py # 这两个文件执行 python 打包，包含在 git 中
```

### 环境配置

- 需要 windows 10 操作系统

- 需要 python 3.0 及以上版本（推荐 conda 虚拟环境）

`Note：` 我们的 project 可以直接通过命令行使用。使用 -e 方式安装，表示在安装的同时复制源码，所以也支持对我们的 project 进行修改，将其作为 python 库在其他的代码中调用，project 的代码相关文件夹都已经封装成了 python package，可以直接使用 import 导入其中的方法。

`Note：` 如果是解压我们提交的压缩包以后，只需要做**配置 nltk 必要包**这一步操作，然后在命令行输入**start_engine**进行测试即可，其他安装和构建引擎的操作我们已经完成了。如果是从 GitHub 拉取的 project，则需要执行下面所有的配置步骤。

### 安装 miniSearchEngine

```shell
git clone https://github.com/cuteyyt/searchEngine.git
cd searchEngine
pip install -e .
```

### 配置 nltk 必要包

请将`nltk_data`这个文件夹放到路径`C:/users/xxx/`下，并保持名字不变。其中，xxx 是当前 windows 系统的用户名。

### 创建搜索引擎、构建倒排列表等必要文件

单独构建一个只含有词项词典+倒排记录表的文件，用于展示我们索引构建的速度。这部分生成的内容已保存在路径`searchEngine/engine/example`下。

```shell
construct_engine --presentation True
```

使用默认参数构建搜索引擎：将产生一个和我们默认搜索引擎相同参数的引擎文件夹。

```shell
construct_engine
```

在该文件夹下，包含如下文件，使用它们就足以支撑我们的搜索，`args.json`记录了构建搜索引擎所使用的所有参数：

![engine](.\images\engine.PNG)

构建词典+含位置索引的倒排索引的过程需要3~5分钟。

![term_dict_speed](.\images\term_dict_speed.PNG)

同样，向量空间模型的规模与词典相近，也需要3~5分钟。

![vector_model_speed](.\images\vector_model_speed.PNG)

查看构建引擎过程中参数的详细说明和帮助：

```shell
construct_engine -h
```

`Note：` 我们以构建的时间标志不同的引擎文件，每次构建都将在用户指定的文件路径下生成一个以系统当前时间命名的引擎文件夹，内含词典、倒排索引、向量空间模型等等。

`Note：`在实际探索以后，虽然保留了诸如产生 b+ 树这样的参数，但考虑到构建的速度和使用的方便性，即使指定了这些参数，我们也不会生成相应的文件。我们会在构建过程的命令行输出中给出提示，同时，可以参考 `searchEngine/engine/example`文件夹下的文件来查看我们在引擎构建方面所做出的所有探索和努力。对于双词索引、双词拓展、轮排索引、k-gram索引、b+ 树、vb 编码、 gamma 编码、gzip 压缩，我们都有实现。

### 启动搜索引擎

如果不构建搜索引擎，将使用我们默认的引擎文件`searchEngine/engine/2021_06_27_23_58_59`

该引擎基于如下策略建立：

1. 预处理
   - 分词：按空格分词后，仅保留大小写字母和数字，以及'.'（浮点数），'/'和'-'（日期或专有词）。
   - 停用词：不去除。
   - normalization：大写字母统一转为小写。
   - lemmatization：不做。
   - stemming：不做。
2. 引擎内容：除以下三种，其他均不做。
   - 词项词典+含位置索引的倒排记录表
   - 对应向量空间模型

实际测试中，该引擎可取得最优效果。

另一个文件夹`searchEngine/engine/2021_06_28_00_43_27`代表仅根据空格分词的策略下建成的索引，虽然理论上粒度高的引擎能取得更好的搜索效果，但实际测试发现不然。

使用如下命令即可启动引擎进行搜索测试：

```shell
start_engine
```

### 使用命令

模式切换

```shell
# 使用以下三种命令均可切换到模式1:布尔搜索模式（默认）
! switch bool search mode
! switch 1
! s1
# 使用以下命令均可切换到模式2:topk搜索模式
! switch topk mode
! switch 2
! s2
# 使用以下命令均可切换到模式3:k临近算法搜索模式
! switch k nearest search mode
! switch 3
! s3
# 使用以下命令均可切换到模式4:同义词扩展搜索模式
! switch synonym topk mode
! switch 4
! s4
```

拼写矫正开关

```shell
# 使用以下命令均可打开拼写矫正功能（默认）
! open word correction
! open wc
! owc
# 使用以下命令均可关闭拼写矫正功能
! close word correction
! close wc
! cwc
```

展示格式切换

```shell
# 使用以下命令均可切换到简洁模式（默认）
! brief
! b
# 使用以下命令均可切换到扩展模式
! detail
! d
```

退出搜索引擎

```shell
# 使用以下命令退出搜索引擎
! exit
! e
```

### 查询/搜索方法

#### 布尔搜索

布尔搜索内容应当符合如下语法（注意符号与）：

```shell
word
word1 word2   #word1 AND word2
word1 & word2 #word1 AND word2
word1 | word2 #word1 OR word2
~ word        #not word 
( word )
```

示例:

```
! s1
( five | ~ company ) & shares
```

#### 拼写矫正

拼写矫正默认打开，当输入错误的单词时程序会自动矫正。

#### 通配查询

当输入的查询中带有" * "时，程序会对带有" * "的词语做通配搜索（但不可以输入只含有" * "的词语）。

示例：

```
fiv*
*ve
*iv*
f*v*
fiv* company
```

#### 向量空间模型评估相似度、排序

切换到模式2，使用topk搜索模式进行搜索(同时支持拼写矫正和通配查询)。

示例：

```shell
! s2
education
```

#### 短语查询

切换到模式3，使用k nearest搜索模式进行搜索（同时支持拼写矫正和通配查询）。

默认k值为5,即所输入的所有词语的相互间隔不超过5。至少要输入两个词语。

示例：

```
! s3
five company
```

#### 同义词扩展

切换到模式4，使用同义词扩展搜索模式进行搜索。

示例：

```
! s4
education
```



## 简要实现原理

### 数据结构

#### 文档字典 doc dict

```python
doc_dict = {
    1: {  # doc_id
        'file_path': '1.html',  # 文档文件名
        'text': 'mini search engine',  # 文档内容
    },
}
```

#### 词典 term dict

```python
term_dict = {
    'a': {  # 词项
        'doc_feq': 1,  # 文档频率
        'posting_list': {  # 倒排索引
            1: [2, 3, ...],  # 文档 id: [位置索引, ...]
        },
    },
}
```

#### 向量空间模型 vector model

```python
vector_model = {
    1: {
       	'a': 1.1,  # term: tf-idf
        'b': 2.2,
        # ...
    },
    2: {
       	'a': 1.1,  # term: tf-idf
        'b': 2.2,
        # ...
    },
    # ...
}
```

### 布尔搜索

* 使用栈处理布尔搜索所需的表达式。
* 双指针方式处理布尔运算操作中的AND和OR。
* NOT操作时就在所有文章ID中刨去当前词所在的文章的ID。

### 拼写矫正

* 按首字母第一关键字，长度第二关键字，字典序第三关键字存放所有待选词项。

  存储结构大致为：

  ```python
  spell_correction_dict = {
      ('a', 1): ['a'],
      ('a', 2): ['aa', 'ab', 'ac', ...]
      #...
      ('b', 1): ['b'],
      ('b', 2): ['be', 'bh', ...]
      #...
  }
  ```

* 二分查找所有长度与bad word长度相近的词语缩小待选词项范围。

* 计算编辑距离，选择编辑距离较小的词语作为待选词项。

* 从待选词项中选择分数最高的词语作为修正后的词语。分数高的判定方法：编辑距离越小的词语分数越高，如果编辑距离相同，则词频越高的词语分数越高。

### 通配查询

* 给每个词语加上'$'，然后构建轮排索引。

* 按照前两个字母和字典序存放索引，大致结构为

  ```python
  rotation_index = {
  	"$a" : [("$a", "a"), ("$abandon", "abandon"), ...]
      "$b" : [("$b", "b"), ("$back", "back"), ...]
      #...
      "ea" : [("ea$andr","andrea"), ("ea$ap", "apea"), ...]
      #...
  }
  ```

*  将查询分割成若干个词语片段，使用任意一个词语片段在索引中二分查找待选词项。

* 贪心判断得到的每一个待选词项是否符合要求。

  

## 测试

### 启动搜索引擎

```shell
start_engine
```

![](.\images\start_engine.png)

### 向量空间模型评估相似度、排序：

调整模式到topk搜索模式（k默认为10），输入查询。

```
! s2
education
```

![](.\images\topk.png)

### 布尔查询

调整到布尔搜索模式。使用前文提到的表达式规则进行搜索。

* **AND**： "government" AND "policy"

  ```shell
  ! s1
  # 如果希望看到文档中包含查询的具体内容可以使用! d来显示细节
  ! d
  government & policy
  ```

  返回127个结果。

  ![](.\images\bool_and.png)

* **OR**: "billion" OR "million"

  ```shell
  billion | million
  ```

  返回1713个结果。前面几个返回结果都是含"billion"的结果，按回车键可以查看更多带有"billion"或"million"的结果。

  ![](.\images\bool_or.png)

* **NOT**: NOT "fall" AND "rise"

  ```
  ~ fall & rise
  ```

  返回591个结果。

  ![image-20210629195415546](.\images\bool_not.png)

### 通配查询

```
technol*
```

会先列出所有匹配到的词再展示搜索到的结果。

![image-20210629195749709](.\images\technol.png)

```
*formatio*
```

同样先列出匹配的词再列出所有的搜索结果。

![](.\images\formatio.png)

### 短语查询

切换到k nearest搜索模式（默认k为5），再输入要查的短语。

```
! s3
commodity company
```

![image-20210629201729346](.\images\phrase.png)

```
information technology
```

![](.\images\information_technology.png)

### 拼写矫正（改进）

我们改进了选择词语时的策略。使用编辑距离小于2的同时编辑距离最小的词语，如果编辑距离相同，则使用词频最高的一项（改进前是有限词频，其次编辑距离）。

调整回布尔搜索模式，并输入查询。

```
! s1
gurantee
```

首先提示查询词项不存在，并显示改正后的词项：guarantee。然后显示查询结果。

![image-20210629202612976](.\images\gurantee.png)

```
kindom
```

![](.\images\kindom.png)

### 同义词查询

调整到同义词查询模式，并输入查询。

```
! s4
education
```

先显示输入查询中每个词的最多五个同义词，再返回搜索结果。

![image-20210629203212410](.\images\synmoym.png)

### 退出

使用exit命令退出。

```shell
! exit
```

![exit](./images/exit.png)



## 其他

有任何疑问，可以直接联系尹幽潭 [youtanyin@zju.edu.cn]。

