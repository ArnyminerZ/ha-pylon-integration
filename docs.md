# Example Responses

## `help`
### Raw:
```
help\n\r@\r\r\nLocal command:\r\n\rbat      Battery data show - bat [pwr][index]\r\n\rdata     History data load - data [event/history/misc][item]\r\n\rdatalist Show recorded data - datalist [event/history/misc][item/bat][batnun][volt/curr/temp/coul][item]\r\n\rdisp     Display Info at regular intervals - disp [(pwrs pwrNo)/val]/[(bats batNo)/volt/curr/temp]\r\n\rgetpwr   Get power Info - getpwr\r\n\rhelp     Help [cmd]\r\n\rinfo     Device infomation - info\r\n\rlog      Log information show - log\r\n\rlogin    Login Admin mode - login [password]\r\n\rlogout   user mode  - logout\r\n\rpwr      Power data show - pwr [index]\r\n\rshut     Shut down - shut\r\n\rsoh      State of health - soh [addr]\r\n\rstat     Statistic data show - stat\r\n\rtime     Time - time [year] [month] [day] [hour] [minute] [second]\r\n\rtrst     Test Soft Reset - trst\r\n\rupdata   updata system - updata\r\r\n**********************************************************\r\r\nRemote command:\n\rPress [Enter] to be continued,other key to exit\r
```
### Clean:
```
Local command:
bat      Battery data show - bat [pwr][index]
data     History data load - data [event/history/misc][item]
datalist Show recorded data - datalist [event/history/misc][item/bat][batnun][volt/curr/temp/coul][item]
disp     Display Info at regular intervals - disp [(pwrs pwrNo)/val]/[(bats batNo)/volt/curr/temp]
getpwr   Get power Info - getpwr
help     Help [cmd]
info     Device infomation - info
log      Log information show - log
login    Login Admin mode - login [password]
logout   user mode  - logout
pwr      Power data show - pwr [index]
shut     Shut down - shut
soh      State of health - soh [addr]
stat     Statistic data show - stat
time     Time - time [year] [month] [day] [hour] [minute] [second]
trst     Test Soft Reset - trst
updata   updata system - updata
**********************************************************
```

## `bat`
### Raw:
```
bat\n\r@\r\r\nBattery  Volt     Curr     Tempr    Base State   Volt. State  Curr. State  Temp. State  Coulomb     \r\r\n0        3379     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\r\n1        3379     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\r\n2        3379     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\r\n3        3379     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\r\n4        3381     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\r\n5        3378     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\r\n6        3378     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\r\n7        3378     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\r\n8        3380     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\r\n9        3379     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\r\n10       3380     4076     13000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\r\n11       3380     4076     13000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\r\n12       3378     4076     13000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\r\n13       3380     4076     13000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\r\n14       3380     4076     13000    Charge       Normal       Normal       Normal        89%      42586 mAH\r\n\rCommand completed successfully\r\n\r$$\r\n\rpylon>
```
### Clean:
```
Battery  Volt     Curr     Tempr    Base State   Volt. State  Curr. State  Temp. State  Coulomb     
0        3379     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH
1        3379     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH
2        3379     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH
3        3379     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH
4        3381     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH
5        3378     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH
6        3378     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH
7        3378     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH
8        3380     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH
9        3379     4076     14000    Charge       Normal       Normal       Normal        89%      42586 mAH
10       3380     4076     13000    Charge       Normal       Normal       Normal        89%      42586 mAH
11       3380     4076     13000    Charge       Normal       Normal       Normal        89%      42586 mAH
12       3378     4076     13000    Charge       Normal       Normal       Normal        89%      42586 mAH
13       3380     4076     13000    Charge       Normal       Normal       Normal        89%      42586 mAH
14       3380     4076     13000    Charge       Normal       Normal       Normal        89%      42586 mAH
```

