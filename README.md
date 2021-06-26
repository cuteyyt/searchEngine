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

### 创建搜索引擎
```shell
construct_engine
```
使用默认参数，将会...
```shell
construct_engine -h
```
查看参数说明。

### 查询/搜索

3. Bool Search

Input should follow such format(spaces are needed anywhere)：

```
word
word1 word2
word1 & word2 
word1 | word2
~ word
( word )
```

example:

```
( five | ~ company ) & shares
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

## 其他