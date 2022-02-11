import pyqtgraph as pg

class Line_plot():
    def __init__(self,widget):
        self.win = widget
        self.legend = pg.LegendItem((40,30))
        self.legend.setParentItem(self.win.graphicsItem())
        self.win.showGrid(x=True, y=True, alpha=0.5) 
        self.p2 = self.win.plot(pen='g',name="s1") # 返回的是PlotDataItem对象
        self.p1 = self.win.plot(pen='w',name="s1")
        self.p3 = self.win.plot(pen='y',name="s1")

        self.legend.addItem(self.p1,'p1')
        self.legend.addItem(self.p2,'p2')
        self.legend.addItem(self.p3,'p3')
        self.on = False

    # 初始化曲线数目
    def plot(self,data_dict:dict):
        if self.on:
            self.p1.setData(data_dict["series1"])
            self.p2.setData(data_dict["series2"])
            self.p3.setData(data_dict["series3"])


            