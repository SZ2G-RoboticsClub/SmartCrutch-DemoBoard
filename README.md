# SmartCrutch-DemoBoard

SmartCrutch-v4 demoboard Repo


## Hardware required
- 掌控宝 × 1(ESP32模组)
- 灯带（63颗） × 2
- 按钮 × 2（AB按键）
- SIM卡模块 × 1
- 北斗+GPS定位模块 × 1
- 行车记录仪摄像头 × 2
- TF卡模块（存储记录仪视频）
- 光敏电阻 × 1
- 无线充电互感线圈一套
- 锂电池
- 稳压器
- 喇叭（接掌控宝扩展板喇叭引脚）



## Functions
主要功能

### Fall-detecting 摔倒检测，远端报警

#### Description
检测老人是否摔倒，若摔倒则向服务端发送报警信息(准备增加发送短信)并亮灯蜂鸣，30s还没起来直接拨打紧急联系人电话

#### Sensor and Actuators
- 三轴加速度计(内置在掌控板中)
- 灯带
- 光敏电阻
- 按钮
- 蜂鸣器(内置在掌控板中)
- SIM卡模块
- 北斗+GPS定位模块

#### Method
- 正常情况
    - 按一下灯带彩虹灯，若光线暗亮白灯（手电筒）；按第二下白灯；按第三下关掉
    - status: "ok"
    - Loc: 实时获取经纬度

- 检测摔倒:
    - 竖直方向加速度值的范围√
    - 10s内是否回复正常
    - 剧烈加速度变化（待定）

- 定位获取：
    - 串口读取北斗+GPS定位模块检测的坐标

- 远端报警——掌控板urequests post:
    - 当前位置经纬度
    - status：“emergency”

- 拨打电话——SIM卡模块：
    - uart1.write('AT+SETVOLTE=1')
    - uart1.write('ATD号码')，**中间无'+'号**

- 发送短信——SIM卡模块：
    - （暂时未知）


### Video recording 拐杖记录仪

#### Description
拐杖记录仪，全天拍摄

#### Sensor
- 行车记录仪摄像头 × 2

#### Method
- 独立于掌控板，全天摄像，存入内存卡或者本地app，可通过摔倒时发送的摔倒时间来查看录像


### Take you home “带你回家”

#### Description
带你回家，当老人按下按钮时，导航带老人回家

#### Sensor
- 北斗+GPS定位模块

#### Method
- 初始位置获取：
    - settings中的地点描述上传到高德地图经纬坐标转换——提高导航准确度

- 当前位置获取:
    - 串口读取北斗+GPS定位模块检测的坐标

- 导航路径：
    - 起止点坐标上传至高德地图获得路径

- 带你回家：
    - 掌控板屏幕显示
    - 语音（目前）
    - ……


## Module request:
与服务器交互

### Heartbeat sending发送心跳包

#### Description
拐杖心跳包，每隔**5秒**发送一次

#### Data——post上传
- 正常情况
    - status: "ok"
    - loc: 
        - latitude: 实时获取纬度
        - longitude: 实时获取经度

- 摔倒
    - status: "emergency"
    - loc:
        - latitude: 摔倒纬度
        - longitude: 摔倒经度
    
    - 可做历史记录【falltime:
        - date: 摔倒日期(年月日)
        - time: 摔倒时间(时分秒)】

- 其他错误
    - status: "error"
    - loc: None


### Get settings获取设置

#### Description
获取拐杖设置信息
在拐杖启动时请求，若uuid(拐杖身份证号)不存在则自动注册

#### Data——get获取
- settings设置信息
    - phone: *可选项*，紧急联系人电话号码
    - password: *可选项*，App登录密码
    - home: *可选项*，老人家庭住址
