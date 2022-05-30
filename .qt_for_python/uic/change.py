# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'change.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(991, 524)
        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(20, 20, 241, 231))
        self.splitter = QSplitter(self.groupBox_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setGeometry(QRect(0, 30, 241, 141))
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_3.addWidget(self.label_5)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget_2 = QWidget(self.splitter)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.floor = QComboBox(self.layoutWidget_2)
        self.floor.setObjectName(u"floor")

        self.verticalLayout_2.addWidget(self.floor)

        self.seat_number = QLineEdit(self.layoutWidget_2)
        self.seat_number.setObjectName(u"seat_number")

        self.verticalLayout_2.addWidget(self.seat_number)

        self.begin_date = QDateEdit(self.layoutWidget_2)
        self.begin_date.setObjectName(u"begin_date")

        self.verticalLayout_2.addWidget(self.begin_date)

        self.begin_time = QTimeEdit(self.layoutWidget_2)
        self.begin_time.setObjectName(u"begin_time")

        self.verticalLayout_2.addWidget(self.begin_time)

        self.duration = QTimeEdit(self.layoutWidget_2)
        self.duration.setObjectName(u"duration")

        self.verticalLayout_2.addWidget(self.duration)

        self.splitter.addWidget(self.layoutWidget_2)
        self.layoutWidget_3 = QWidget(self.groupBox_2)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(0, 200, 241, 25))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.add_button = QPushButton(self.layoutWidget_3)
        self.add_button.setObjectName(u"add_button")
        self.add_button.setEnabled(True)

        self.horizontalLayout.addWidget(self.add_button)

        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(20, 300, 241, 201))
        self.layoutWidget_4 = QWidget(self.groupBox_3)
        self.layoutWidget_4.setObjectName(u"layoutWidget_4")
        self.layoutWidget_4.setGeometry(QRect(0, 20, 241, 113))
        self.formLayout = QFormLayout(self.layoutWidget_4)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.layoutWidget_4)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_7)

        self.uniform_begin_time = QTimeEdit(self.layoutWidget_4)
        self.uniform_begin_time.setObjectName(u"uniform_begin_time")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.uniform_begin_time)

        self.label_6 = QLabel(self.layoutWidget_4)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_6)

        self.uniform_begin_date = QDateEdit(self.layoutWidget_4)
        self.uniform_begin_date.setObjectName(u"uniform_begin_date")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.uniform_begin_date)

        self.uniform_duration = QTimeEdit(self.layoutWidget_4)
        self.uniform_duration.setObjectName(u"uniform_duration")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.uniform_duration)

        self.label_8 = QLabel(self.layoutWidget_4)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_8)

        self.uniform_change_button = QPushButton(self.groupBox_3)
        self.uniform_change_button.setObjectName(u"uniform_change_button")
        self.uniform_change_button.setEnabled(True)
        self.uniform_change_button.setGeometry(QRect(0, 160, 239, 23))
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(300, 20, 671, 481))
        self.seat_table = QTableView(self.groupBox)
        self.seat_table.setObjectName(u"seat_table")
        self.seat_table.setGeometry(QRect(0, 70, 671, 411))
        self.delete_all_button = QPushButton(self.groupBox)
        self.delete_all_button.setObjectName(u"delete_all_button")
        self.delete_all_button.setGeometry(QRect(10, 30, 71, 31))
        self.delete_one_button = QPushButton(self.groupBox)
        self.delete_one_button.setObjectName(u"delete_one_button")
        self.delete_one_button.setGeometry(QRect(90, 30, 81, 31))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u4fee\u6539\u5ea7\u4f4d\u5217\u8868", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u6dfb\u52a0\u5ea7\u4f4d", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u697c\u5c42\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u5ea7\u4f4d\u53f7\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u65e5\u671f\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u65f6\u95f4\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u6301\u7eed\u65f6\u95f4\uff1a", None))
        self.add_button.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0\u5ea7\u4f4d", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"\u4e00\u952e\u4fee\u6539\u65f6\u95f4", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u65f6\u95f4\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u65e5\u671f\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u6301\u7eed\u65f6\u95f4\uff1a", None))
        self.uniform_change_button.setText(QCoreApplication.translate("Form", u"\u7edf\u4e00\u4fee\u6539\u65f6\u95f4", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u5f85\u62a2\u5ea7\u5217\u8868", None))
        self.delete_all_button.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u5168\u90e8", None))
        self.delete_one_button.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u6307\u5b9a\u9879", None))
    # retranslateUi

