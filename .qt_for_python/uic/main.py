# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
        Form.resize(997, 512)
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(310, 30, 671, 441))
        self.seat_table = QTableView(self.groupBox)
        self.seat_table.setObjectName(u"seat_table")
        self.seat_table.setGeometry(QRect(0, 50, 671, 421))
        self.change_button = QPushButton(self.groupBox)
        self.change_button.setObjectName(u"change_button")
        self.change_button.setGeometry(QRect(10, 20, 111, 23))
        self.user_info = QLabel(Form)
        self.user_info.setObjectName(u"user_info")
        self.user_info.setGeometry(QRect(10, 10, 481, 16))
        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(0, 40, 291, 321))
        self.widget = QWidget(self.groupBox_2)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 40, 281, 271))
        self.formLayout = QFormLayout(self.widget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.begin_date = QDateEdit(self.widget)
        self.begin_date.setObjectName(u"begin_date")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.begin_date)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.begin_time = QTimeEdit(self.widget)
        self.begin_time.setObjectName(u"begin_time")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.begin_time)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.interval = QLineEdit(self.widget)
        self.interval.setObjectName(u"interval")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.interval)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_5)

        self.max_try_times = QLineEdit(self.widget)
        self.max_try_times.setObjectName(u"max_try_times")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.max_try_times)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_3)

        self.status = QLabel(self.widget)
        self.status.setObjectName(u"status")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.status)

        self.about_button = QPushButton(self.widget)
        self.about_button.setObjectName(u"about_button")

        self.formLayout.setWidget(9, QFormLayout.SpanningRole, self.about_button)

        self.imme_run_button = QPushButton(self.widget)
        self.imme_run_button.setObjectName(u"imme_run_button")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.imme_run_button)

        self.wait_run_button = QPushButton(self.widget)
        self.wait_run_button.setObjectName(u"wait_run_button")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.wait_run_button)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u4e3b\u754c\u9762", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u5f85\u62a2\u5ea7\u5217\u8868", None))
        self.change_button.setText(QCoreApplication.translate("Form", u"\u4fee\u6539\u5f85\u62a2\u5ea7\u5217\u8868", None))
        self.user_info.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u62a2\u5ea7", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u65e5\u671f\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u65f6\u95f4\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u8bf7\u6c42\u95f4\u9694\uff08\u79d2\uff09\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u6700\u5927\u8bf7\u6c42\u6b21\u6570\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u72b6\u6001\uff1a", None))
        self.status.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.about_button.setText(QCoreApplication.translate("Form", u"\u5173\u4e8e", None))
        self.imme_run_button.setText(QCoreApplication.translate("Form", u"\u7acb\u5373\u5f00\u59cb\u62a2\u5ea7", None))
        self.wait_run_button.setText(QCoreApplication.translate("Form", u"\u6307\u5b9a\u65f6\u95f4\u5f00\u59cb\u62a2\u5ea7", None))
    # retranslateUi

