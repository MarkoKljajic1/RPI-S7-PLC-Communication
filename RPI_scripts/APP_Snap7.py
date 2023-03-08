from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QDialog, QWidget, QStackedWidget
from PyQt5 import uic 
from PyQt5 import QtWidgets
from PyQt5.QtGui import QMovie
import sys
import QrScan
import time
import snap7
import threading



class Snap7():
    IP = "192.168.137.100"
    RACK = 0
    SLOT = 1
        
    DB_NUMBER = 1
    
    
    data = bytearray(b'\x00')
     
        
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)
        #print(plc.get_cpu_info())
    plc.db_write(1, 0, data)   
        #db = plc.db_read(DB_NUMBER. 0, 1)
        
    def ReadDB():
        
        db = Snap7.plc.db_read(1, 0, 1)
        #value = int.from_bytes(db[0:1], byteorder = "big")
        print (db)
        #print (value)
        #data = bytearray(b'\x00')
        #Snap7.plc.db_write(1, 0, data)
        #value = int.from_bytes(db[0:1], byteorder = "big")
        #print (db)
        
    
    

class Data():
    a = 0
    b = 0
    data = ""
    prev = 0 
    
    
    
    


class MainUi(QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        uic.loadUi('app.ui', self)
        
        self.movie = QMovie("box.gif")
        self.label.setMovie(self.movie)
        self.movie.start()
        
        self.label_5.setText(str(Data.a))
        self.label_6.setText(str(Data.b))
        
        self.pushButton.clicked.connect(self.Start)
        
        self.pushButton_2.clicked.connect(self.Stop)
        
                             
        #self.showMaximized()
        
        #QrScan.Scanner.scan()
        
    def Start(self):
        #Snap7.ReadDB()
        #ScanData()
        data2 = bytearray(b'\x01')
        Snap7.plc.db_write(1, 0, data2)
        time.sleep(0.5)
        data2 = bytearray(b'\x00')
        Snap7.plc.db_write(1, 0, data2)
        
        
    
    def Stop(self):
        data1 = bytearray(b'\x02')
        Snap7.plc.db_write(1, 0, data1)
        time.sleep(0.5)
        data1 = bytearray(b'\x00')
        Snap7.plc.db_write(1, 0, data1)
    

def ScanData():
        db = Snap7.plc.db_read(1, 1, 1)
        value = int.from_bytes(db[0:1], byteorder = "big")
        if value == 0:
            Data.prev = 0
        print(value)
        if value == 1 and Data.prev ==0:
            window.Stop()
            Data.prev = 1
            Data.data = QrScan.Scanner.scan()
            print(Data.data)
            if Data.data == "A":
                Data.a = Data.a + 1
                data2 = bytearray(b'\x05')
                Snap7.plc.db_write(1, 0, data2)
                time.sleep(0.5)
                data1 = bytearray(b'\x00')
                Snap7.plc.db_write(1, 0, data1)
                #print(Data.a)
            if Data.data == 'B':
                Data.b +=1
                window.Start()
            window.label_5.setText(str(Data.a))
            window.label_6.setText(str(Data.b))
        
        threading.Timer(0.1, ScanData).start()
        
app = QtWidgets.QApplication(sys.argv)
window = MainUi()
window.show()
QrScan.Scanner.scan()
Snap7()

threading.Timer(0.1, ScanData).start()

#t1 = Thread(target = ScanData)
#t1.start()
#t1.join()


app.exec_()