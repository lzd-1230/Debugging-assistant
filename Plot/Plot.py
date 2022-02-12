import pyqtgraph as pg
import threading
import time
import yaml

class Line_plot(threading.Thread):
    def __init__(self,widget):
        super().__init__()
        self.win = widget
        # 配置文件导入
        self.load_yaml()
        # 绘图部分初始化
        self.graph_init()
        # 线程控制变量
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True

    def graph_init(self):
        self.first_on = False
        self.new_data = False
        self.pic_list = []
        self.data_dict = dict()
        self.cur_x = 0
        self.on_click_regin = False 
        self.color_list = ["#ff7f0e","#2ca02c","#1f77b4"]

        pen_list = [
            pg.mkPen(width=3,color=self.color_list[i]) 
            for i in range(len(self.curve_names))
        ]

        # 样式设置
        self.win.setBackground('#1e1e1e')
        # 添加标签(标签也要占据行数)
        self.label = pg.LabelItem(justify='right')
        self.win.addItem(self.label,row=0,col=0)
        self.layout = self.win.ci.layout # 拿到graphwindow的布局
        self.layout.setRowStretchFactor(1,3)
        self.layout.setRowStretchFactor(2,1)

        # 创建画图区域
        self.p1 = self.win.addPlot(row=1,col=0)    # 返回一个PlotItem对象
        self.p2 = self.win.addPlot(row=2,col=0)
        self.p1.setAutoVisible(y=True)

        # 添加鼠标十字架
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.p1.addItem(self.vLine, ignoreBounds=True)
        self.p1.addItem(self.hLine, ignoreBounds=True)
        self.proxy = pg.SignalProxy(self.p1.scene().sigMouseMoved,rateLimit=60, slot=self.mouseMoved) # 这个一定要设成属性

        # p1区域绘图
        self.p1.addLegend()             # 这个一定要放在plot前面
        self.p1.setAutoVisible(y=True)
        
        # 当绘图的区域改变的时候
        self.p1.sigRangeChanged.connect(self.p2_regin_updata) # 当p1的rgn发生改变时会通知p2
        # 添加曲线
        for i in range(self.curve_num):
            self.pic_list.append(self.p1.plot(name=self.curve_names[i],pen=pen_list[i]))

        # p2区域绘图
        self.region = pg.LinearRegionItem()
        self.region.setZValue(10)
        self.p2.addItem(self.region,ignoreBounds=True)
        self.p2_1 = self.p2.plot(pen=pen_list[0])
        self.region.setClipItem(self.p2_1)
        # 拖动框信号
        self.region.sigRegionChanged.connect(self.p1_regin_update)

    def load_yaml(self):
        with open("./config/config.yaml",mode="rt") as f:
            self.config = yaml.safe_load(f)
        self.curve_names = self.config["graph"]["curve_names"]
        self.curve_num = self.config["graph"]["curve_num"]

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
        # 假如开关并且有新数据
        if self.new_data:
            for idx,key in enumerate(self.data_dict):
                self.pic_list[idx].setData(self.data_dict[key])

                # 用第一条曲线的数据对p2更新
                if idx == 0:
                    self.p2_1.setData(self.data_dict[key])
                    
            # 设置下方拖动框跟随最前线
            if not self.on_click_regin:
                
                if self.cur_x > 100:
                    self.region.setRegion([self.cur_x-100,self.cur_x])
                else:
                    self.region.setRegion([0,self.cur_x])
            self.new_data = False
        else:
            time.sleep(0.02) # !如果没有开启就睡眠,否则会占用大量资源
            

    # 这个函数没有反应
    def mouseMoved(self,evt):
        # 如果在p1的里面
        pos = evt[0]  # using signal proxy turns original arguments into a tuple
        if self.p1.sceneBoundingRect().contains(pos):
            vb = self.p1.vb  # 拿到visualbox对象
            mousePoint = vb.mapSceneToView(pos)  # 坐标映射到图像里的坐标 
            res_text = self.get_stats_text(evt,mousePoint)
            self.label.setText(res_text)


    def get_stats_text(self,evt,mousePoint):
        index = int(mousePoint.x())
        self.vLine.setPos(mousePoint.x())
        self.hLine.setPos(mousePoint.y())
        x_text = f"<span style='font-size: 12pt'>x={mousePoint.x():.2} "
        tmp = ""
        if index > 0:
            for idx,key in enumerate(self.curve_names):
                color = self.color_list[idx]
                data = self.data_dict[key][index]
                tmp += f"<span style='color:{color}'>{key}={data}</span> "
        return x_text+tmp



        
    def run(self):
        while self.__running.isSet():
            self.__flag.wait()
            self.plot()
    def stop(self):
        self.__running.clear()
    def pause(self):
        self.__flag.clear()
    def resume(self):
        self.__flag.set()
        