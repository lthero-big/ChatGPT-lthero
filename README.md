# ChatGPT-lthero

## 安装依赖

```
pip install -r requirements.txt
```



## 运行代码

```
python index.py
```

或者尝试

```
python3 index.py
```



## 使用

1. 必须在代码中设置userApiKey，或者在运行后的网页setting输入userApiKey
2. 支持自行动态调整topP,temperature等参数
3. 回复支持Markdown语法
4. 左侧的LastResponse部分支持markdown格式的代码显示，但仅显示ChatGPT回复的最后一条信息。





## 部署

1. 默认只能本机访问：程序最后一条代码`blocks.launch(server_name="127.0.0.1", server_port=7860, debug=False)`。

2. 如果需要部署在服务器，并设置公网访问，要将上述代码`127.0.0.1`修改成`0.0.0.1`，并需要自行放开端口`7860`号

3. 如果没有自己服务器，`blocks.launch(server_name="127.0.0.1", server_port=7860, debug=True)`，程序会自己创建一个公网访问的链接，但必须让程序持续运行

   





## 参数说明

### openAPI

是chatGPT访问链接

默认值：https://api.openai.com/v1/chat/completions

如果想部署在自己国内服务器上，需要使用国内能访问的api

具体方案请查看：https://github.com/noobnooc/noobnooc/discussions/9



### userApiKey

是chatGPT的api，每个账号有18美元额度

默认值：NULL

在openai申请api

具体查看：https://platform.openai.com/account/api-keys



### temperature

温度较高，则生成的文本将更加多样化，但存在语法错误和产生无意义内容的风险更高。

温度较低，意味着模型会更加保守，并坚持从其训练数据中学到的内容，导致预测结果更可预测但创造性较差。

默认值：1



### topP

Top P可以生成与低温相似的准确性和正确性的文本，但具有更多变化和创造力。

如果Top P值设置得太高，则也存在生成无意义或不相关文本的风险。

默认值：0.5



### presencePenalty

presencePenalty是一些自然语言处理模型中使用的参数，用于惩罚已经在对话中提到过的单词或短语的重复出现。这种惩罚鼓励模型生成更多样化和多变化的回应。

如果presencePenalty参数变得很高，它将强烈阻止已经在对话中提到过的单词或短语的重复出现。这可能会导致模型生成更多样化和多变化的回应，但如果模型无法正确地将先前提到的信息纳入其输出中，则可能会导致不太连贯或相关的回应。

默认值：0



### frequencyPenalty

用于惩罚生成的回应中过于频繁出现的单词或短语。这个惩罚的目的是鼓励模型使用更广泛的词汇并产生更多样化和有趣的回应。如果将frequencyPenalty设置得太高，则可能会导致不太连贯或相关的回应

默认值：0



### maxTokens

单次对话最大token量

默认值:500
