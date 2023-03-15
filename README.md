# ChatGPT-lthero

在线体验：https://huggingface.co/spaces/lthero/ChatGPT-lthero

在Setting 里可以修改`apiKEY`与`apiHost`，可以克隆此项目，运行速度更快

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

## 关于代码
1. 使用gpt-3.5-turbo模型
2. 练手项目，代码写得不好


## 使用

1. 必须在代码中设置userApiKey，或者在运行后的网页setting输入userApiKey
2. 支持自行动态调整topP,temperature等参数
3. 回复支持Markdown语法
4. 左侧的LastResponse部分支持markdown格式的代码显示，但仅显示ChatGPT回复的最后一条信息。





## 部署

1. 默认只能本机访问：程序最后一条代码`blocks.launch(server_name="127.0.0.1", server_port=7860, debug=False)`。

2. 如果需要部署在服务器，并设置公网访问，要将上述代码`127.0.0.1`修改成`0.0.0.0`，并需要自行放开端口`7860`号

3. 如果没有自己服务器，`blocks.launch(server_name="127.0.0.1", server_port=7860, debug=True)`，程序会自己创建一个公网访问的链接，但必须让程序持续运行

4. 如果想部署在自己国内服务器上，需要使用国内能访问的api，具体方案请查看：noobnooc/noobnooc#9

   
## 自定义域名

使用Nginx反向代理，实现自定义域名访问

在nginx的conf.d这个目录下面，添加一个文件【文件名设置为**要访问的域名**同，如chat.abc.com】，用来让nginx作反向代理。比如创建文件

```SHELL
vim /etc/nginx/conf/conf.d/chat.abc.com.conf
```

### 使用HTTP

nginx配置文件

```nginx
server {
	listen 80;
	# 要修改server，就是域名
    server_name chat.abc.com;
	access_log off;
	error_log off;
	location / {
		# 这里只要修改“7860”运行端口
        # 127.0.0.1不要动，http不要修改成https
		proxy_pass http://127.0.0.1:7860;   
		proxy_redirect off;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_max_temp_file_size 0;
		client_max_body_size 10m;
		client_body_buffer_size 128k;
		proxy_connect_timeout 90;
		proxy_send_timeout 90;
		proxy_read_timeout 90;
		proxy_buffer_size 4k;
		proxy_buffers 4 32k;
		proxy_busy_buffers_size 64k;
		proxy_temp_file_write_size 64k;
	}
}
```





### 使用HTTPS

需要有域名证书

nginx配置文件

```Nginx
server {
    listen 80;
    # 要修改server，就是域名
    server_name chat.abc.com;
    # 将访问http的强制重定向到https
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    # 要修改server，就是域名
    server_name chat.abc.com;
	# TLS的证书位置【要提前上传到服务器】
    ssl_certificate /root/ssl/chat.abc.com/chat.abc.com.crt;
    # TLS的公钥位置【要提前上传到服务器】
    ssl_certificate_key /root/ssl/chat.abc.com/chat.abc.com.key;

    client_max_body_size 50m;
    client_body_buffer_size 256k;
    client_header_timeout 3m;
    client_body_timeout 3m;
    send_timeout 3m;
    proxy_connect_timeout 300s;
    proxy_read_timeout 300s;
    proxy_send_timeout 300s;
    proxy_buffer_size 64k;
    proxy_buffers 4 32k;
    proxy_busy_buffers_size 64k;
    proxy_temp_file_write_size 64k;
    proxy_ignore_client_abort on;

    location / {
        # 这里只要修改“7860”运行端口
        # 127.0.0.1不要动，http不要修改成https
        proxy_pass http://127.0.0.1:7860;
        proxy_redirect off;
        proxy_set_header Host $host:80;
        proxy_ssl_server_name on;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```



## 参数说明

### openAPIHost

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
