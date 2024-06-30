import sys
from PyQt5 import QtWidgets
from login_layout import Ui_Form as login_layout
from main_layout import Ui_Form as main_layout

class instagram(login_layout):
	def __init__(self, dialog):
		login_layout.__init__(self)
		self.setupUi(dialog)

		self.pushButtonMasuk.clicked.connect(self.login)
		self.pushButtonBatal.clicked.connect(self.batal)

	def login(self):
		username = self.lineEditUsername.text()
		Password = self.lineEditPassword.text()
		if username == "eri" and Password == "232102020":
			self.mainWindow = QtWidgets.QDialog()
			self.mainUI = main_layout()
			self.mainUI.setupUi(self.mainWindow)

			loginWindow.hide()
			self.mainWindow.show()

		self.mainUI.pushButtonSimpan.clicked.connect(self.tambahData)
		self.mainUI.pushButtonHapus.clicked.connect(self.HapusData)

	def tambahData(self):
		USername_Instagram = self.mainUI.lineEditUsernameInstagram.text()
		Jumlah_Follower = self.mainUI.lineEditJumlahFollower.text()
		Jumlah_Posting = self.mainUI.lineEditJumlahPosting.text()

		rowPosition = self.mainUI.tableWidget.rowCount()		

		self.mainUI.tableWidget.insertRow(rowPosition)
		self.mainUI.tableWidget.setItem(rowPosition, 0, QtWidgets. QTableWidgetItem(USername_Instagram))
		self.mainUI.tableWidget.setItem(rowPosition, 1, QtWidgets. QTableWidgetItem(Jumlah_Follower))
		self.mainUI.tableWidget.setItem(rowPosition, 2, QtWidgets. QTableWidgetItem(Jumlah_Posting))


	def HapusData(self):
		selectedRow = self.mainUI.tableWidget.currentRow()
		nama = self.mainUI.tableWidget.item(selectedRow,0).text()
		self.mainUI.tableWidget.removeRow(selectedRow)

	def batal(self):
		app = QtWidgets.QApplication(sys.argv)
		ex = login_layout()
		sys.exit(app.exec_())


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	loginWindow = QtWidgets.QDialog()
	loginUI = instagram(loginWindow)

	loginWindow.show()
	sys.exit(app.exec_())
