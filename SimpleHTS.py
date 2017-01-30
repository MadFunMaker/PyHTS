import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

        self.setWindowTitle("Python Home Trading System by bsjeon")
        self.setGeometry(300, 300, 300, 150)

        btn1 = QPushButton("Show", self)
        btn1.move(190, 10)
        btn1.clicked.connect(self.btn1_clicked)

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(10, 10, 170, 130)

    def btn1_clicked(self):
        # SetInputValue
        code = "000030"
        startDate = "20160101"
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "시작일자", startDate)

        # CommRqData
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10015_req", "opt10015", 0, "0101")

    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == "opt10015_req":
            name = self.kiwoom.dynamicCall("CommGetDataEx(QString, QString, QString, int, QString)", trcode, "", rqname,
                                           0, "일자")
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname,
                                             0, "종가")
            print(name)
            dateClosingPriceList = []
            dateClosingPriceList.append(name.strip())
            dateClosingPriceList.append(volume.strip())
            self.listWidget.addItems(dateClosingPriceList)
        # ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"])
        # kospi_code_list = ret.split(';')
        # kospi_code_name_list = []
        #
        # for x in kospi_code_list:
        #     name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", [x])
        #     kospi_code_name_list.append(x + " : " + name)
        #
        # self.listWidget.addItems(kospi_code_name_list)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())