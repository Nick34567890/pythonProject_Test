from enum import global_str

import requests
from urllib3 import request

from ui_mainpage import Ui_Dialog
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QDialog, QPushButton, QRadioButton, QLabel, QWidget
from PySide6.QtCore import QRect
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QWidget
from PySide6.QtCore import QCoreApplication
url = ''

last_index = 0


class MyMainPage(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle("Main Page")

        # Hide widget initially
        self.widget_3.setHidden(True)
        global url
        url = requests.get("https://raw.githubusercontent.com/burdujaadrian/practice_work/main/url.txt").text
        print(url)
        print(url[:-1]+"/api/collections/students/records?fields=id,Surname_Name,Age,Year")

        response = requests.get(url[:-1]+"/api/collections/students/records?fields=id,Surname_Name,Age,Year")
        print(response.text)

        # Example student data with consistent lowercase status
        self.students = {
            "burduja_adrian": {
                "name": "Burduja Adrian",
                "age": "20",
                "year_of_birth": "2004",
                "gender": "Male",
                "student_id": "33441",
                "percentage": "10",
                "status": "present"  # Initial status set to 'present'
            },
            "denis_plesa": {
                "name": "Plesa Denis",
                "age": "19",
                "year_of_birth": "2005",
                "gender": "Male",
                "student_id": "33442",
                "status": "absent",  # Initial status set to 'absent'
            },
            # Add more students as needed...
        }

        # Add student widgets
        index = 0
        row = 0
        width = 161
        height = 201
        padding = 40
        spacing = 20
        for key, value in self.students.items():
            # button formating
            button = QPushButton(parent=self.Students, text=f"{value['name']} - Age: {value['age']}")
            button.setStyleSheet(u"background-color: #8DB7F5;\n"
"border-top-left-radius: 10px;          \n"
"border-bottom-left-radius: 10px;       \n"
"border-top-right-radius: 10px;         \n"
"border-bottom-right-radius: 10px;      \n"
"\n"
"   ")

            button.setGeometry(QRect(30+(width+padding)*index, 30+(height + spacing)*row, width, height))
            index += 1
            if index > 3:
                index = 0
                row+=1

            # Connect the button's clicked signal to a lambda function
            # TODO! add the function for the whole button
            # button.clicked.connect(lambda _, k=key: self.handle_button_click(k))

        # Initialize the current student key
        self.current_student_key = None

        # Connect buttons to functions
        self.search_1.clicked.connect(self.switch_to_search_Page)
        self.search_2.clicked.connect(self.switch_to_search_Page)
        self.classes_1.clicked.connect(self.switch_to_classes_Page)
        self.classes_2.clicked.connect(self.switch_to_classes_Page)
        self.setting_1.clicked.connect(self.switch_to_setting_Page)
        self.setting_2.clicked.connect(self.switch_to_setting_Page)
        self.pushButton_4.clicked.connect(self.switch_to_class_with_students)

        # Connect student buttons with lambda functions
        self.pushButton_7.clicked.connect(lambda: self.switch_to_page_with_present("denis_plesa"))
        # self.pushButton_14.clicked.connect(lambda: self.switch_to_page_with_present("burduja_adrian"))
        # # Repeat for all other buttons
        # self.pushButton_20.clicked.connect(lambda: self.switch_to_page_with_present("artur_tugui"))
        # self.pushButton_23.clicked.connect(lambda: self.switch_to_page_with_present("nichita_gancear"))
        # self.pushButton_26.clicked.connect(lambda: self.switch_to_page_with_present("victoria_cerchez"))


        # Back button
        self.pushButton_64.clicked.connect(self.switch_to_class_with_students)

        # Connect the pushButton_62 click to toggle status
        self.pushButton_62.clicked.connect(self.toggle_status)

    def switch_to_search_Page(self):
        self.stackedWidget.setCurrentIndex(0)

    def switch_to_classes_Page(self):
        self.stackedWidget.setCurrentIndex(3)

    def switch_to_setting_Page(self):
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_class_with_students(self):
        self.stackedWidget.setCurrentIndex(2)

    def switch_to_page_with_present(self, student_key):
        # Store the current student key
        self.current_student_key = student_key

        value = self.students.get(student_key, {})

        if value:
            self.stackedWidget.setCurrentIndex(4)
            # Update the buttons with student info
            self.pushButton_57.setText(QCoreApplication.translate("Dialog", value["name"], None))
            self.pushButton_58.setText(QCoreApplication.translate("Dialog", value["age"], None))
            self.pushButton_59.setText(QCoreApplication.translate("Dialog", value["year_of_birth"], None))
            self.pushButton_60.setText(QCoreApplication.translate("Dialog", value["gender"], None))
            self.pushButton_61.setText(QCoreApplication.translate("Dialog", value["student_id"], None))

            # Update the status button based on the student's current status
            self.update_status_button(value["status"])

            self.label_6.setText(QCoreApplication.translate("Dialog", u"Classes", None))
        else:
            print(f"Student info for {student_key} not found.")

    def update_status_button(self, status):
        """Update the pushButton_62 with the correct text and style."""
        if status == 'present':
            self.pushButton_62.setText(QCoreApplication.translate("Dialog", "Present", None))
            self.pushButton_62.setStyleSheet(u"background-color: #108476; color: #ffffff")
        else:
            self.pushButton_62.setText(QCoreApplication.translate("Dialog", "Absent", None))
            self.pushButton_62.setStyleSheet(u"background-color: #d8d8d8; color: #000000")

    def toggle_status(self):
        """Toggle the status of the currently selected student between 'present' and 'absent'."""
        if self.current_student_key:
            value = self.students.get(self.current_student_key)
            if value:
                # Toggle status
                if value["status"] == "present":
                    value["status"] = "absent"
                else:
                    value["status"] = "present"

                # Update the button display based on the new status
                self.update_status_button(value["status"])
        else:
            print("No student selected for status change.")
