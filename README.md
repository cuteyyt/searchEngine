# 搜索引擎

浙江大学 2021 年春夏学期 **信息检索与WEB搜索** 课程大作业

[toc]

## 使用

### 文件组织

等待完善

### 环境配置

需要 python 3.0 及以上版本。  
推荐 conda 环境。

### 安装 miniSearchEngine

```shell
git clone https://github.com/cuteyyt/searchEngine.git
cd searchEngine
pip install -e .
```

### 创建搜索引擎、构建倒排列表等必要文件
使用默认参数构建搜索引擎:
```shell
construct_engine
```

查看参数说明:
```shell
construct_engine -h
```

### 启动搜索引擎

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
# 使用一下命令退出搜索引擎
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
    'a': {
        1: 1.1,  # doc_id: tf-idf
        2: 2.2,
        # ...
    },
    'b': {
        1: 1.1,  # doc_id: tf-idf
        2: 2.2,
        # ...
    },
    # ...
}
```

#### 快速词项定位
1. 基于哈希表的词典索引
python 字典本身就是基于哈希表实现
2. 基于搜索树的词典索引

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

### 索引构建

TODO

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

## 其他