## `info`
### Raw:
```
info\n\r@\r\n\rDevice address      : 1\r\n\rManufacturer        : Pylon\r\n\rDevice name         : US2KBPL\r\n\rBoard version       : PHANTOMSAV10R03\r\n\rMain Soft version   : B66.6\r\n\rSoft  version       : V2.4\r\n\rBoot  version       : V2.0\r\n\rComm version        : V2.0\r\n\rRelease Date        : 20-05-28\r\n\rBarcode             : PPTBH02400710243\r\n\r\r\n\rSpecification       : 48V/50AH\r\n\rCell Number         : 15\r\n\rMax Dischg Curr     : -100000mA\r\n\rMax Charge Curr     : 102000mA\r\n\rEPONPort rate       : 1200\r\n\rConsole Port rate   : 115200\r\n\rCommand completed successfully\r\n\r$$\r\n\rpylon>
```
### Clean:
```
Device address      : 1
Manufacturer        : Pylon
Device name         : US2KBPL
Board version       : PHANTOMSAV10R03
Main Soft version   : B66.6
Soft  version       : V2.4
Boot  version       : V2.0
Comm version        : V2.0
Release Date        : 20-05-28
Barcode             : PPTBH02400710243

Specification       : 48V/50AH
Cell Number         : 15
Max Dischg Curr     : -100000mA
Max Charge Curr     : 102000mA
EPONPort rate       : 1200
Console Port rate   : 115200
```

## `pwr`
### Raw:
```
pwr\n\r@\r\r\nPower Volt   Curr   Tempr  Tlow   Thigh  Vlow   Vhigh  Base.St  Volt.St  Curr.St  Temp.St  Coulomb  Time                 B.V.St   B.T.St  \r\r\n1     50691  3806   17000  13000  14000  3378   3381   Charge   Normal   Normal   Normal   89%      2025-12-21 20:53:06  Normal   Normal  \r\r\n2     50673  4087   16000  13000  14000  3377   3380   Charge   Normal   Normal   Normal   89%      2025-12-21 20:53:04  Normal   Normal  \r\r\n3     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       \r\r\n4     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       \r\r\n5     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       \r\r\n6     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       \r\r\n7     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       \r\r\n8     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       \r\n\rCommand completed successfully\r\n\r$$\r\n\rpylon>
```
### Clean:
```
Power Volt   Curr   Tempr  Tlow   Thigh  Vlow   Vhigh  Base.St  Volt.St  Curr.St  Temp.St  Coulomb  Time                 B.V.St   B.T.St  
1     50691  3806   17000  13000  14000  3378   3381   Charge   Normal   Normal   Normal   89%      2025-12-21 20:53:06  Normal   Normal  
2     50673  4087   16000  13000  14000  3377   3380   Charge   Normal   Normal   Normal   89%      2025-12-21 20:53:04  Normal   Normal  
3     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
4     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
5     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
6     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
7     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
8     -      -      -      -      -      -      -      Absent   -        -        -        -        -                    -        -       
```

## `soh`
### Raw:
```
soh\n\r@\r\r\nPower   1\r\r\nBattery    Voltage    SOHCount   SOHStatus \r\r\n0          3378       0          Normal    \r\r\n1          3378       0          Normal    \r\r\n2          3378       0          Normal    \r\r\n3          3377       0          Normal    \r\r\n4          3378       0          Normal    \r\r\n5          3378       0          Normal    \r\r\n6          3377       0          Normal    \r\r\n7          3378       0          Normal    \r\r\n8          3377       0          Normal    \r\r\n9          3378       0          Normal    \r\r\n10         3379       0          Normal    \r\r\n11         3378       0          Normal    \r\r\n12         3378       0          Normal    \r\r\n13         3378       0          Normal    \r\r\n14         3379       0          Normal    \r\n\rCommand completed successfully\r\n\r$$\r\n\rpylon>
```
### Clean:
```
Battery    Voltage    SOHCount   SOHStatus 
0          3378       0          Normal    
1          3378       0          Normal    
2          3378       0          Normal    
3          3377       0          Normal    
4          3378       0          Normal    
5          3378       0          Normal    
6          3377       0          Normal    
7          3378       0          Normal    
8          3377       0          Normal    
9          3378       0          Normal    
10         3379       0          Normal    
11         3378       0          Normal    
12         3378       0          Normal    
13         3378       0          Normal    
14         3379       0          Normal    
```

