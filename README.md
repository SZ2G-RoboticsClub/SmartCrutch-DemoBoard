# SmartCrutch-DemoBoard

SmartCrutch-v4 demoboard Repo


## Hardware required
    - 掌控板
    - 灯带 × 1
    - 按钮 × 1
    - SIM卡模块 × 1
    - 北斗+GPS定位模块 × 1
    - 摄像头+SD卡 × 4


## Functions
主要功能

### Fall-detecting 摔倒检测，远端报警

#### Description
检测老人是否摔倒，若摔倒则向服务端发送报警信息并亮灯蜂鸣，30s还没起来直接拨打紧急联系人电话

#### Sensor
    - 三轴加速度计(内置在掌控板中)
    - 灯带
    - 蜂鸣器(内置在掌控板中)
    - SIM卡模块
    - 北斗+GPS定位模块

#### Method
    - 检测摔倒:
        - z轴加速度值的范围
        - 10s内是否回复正常
        - 剧烈加速度变化（待定）

    - 定位获取：
        - 串口读取北斗+GPS定位模块检测的坐标

    - 远端报警——掌控板urequests post:
        - 位置经纬度
        - status：“emergency”

    - 拨打电话——SIM卡模块：
        - uart1.write('AT+SETVOLTE=1')
        - uart1.write('ATD号码')，**中间无'+'**


### Video recording 拐杖记录仪

#### Description
拐杖记录仪，老人摔倒时开启录像六十秒

#### Sensor
    - 四个摄像头（传感器类型）

#### Method
    - 待定


### Take you home “带你回家”

#### Description
带你回家，当老人按下按钮时，记录当前位置，而后导航带老人回家

#### Sensor
    - 北斗+GPS定位模块

#### Method
    - 初始位置获取：
        - get_settings中的位置上传到百度地图经纬坐标转换
    
    - 当前位置获取：
        - 串口读取北斗+GPS定位模块检测的坐标

    - 导航路径：
        - 起止点坐标上传至百度地图获得路径
    
    - 带你回家：
        - 待定