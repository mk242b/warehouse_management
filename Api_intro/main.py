import typing
from PyQt5.QtWidgets import QPlainTextEdit,QVBoxLayout,QWidgetItem,QLabel,QLineEdit,QSpinBox,QLayout,QApplication,QMainWindow,QPushButton, QWidget,QListWidget,QListWidgetItem
from PyQt5 import QtCore, uic
import requests
import sys
import random






class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        
        self.setFixedWidth(400)
        self.setFixedHeight(480)

        uic.loadUi("mainUI.ui",self)
        self.show()
 
        #login sector
        # self.l_btn : QPushButton = self.findChild(QPushButton,"l_btn")
        # self.Login_sector : QWidget = self.findChild(QWidget,"login_sec")
        # self.phone : QLineEdit = self.findChild(QLineEdit,"phone")
        # self.password : QLineEdit = self.findChild(QLineEdit,"pass")
        # self.password.setEchoMode(QLineEdit.Password)
        # self.r_btn : QPushButton = self.findChild(QPushButton,"reg")
       #import
        self.import_sector : QWidget = self.findChild(QWidget,"import_main")
        self.export_sector : QWidget = self.findChild(QWidget,"export_main")
        self.i_name : QLineEdit = self.findChild(QLineEdit,"name")
        self.i_price : QLineEdit = self.findChild(QLineEdit,"price")
        self.i_model : QLineEdit = self.findChild(QLineEdit,"model")
        self.i_disc : QLineEdit = self.findChild(QLineEdit,"discription")
        self.import_btn : QPushButton = self.findChild(QPushButton,"importBtn")
        self.toExport_btn : QPushButton = self.findChild(QPushButton,"toExport")
        self.toImport_btn : QPushButton = self.findChild(QPushButton,"back")
        self.list : QListWidget= self.findChild(QListWidget,"listWidget")
        self.result : QLabel = self.findChild(QLabel,"result_text")
        ##Edit Box
        self.editBox : QWidget = self.findChild(QWidget,"edit_box")
        self.uitem_label : QLabel = self.findChild(QLabel,"uitem_label")
        self.uResult_label : QLabel = self.findChild(QLabel,"uResult")
        self.uname : QLineEdit = self.findChild(QLineEdit,"uname")
        self.uprice : QLineEdit = self.findChild(QLineEdit,"uprice")
        self.umodel : QLineEdit = self.findChild(QLineEdit,"umodel")
        self.udisc : QLineEdit = self.findChild(QLineEdit,"udisc")
        self.update_btn : QPushButton = self.findChild(QPushButton,"update")
        self.delete_btn : QPushButton = self.findChild(QPushButton,"delete_btn")
        self.close_btn : QPushButton = self.findChild(QPushButton,"close_box")
        self.reload_btn : QPushButton = self.findChild(QPushButton,"reload")
        self.searchBox : QLineEdit = self.findChild(QLineEdit,"searchbox")
        self.find_Btn : QPushButton = self.findChild(QPushButton,"find")
        #functions
        self.editBox.hide()
    def hideImport(self):
        self.import_sector.hide()
        self.export_sector.show()
        self.FetchData()

    def hideExport(self):
        self.export_sector.hide()
        self.import_sector.show()
        self.list.clear()
        self.result.clear()
        self.closeEidt_box()
    def importData(self):
        id = random.randint(100,999)
        name = self.i_name.text()
        price = int(self.i_price.text())
        model = self.i_model.text()
        disc = self.i_disc.text()
        
        data = {"name" : name , "price" : price ,"model" : model , "discription" : disc}
        
        response = requests.put("http://127.0.0.1:8000/put/{}".format(id),json=data)
        if response.status_code == 200:
            self.i_name.clear(),self.i_price.clear(),self.i_model.clear(),self.i_disc.clear()
            
            self.result.setText("Import Successful")
        else:
            self.result.setText("Import Failed")
    def closeEidt_box(self):
        self.uResult_label.clear()
        self.editBox.hide()
        self.export_sector.setEnabled(True)
        self.uname.clear()
        self.uprice.clear()
        self.umodel.clear()
        self.udisc.clear()
    def updateData(self,id):
        
        data = {"name" : self.uname.text() , "price" : self.uprice.text() ,"model" : self.umodel.text() , "discription" : self.udisc.text()}
        response = requests.put("http://127.0.0.1:8000/update/{}".format(id),json=data)
        if response.status_code == 200:
            self.uResult_label.setText("Update Successful")
            self.clearUpdateField()
            self.Reload()
        else:
            self.uResult_label.setText("Update Failed")
            self.clearUpdateField()
    def clearUpdateField(self):
        self.uname.clear()
        self.uprice.clear()
        self.umodel.clear()
        self.udisc.clear()
    def Find(self):
        
        response = requests.get("http://127.0.0.1:8000/find/{}".format(self.searchBox.text()))
        
        if response.status_code == 200:
            #print(response.json())
            
            responseData = response.json()
            
            self.list.clear()
            if responseData != None: 
                for i in responseData:
                    if i != None:
                        infoData = "\nid: {} ‎ \n name: {} ‎  \n price: {} ‎ \n model: {}‎ \n description: {}\n".format(
                        i,
                        responseData[i]['name'],
                        str(responseData[i]['price']),
                        responseData[i]['model'],
                        responseData[i]['discription']
                        )

                        item = QListWidgetItem(infoData)
                        self.list.addItem(item)
                    
    def itemClick_handler(self,item : QListWidgetItem):
    
        self.export_sector.setEnabled(False)
        self.editBox.show()
        dataFromitem = item.text().split("‎")
        self.cleanedData = []
        print(dataFromitem)
        for item in dataFromitem:
            splitted = item.split(": ")
            self.cleanedData.append(splitted[1].strip())
            
        print(self.cleanedData)
        self.uitem_label.setText("Item : {}".format(self.cleanedData[0]))
        # print(item.text())
    def Reload(self):
        self.list.clear()
        self.FetchData()
    
    
    def FetchData(self):
        response = requests.get("http://127.0.0.1:8000/get_item/{item_name}")
        if response.status_code == 200:
            #print(response.json())
            
            responseData = response.json()
            
            for i in responseData:
                infoData = "\nid: {} ‎ \n name: {} ‎  \n price: {} ‎ \n model: {}‎ \n description: {}\n".format(
                i,
                responseData[i]['name'],
                str(responseData[i]['price']),
                responseData[i]['model'],
                responseData[i]['discription']
            )

                item = QListWidgetItem(infoData)
                self.list.addItem(item)
    def Delete(self,id):
        response = requests.put("http://127.0.0.1:8000/delete/{}".format(id))
        if response.status_code == 200:
            self.clearUpdateField()
            
            self.closeEidt_box()
        else:
            self.clearUpdateField()
            self.uResult_label.setText("Deletion Failed")      
            
        self.Reload()    
  
app= QApplication(sys.argv)
window = UI()

window.setWindowTitle("WH Manager by Khun")
#login
# window.l_btn.clicked.connect(lambda: window.login())
# window.r_btn.clicked.connect(lambda: window.reg_sector.show())
window.toExport_btn.clicked.connect(lambda : window.hideImport())
window.toImport_btn.clicked.connect(lambda : window.hideExport())
window.import_btn.clicked.connect(lambda : window.importData())
window.list.itemClicked.connect(lambda : window.itemClick_handler(window.list.currentItem()))
window.close_btn.clicked.connect(lambda : window.closeEidt_box())
window.update_btn.clicked.connect(lambda : window.updateData(window.cleanedData[0]))
window.reload_btn.clicked.connect(lambda : window.Reload())
window.delete_btn.clicked.connect(lambda : window.Delete(window.cleanedData[0]))
window.find_Btn.clicked.connect(lambda : window.Find())
sys.exit(app.exec())
#history



#fix toggles