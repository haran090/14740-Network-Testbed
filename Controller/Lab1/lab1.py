
import os
import requests
import time
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtNetwork import *
from l1_rpc_controller import *

def ping():
	result = ""
	response = os.popen("ping 192.168.1.100 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result = result + "Spoofer is down;"

	response = os.popen("ping 192.168.1.101 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result += "DNS Resolver is Down;"

	response = os.popen("ping 192.168.1.102 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result += "Http Server 1 is Down;"


	response = os.popen("ping 192.168.1.103 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result += "Http Server 2 is Down;"


	response = os.popen("ping 192.168.1.104 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result += "Proxy is Down;"

	response = os.popen("ping 192.168.1.105 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result += "Root NS is Down;"
	
	response = os.popen("ping 192.168.1.106 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result += "TLD COM is Down;"
	
	response = os.popen("ping 192.168.1.107 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result += "TLD EDU is Down;"
	 
	response = os.popen("ping 192.168.1.108 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result += "NS 1 is Down;"
	 
	response = os.popen("ping 192.168.1.109 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result += "NS 2 is Down;"
	 
	response = os.popen("ping 192.168.1.110 -n 1").read()
	if "100% loss" in response or "unreachable" in response:
		result += "NS 3 is Down;"
	
	
	if result == "":
		result += "All hosts are Up!"
	return "Status: " + result

def doRequest(message):
	try:
		proxy = ""
		header = ""
		if message['use_range'] != '':
			header = {"Range":message['use_range']}
		if message['use_proxy']:
			proxy = {'http' : 'http://192.168.0.104:3128'}
		if message['method'] == 'POST':
			param = message['post_param'].split('=')
			data = ''
			try:
				data = {param[0]:param[1]}
			except:
				print('Parameter error')
			res = requests.post(url=message['url'], proxies=proxy, data=data)
		else:
			res = requests.get(url=message['url'], proxies=proxy, headers=header, timeout=10)
		print('Remote Callback compelte')
		print(res)
		return {'body':res.text, 'url':res.url}
	except requests.exceptions.RequestException as err:
		print(err)
		if 'Name or service not known' in str(err):
			return {'body':'Could not resolve the domain ' + message['url'], 'url':''}
		else:
			return {'body':str(err), 'url':''}
	except:
		print("Unkown Error")
		return {'body':'Connection failed', 'url':''}



class App(QWidget):
	def __init__(self):
		super().__init__()
		self.title = '14740 Lab 1'
		self.left = 100
		self.top = 100
		self.width = 840
		self.height = 480
		self.initUI()
		
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.comboBox = QComboBox(self)
		self.comboBox.addItem("GET")
		self.comboBox.addItem("POST")
		self.comboBox.move(20,20)

		self.input = QLineEdit(self)
		self.input.setText("http://")
		self.input.move(75, 20)
		self.input.resize(665, 20)

		self.post_lb = QLabel("POST Parameter [Optional]", self)
		self.post_lb.move(20, 45)
		self.post_lb.resize(130, 20)

		self.post = QLineEdit(self)
		self.post.move(155, 45)
		self.post.resize(150, 20)
		self.post.setPlaceholderText('Key = Value')

		self.range_lb = QLabel("GET Range [Optional]", self)
		self.range_lb.move(330, 45)
		self.range_lb.resize(120, 20)

		self.range = QLineEdit(self)
		self.range.move(440, 45)
		self.range.resize(100, 20)
		self.range.setPlaceholderText('0-100')

		self.button = QPushButton('Go!', self)
		self.button.move(745, 19)
		self.button.clicked.connect(self.on_click_doget)

		self.checkb = QCheckBox("Use Proxy", self);
		self.checkb.move(746, 45)

		self.html = QWebEngineView(self)
		self.html.page().profile().setHttpCacheMaximumSize(0)
		self.html.move(20,70)
		self.html.resize(800, 380)
		self.html.load(QUrl(''))
		self.html.setHtml("*Responses will show up here")

		self.attack = QPushButton("Start DNS Spoofer", self)
		self.attack.move(726, 452)
		self.attack.clicked.connect(self.on_attack)

		settings = QWebEngineSettings.globalSettings()
		for attr in (QWebEngineSettings.PluginsEnabled, 
					 QWebEngineSettings.ScreenCaptureEnabled,):
			settings.setAttribute(attr, True)

		self.label = QLabel("Status", self)
		self.label.move(20, 455)
		self.label.resize(700, 20)

		self.show()
		
		result = ping()
		print(result)
		self.label.setText(result)

	@pyqtSlot()
	def on_click_doget(self):
		input = self.input.text()
		if len(input) < 1:
			QMessageBox.question(self, "Oops", "Can't GET an empty URL. Try again.", QMessageBox.Ok, QMessageBox.Ok)
			return
		range = self.range.text().strip()
		if len(range) != 0:
			range = 'bytes=' + range;
		if self.checkb.isChecked():
			QNetworkProxy.setApplicationProxy(proxy)
		else:
			QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.DefaultProxy))
		req = QWebEngineHttpRequest(QUrl(input))
		req.setMethod(self.comboBox.currentIndex())
		if range != '':
			req.setHeader(b'Range', bytes(range,'utf-8'))

		if self.post.text() != '':
			try:
				param = self.post.text().split('=')
				data = ''
				req.setHeader(b'Content-Type', b'application/x-www-form-urlencoded')
				req.setPostData(bytes(self.post.text(), 'utf-8'))
			except Exception as e:
				print(e)
		self.html.load(req)
		self.html.page().profile().clearHttpCache()


	@pyqtSlot()
	def on_attack(self):
		reply = QMessageBox.question(self, 
			"With great power, comes great responsibility", 
			"1. Use this only after all the other questions are complete. Once this is done you have to restart the machines to go back.\n2. Do not use what you learn here for evil :)\nDo you want to continue?", 
			QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			Controller().sendDNSSpoof()

os.system("ipconfig /flushdns")
app = QApplication([])
proxy = QNetworkProxy()
proxy.setType(QNetworkProxy.HttpProxy)
proxy.setHostName('192.168.1.104')
proxy.setPort(3128)
ex = App()
print('\n\nStarting Application...')
app.exec_()

