## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://totolink.com.my/products/a3000ru/

## Affected version

A3000RU_Firmware V5.9c.5185

## Vulnerability details

There is a hard code password for telnet in /web_cste/cgi-bin/product.ini

## POC

```c
[PRODUCT]
Csid=C8189R
Model=C8189R
HostName=
webTitle=
Vendor=
CopyRight=
IpAddress=192.168.0.1
DhcpStart=192.168.0.2
DhcpEnd=192.168.0.250
DnsBackup=149.112.112.112
Language=
MultiLang=
SoftVersion=V4.1.2cu
TelnetKey=cs2012
TimeZone=
StatisticsModel=C8189R
StatisticsDomain=esas.carystudio.com,totolinkc.com
DomainAccess=
LoginPassword=admin // leak login password
WanTypeList=dhcp,static,pppoe,l2tp,pptp
WanTypeDefault=1
PppoeSpecSupport=0
Ipv6Support=0
NoticeSupport=1
WechatQrSupport=0
PppoeSpecRussia=0
PingCheck=0
DomainSupport=1
versionControlSupport=0

[WLAN]
Ssid_2G=wifi
Ssid_5G=wifi_5G
FixedMac=0
WlanKey_2G=
WlanKey_5G=
Channel_2G=0
Channel_5G=0
MaxSta=32
CountryCodeSupport=1
CountryCodeList=CN,US,EU,OT
CountryCode_2G=CN
CountryCode_5G=CN

[IPTV]
IptvSupport=1
IptvEnable=0
IptvModeList=0
IptvModeDefault=0
```

