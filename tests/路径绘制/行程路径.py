import matplotlib.pyplot as plt

#各个点的经纬度及编号
loc_collect = [[120.7015202,36.37423,0],
[120.7056165,36.37248342,4],
[120.70691,36.37579616,3],
[120.7031731,36.37753964,5],
[120.7011609,36.37905063,10],
[120.6973521,36.37876006,8],
[120.6928965,36.37800457,6],
[120.6943337,36.37521499,7],
[120.6962022,36.37643544,9],     
[120.6987175,36.37457569,1],
[120.6997954,36.37591239,2],
[120.7015202,36.37423,0]]


def drawPic(dots):
    plt.figure(figsize=(10,6))
    plt.xlim(120.692,120.708,0.002)     #x轴的刻度范围
    plt.ylim(36.372,36.380,0.001)       #y轴的刻度范围
    plt.xlabel('经度',fontproperties="simhei")    #x轴的标题
    plt.ylabel('纬度',fontproperties="simhei")    #y轴的标题
	#绘制各个点及点所代表地点名称
    for i in range(len(dots)-1):
        plt.text(l[i][0],l[i][1],'点'+str(l[i][2]),color='#0085c3',fontproperties="simhei")
        plt.plot(l[i][0],l[i][1],'o',color='#0085c3')
    #连接各个点
    for i in range(len(dots)-1):
        start = (l[i][0],l[i+1][0])
        end = (l[i][1],l[i+1][1])
        plt.plot(start,end,color='#0085c3')
    plt.show()

drawPic(loc_collect)
