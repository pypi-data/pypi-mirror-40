# Flask-QiniuStoraging

## 介绍
七牛云对象储存 Flask 扩展，便于执行文件的上传、修改、删除操作。

## 安装

```shell
pip install Flask-QiniuStoraging
```

## 配置

| 配置项 | 说明 | 必须 / 默认值 |
| --- | --- | --- |
| QINIU_ACCESS_KEY | 七牛的 ACCESS_KEY | 必须 |
| QINIU_SECRET_KEY | 七牛的 SECRET_KEY | 必须 |
| QINIU_BUCKET_NAME | 七牛的 Bucket 名称 | 必须 |
| QINIU_BUCKET_DOMAIN | 七牛 Bucket 绑定的域名 | 空字符串 '' |
| QINIU_TOKEN_EXPIRES | upload token 过期时间 | 3600 |
| QINIU_GLOBAL_PREFIX | 全局的上传文件名前缀 | 空字符串 '' |

## 使用示例

### 初始化

```python
from flask import Flask
from flask_qiniustoraging import Qiniu

app = Flask(__name__)
qiniu = Qiniu(app)
```

### 一般操作

```python
from flask_qiniustoraging import (
    upload_file， upload_data， fetch_url， rename_file， delete_file
)

# 上传本地文件
filename = 'foo.png'
file_path = 'path/to/foo.png'
qiniu.upload_file(filename, file_path)

# 上传二进制流
filename = 'bar.txt'
data = b'Hello World.'
qiniu.upload_data(filename, data)

# 从 URL 获取文件并上传
filename = 'foz.jpg'
url = 'https://www.image.com/foz.jpg'
qiniu.fetch_url(filename, url)

# 重命名文件
filename = 'foo.png'
filename_to = 'fom.png'
qiniu.rename_file(filename, filename_to)

# 删除文件
filename = 'bar.txt'
qiniu.delete_file(filename)
```

### 添加前缀

Flask-QiniuOS 可以方便的为上传的文件添加前缀。

1. 添加全局前缀

    ```python
    app.config['QINIU_BLOGAL_PREFIX'] = 'my_app/'
    ...

    qiniu.upload_file('baz.png', 'path/to/baz.png')  # 上传后的文件名为 my_app/baz.png
    qiniu.rename_file('baz.png', 'bax.png')  # 将 my_app/baz.png 重命名为 my_app/bax.png
    ```

2. 添加即时前缀

    ```python
    from flask_qiniustoraging import prefix

    files = ['fok1.png', 'fol2.png']
    
    with prefix('images/'):
        for file in files:
          qiniu.upload_file(file, f'path/to/{file}')  # 上传后的文件名为 images/fok1.png, images/fok2.png
    ```

