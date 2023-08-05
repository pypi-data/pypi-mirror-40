# py-ogp-parser

## このライブラリについて

このライブラリはNode.jsで作成した
「[ogp-parser](https://www.npmjs.com/package/ogp-parser)」のPython版です。

## 使い方

requestをimportしてください。

```python
from py_ogp_parser.parser import request
```

## サンプル

```python
from py_ogp_parser.parser import request
import json

status_code, result = request('http://ogp.me')
print(status_code)
print(json.dumps(result, indent=4))

```

## 出力結果サンプル

```python
>>> from py_ogp_parser.parser import request
>>> import json
>>> status_code, result = request('http://ogp.me')
>>> print(status_code)
200
>>> print(json.dumps(result, indent=4))
{
    "title": "The Open Graph protocol",
    "ogp": {
        "og:title": [
            "Open Graph protocol"
        ],
        "og:type": [
            "website"
        ],
        "og:url": [
            "http://ogp.me/"
        ],
        "og:image": [
            "http://ogp.me/logo.png"
        ],
        "og:image:type": [
            "image/png"
        ],
        "og:image:width": [
            "300"
        ],
        "og:image:height": [
            "300"
        ],
        "og:image:alt": [
            "The Open Graph logo"
        ],
        "og:description": [
            "The Open Graph protocol enables any web page to become a rich object in a social graph."
        ],
        "fb:app_id": [
            "115190258555800"
        ]
    },
    "seo": {
        "description": [
            "The Open Graph protocol enables any web page to become a rich object in a social graph."
        ]
    }
}
```
