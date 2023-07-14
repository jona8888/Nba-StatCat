import sys
import pandas as pd
from PyQt6.QtWidgets import(
    QApplication,QWidget,QPushButton, 
    QLabel, QGridLayout, QLineEdit,
    QTableWidget, 
    )

from PyQt6.QtGui import QPixmap, QIcon
from nba_api.stats.static import players
player_dict = players.get_players()
from nba_api.stats.endpoints import playercareerstats

from pandas import ExcelWriter
from openpyxl import load_workbook


pd.set_option('max_columns', None)

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.resize(1000,550)
        #self.setWindowIcon(QIcon('catHead.jpeg'))
        self.setWindowTitle("StatCat")
        self.setContentsMargins(50,500,500,10)
        
        self.table = QTableWidget
        
        label2 = QLabel(self)
        pixmap = QPixmap('top75.jpg')
        label2.setPixmap(pixmap)
        label2.resize(pixmap.width(), pixmap.height())
        
        layout = QGridLayout()
        self.setLayout(layout)
        
        self.label1 = QLabel("Enter Player Name: ")
        layout.addWidget(self.label1,0,0)
        
        self.input1 = QLineEdit('Enter Player Name', self)
        layout.addWidget(self.input1, 0, 0,)
        
        button = QPushButton("Find")
        button.setFixedWidth(50)
        button.clicked.connect(self.display)
        button.clicked.connect(self.login)
        layout.addWidget(button,0,2)
        
    def display(self):
        print(self.input1.text())
    
        
    def login(self):
        
        try:
            x = self.input1.text()
        
            player = [player for player in player_dict if player['full_name'] == x][0]
        
            name_Id = player['id']
            career = playercareerstats.PlayerCareerStats(name_Id) 
            career = career.get_data_frames()
            print(career)
            
            '''Below are instructions to display stats in excel
            -We have created an empty excel sheet in project folder
            -called 'player.xlsx'
            -run program, and open the excel file
            -close excel sheet before running again'''
            
            book = load_workbook('player.xlsx')
            writer = pd.ExcelWriter('player.xlsx', engine='openpyxl')
            
            writer.book = book
            writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
            
            writer = ExcelWriter('player.xlsx')
            career[0].to_excel(writer,x)
            writer.save()
                 
        except IndexError:
                print("Player does not exist OR Player Name spelt wrong")
    
    
               
app = QApplication(sys.argv)
app.setWindowIcon(QIcon('Basketball.jpg'))
window = Window()
window.show()
sys.exit(app.exec())
