# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(400, 253)
        self.quit_button = QPushButton(Login)
        self.quit_button.setObjectName(u"quit_button")
        self.quit_button.setGeometry(QRect(200, 180, 153, 31))
        self.login_button = QPushButton(Login)
        self.login_button.setObjectName(u"login_button")
        self.login_button.setGeometry(QRect(40, 180, 153, 31))
        self.layoutWidget = QWidget(Login)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(50, 60, 281, 95))
        self.formLayout = QFormLayout(self.layoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.username = QLineEdit(self.layoutWidget)
        self.username.setObjectName(u"username")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.username)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.password = QLineEdit(self.layoutWidget)
        self.password.setObjectName(u"password")
        self.password.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.password)


        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"hdu-booker", None))
        self.quit_button.setText(QCoreApplication.translate("Login", u"\u9000\u51fa", None))
        self.login_button.setText(QCoreApplication.translate("Login", u"\u767b\u5f55", None))
        self.label.setText(QCoreApplication.translate("Login", u"\u5b66\u53f7\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Login", u"\u5bc6\u7801\uff1a", None))
    # retranslateUi

