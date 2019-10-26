
import os
import time
import json
import signal
import subprocess
import psutil
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtNetwork import *
from l2_rpc_controller import *

def ping():
	result = ""
	response = os.popen("ping 192.168.2.100 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result = result + "Censor is down;"
	
	response = os.popen("ping 192.168.2.101 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result = result + "Website is down;"
	
	response = os.popen("ping 192.168.2.104 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result = result + "Iperf server is down;"

	response = os.popen("ping 192.168.2.103 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result = result + "Iperf client is down;"

	response = os.popen("ping 192.168.2.105 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result = result + "Streming server is down;"
	
	if result == "":
		result += "All hosts are Up!"
	return "Status: " + result


class Website(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = 'TCP RFC'
		self.left = 0
		self.top = 0		
		self.width = 800
		self.height = 600
		self.initUI()
			
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.html = QWebEngineView(self)
		self.html.move(20, 20)
		self.html.resize(760, 560)
		self.html.load(QUrl('http://tcp.rfc.com'))


class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = '14740 Lab 2'
		self.left = 100
		self.top = 100
		self.width = 680
		self.height = 180
		self.initUI()
		
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.rfc = QPushButton('Open RFC', self)
		self.rfc.move(20, 20)
		self.rfc.clicked.connect(self.rfc_click)

		self.iperf = QPushButton('Run IPERF test', self)
		self.iperf.move(210, 20)
		self.iperf.clicked.connect(self.iperf_click)

		self.start = QPushButton('Start Video Stream', self)
		self.start.move(390, 20)
		self.start.clicked.connect(self.start_video)

		# self.stop = QPushButton('Stop Video', self)
		# self.stop.move(360, 20)
		# self.stop.clicked.connect(self.stop_video)

		self.image = QPushButton('Download Image', self)
		self.image.move(570, 20)
		self.image.clicked.connect(self.image_click)

		self.sld = QSlider(Qt.Horizontal, self)
		self.sld.move(20, 75)
		self.sld.resize(300, 30)
		self.sld.valueChanged.connect(self.loss_change)

		self.input = QLineEdit(self)
		self.input.move(520, 75)
		self.input.resize(40, 30)
		self.input.setReadOnly(True)
		self.input.setText("0%")

		self.comboBox = QComboBox(self)
		self.comboBox.move(330, 75)
		self.comboBox.resize(180, 30)
		self.comboBox.addItem("Packet loss on Stream")
		self.comboBox.addItem("Packet loss on Iperf")

		self.apply = QPushButton('Apply', self)
		self.apply.move(570, 75)
		self.apply.clicked.connect(self.apply_loss)

		self.attack = QPushButton("Start Censor", self)
		self.attack.move(20, 110)
		self.attack.clicked.connect(self.on_attack)

		self.label = QLabel("Status", self)
		self.label.move(25, 145)
		self.label.resize(700, 20)

		self.show()
		
		result = ping()
		print(result)
		self.label.setText(result)


	@pyqtSlot()
	def rfc_click(self):
		self.web = Website()
		self.web.show()

	@pyqtSlot()
	def iperf_click(self):
		Controller().runIperfTest()

	@pyqtSlot()
	def image_click(self):
		subprocess.Popen(['download_image.bat'])

	@pyqtSlot()
	def start_video(self):
		self.proc = subprocess.Popen(['start_video.bat'], creationflags=subprocess.CREATE_NEW_CONSOLE)

	# @pyqtSlot()
	# def stop_video(self):
	# 	os.system('TASKKILL /PID ' + str(self.proc.pid) + ' /F')

	@pyqtSlot()
	def apply_loss(self):
		if "Stream" in self.comboBox.currentText():
			Controller().changeLoss_VID(float(self.input.text()[:-1]))
		else:
			Controller().changeLoss_IPERF(float(self.input.text()[:-1]))

	@pyqtSlot()
	def loss_change(self):
		self.input.setText(str(self.sld.value()*2/10.0) + '%')

	@pyqtSlot()
	def on_attack(self):
		reply = QMessageBox.question(self, 
			"With great power, comes great responsibility", 
			"1. Use this only after all the other questions are complete. Once this is done you have to restart the machines to go back.\n2. Do not use what you learn here for evil :)\nDo you want to continue?", 
			QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			Controller().censor()

app = QApplication([])
ex = App()
print('\n\nStarting Application...')
app.exec_()

