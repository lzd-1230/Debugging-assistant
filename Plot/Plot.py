import pyqtgraph as pg
import threading
import time

class Line_plot():
    def __init__(self,widget):
        self.win = widget
        self.new_data = False
        self.pic_list = []
        self.data_dict = dict()
        self.cur_x = 0
        self.on_click_regin = False 
        name_list = ["l1","l2","l3"]
        pen_list = [
            pg.mkPen(widget=4,color="y"),
            pg.mkPen(widget=4,color="k"),
            pg.mkPen(widget=4,color="g"),
            pg.mkPen(widget=2,color="r"),
            pg.mkPen(widget=2,color="b"),
            pg.mkPen(widget=2,color="c"),
            pg.mkPen(widget=2,color="m"),
            pg.mkPen(widget=2,color="w"),
        ]

        # 样式设置
        # self.win.setBackground('#f0f0f0')
        # 创建画图区域
        self.p1 = self.win.addPlot(row=1,col=0)    # 返回一个PlotItem对象
        self.p2 = self.win.addPlot(row=2,col=0)
        self.p1.setAutoVisible(y=True)

        # 添加标签
        self.label = pg.LabelItem(justify='right')
        self.win.addItem(self.label)

        # 添加鼠标十字架
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.p1.addItem(self.vLine, ignoreBounds=True)
        self.p1.addItem(self.hLine, ignoreBounds=True)
        proxy = pg.SignalProxy(self.p1.scene().sigMouseMoved,rateLimit=60, slot=self.mouseMoved)

        # p1区域绘图
        self.p1.addLegend()             # 这个一定要放在plot前面
        self.p1.setAutoVisible(y=True)
        self.p1.sigRangeChanged.connect(self.p2_regin_updata) # 当p1的rgn发生改变时会通知p2
        for i in range(3):
            self.pic_list.append(self.p1.plot(name=name_list[i],pen=pen_list[i]))

        # p2区域绘图
        self.region = pg.LinearRegionItem()
        self.region.setZValue(10)
        self.p2.addItem(self.region,ignoreBounds=True)
        self.p2_1 = self.p2.plot(pen="w")
        self.region.setClipItem(self.p2_1)
        # 拖动下方选框
        self.region.sigRegionChanged.connect(self.p1_regin_update)
        self.on = False

    # 更新p1的range的槽函数
    def p1_regin_update(self):
        self.on_click_regin = True
        self.region.setZValue(10)
        minX, maxX = self.region.getRegion()
        for pic in self.pic_list:
            self.p1.setXRange(minX, maxX, padding=0)
        self.on_click_regin = False

    def p2_regin_updata(self,window,viewRange):
        self.region.setRegion(viewRange[0])

    # 初始化曲线数目
    def plot(self):
        while True:
            # 假如开关并且有新数据
            if self.new_data and self.on:
                for idx,key in enumerate(self.data_dict):
                    self.pic_list[idx].setData(self.data_dict[key])
                    # self.pic_list[idx].setPos(self.cur_x,0)
                    if idx == 0:
                        self.p2_1.setData(self.data_dict[key])
                if not self.on_click_regin:
                    if self.cur_x > 100:
                        self.region.setRegion([self.cur_x-100,self.cur_x])
                    else:
                        self.region.setRegion([0,100])
                self.cur_x += 1
                self.new_data = False
            else:
                print("绘图开关已关闭")
                time.sleep(0.02) # 如果没有开启就睡眠

    def mouseMoved(self,evt):
        print("mouse")
        vb = self.p1.vb  # 拿到visualbox对象
        key_list = self.data_dict.keys()
        data1 = self.data_dict[key_list[0]]
        data2 = self.data_dict[key_list[1]]
        data3 = self.data_dict[key_list[2]]
        
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.p1.sceneBoundingRect().contains(pos):
            mousePoint = vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            if index > 0 and index < len(self.data_dict[self.data_dict.keys()[0]]):
                self.label.setText("""<span style='font-size: 12pt'>x=%0.1f,
                                    <span style='color: red'>y1=%0.1f</span>,
                                    <span style='color: green'>y2=%0.1f</span>
                                    <span style='color: blue'>y3=%0.1f</span>
                                    """ \
                                    % (mousePoint.x(), data1[index], data2[index], data3[index]))
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())

    # 开启画图线程
    def start_pic_thread(self):
        self.plot_thread = threading.Thread(target=self.plot)
        self.plot_thread.start() 