## `stat`
### Raw:
```
stat\n\r@\r\r\nDevice address           1\r\r\nData Items      :     1689\r\r\nHisData Items   :     1794\r\r\nMiscData Items  :     6230\r\r\nCharge Cnt.     :     4681\r\r\nDischarge Cnt.  :        0\r\r\nCharge Times    :     1150\r\r\nStatus Cnt.     :     4680\r\r\nIdle Times      :    23858\r\r\nCOC Times       :        0\r\r\nDOC Times       :        0\r\r\nCOCA Times      :        0\r\r\nDOCA Times      :        0\r\r\nSC Times        :       12\r\r\nBat OV Times    :       56\r\r\nBat HV Times    :     5832\r\r\nBat LV Times    :        0\r\r\nBat UV Times    :        0\r\r\nBat SLP Times   :        0\r\r\nPwr OV Times    :     4688\r\r\nPwr HV Times    :     6734\r\r\nPwr LV Times    :        0\r\r\nPwr UV Times    :        0\r\r\nPwr SLP Times   :        0\r\r\nCOT Times       :        0\r\r\nCUT Times       :        0\r\r\nDOT Times       :        0\r\r\nDUT Times       :        0\r\r\nCHT Times       :        0\r\r\nCLT Times       :        0\r\r\nDHT Times       :        0\r\r\nDLT Times       :        0\r\r\nShut Times      :      329\r\r\nReset Times     :       67\r\r\nRV Times        :        0\r\r\nInput OV Times  :        0\r\r\nSOH Times       :        0\r\r\nBMICERR Times   :        0\r\r\nCYCLE Times     :      430\r\r\nPwr Percent     :       89\r\r\nPwr Coulomb     : 153311400\r\r\nDsg Cap         : 21506462\r\r\nHT@0.5C Cnt     :        0\r\r\nLT@0.5C Cnt     :        0\r\r\nHT Cnt          :        0\r\r\nLT Cnt          :        0\r\r\nLV Cnt          :       76\r\r\nLifeWarn Times  :        0\r\r\nLifeAlarm Times :        0\r\n\rCommand completed successfully\r\n\r$$\r\n\rpylon>
```
### Clean
```
Device address           1
Data Items      :     1689
HisData Items   :     1794
MiscData Items  :     6230
Charge Cnt.     :     4681
Discharge Cnt.  :        0
Charge Times    :     1150
Status Cnt.     :     4680
Idle Times      :    23858
COC Times       :        0
DOC Times       :        0
COCA Times      :        0
DOCA Times      :        0
SC Times        :       12
Bat OV Times    :       56
Bat HV Times    :     5832
Bat LV Times    :        0
Bat UV Times    :        0
Bat SLP Times   :        0
Pwr OV Times    :     4688
Pwr HV Times    :     6734
Pwr LV Times    :        0
Pwr UV Times    :        0
Pwr SLP Times   :        0
COT Times       :        0
CUT Times       :        0
DOT Times       :        0
DUT Times       :        0
CHT Times       :        0
CLT Times       :        0
DHT Times       :        0
DLT Times       :        0
Shut Times      :      329
Reset Times     :       67
RV Times        :        0
Input OV Times  :        0
SOH Times       :        0
BMICERR Times   :        0
CYCLE Times     :      430
Pwr Percent     :       89
Pwr Coulomb     : 153311400
Dsg Cap         : 21506462
HT@0.5C Cnt     :        0
LT@0.5C Cnt     :        0
HT Cnt          :        0
LT Cnt          :        0
LV Cnt          :       76
LifeWarn Times  :        0
LifeAlarm Times :        0
Command completed successfully
```

## `time`
_Without parameters, returns the current time._
### Raw:
```
\n\rpylon>time\n\r@\r\n\rDs3231 2025-12-21 21:14:53\r\n\rCommand completed successfully\r\n\r$$\r\n\rpylon>
```
### Clean:
```
Ds3231 2025-12-21 21:14:53
```
