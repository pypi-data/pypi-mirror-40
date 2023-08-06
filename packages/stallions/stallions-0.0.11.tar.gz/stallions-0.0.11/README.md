# Stallion
Parsing any web page context.

## Use
```
from stallions import extract
url = "https://www.rtbasia.com/"
article = extract(url=url)
print("title", article.title)
print("h1", article.h1)
print("meta_keywords", article.meta_keywords)
print("meta_description", article.meta_description)
print(article.content)
```

## Version
- v-0.0.1 Static web page download.
- v-0.0.11 增加页面文章和主要内容提取功能


Galen _@20180510_