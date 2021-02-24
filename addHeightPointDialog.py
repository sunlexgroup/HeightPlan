# -*- coding: utf-8 -*-
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMessageBox
from chemeObj import PlanePoint
import sys
from PyQt5 import QtWidgets, uic

"""
Алгоритм работы класса:
1. Заполняем комбобокс списком равным количеству точек схемы;
2. Очищаем все поля формы;
3. Заполняем все поля формы;
4. Нажимаем кнопку ОК;
4.1. Проверяем чтобы все поля были заполнены;
4.2. Делаем запрос в главную схему на присутствие точки с таким же индексом. Если есть с таким же выводим сообщение с запросом хотим ли мы заменить на новое значение. Если с таким же индексом в схеме отсутсвует, то добавляем в схему. Окно закрывается.
"""


class addHeightPointDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        """
        Инициализация диалогового окна добавления высотной отметки к плану 
        """
        super(addHeightPointDialog, self).__init__(parent)
        self.parent = parent
        self.ui = uic.loadUi("./ui/HeightPlan-Add_height_point.ui", self)

        # Валидаторы полей формы
        HeightPail1PointValidator = QIntValidator(0, 100000, self)
        HeightPail2PointValidator = QIntValidator(0, 100000, self)
        WidthPlanePointValidator = QIntValidator(0, 300000, self)

        self.rail1Point = self.ui.HeightPail1Point
        self.rail2Point = self.ui.HeightPail2Point
        self.widthPlanePoint = self.ui.WidthPlanePoint
        self.planePoint = self.ui.PlanePoint

        self.rail1Point.setValidator(HeightPail1PointValidator)
        self.rail2Point.setValidator(HeightPail2PointValidator)
        self.widthPlanePoint.setValidator(WidthPlanePointValidator)

        self.updatePlanePointsOptions()
        self.clearFormFields()

    def updatePlanePointsOptions(self):
        self.planePoint.clear()  # очищаем комбобокс
        # Заполняем сомбобокс списком точек замеров
        for i in range(1, (int(self.parent.cheme.totalPoints)+1)):
            self.planePoint.addItem(str(i))

    def clearFormFields(self):
        """
        Метод очистки формы от значений
        """
        self.rail1Point.setText("")
        self.rail2Point.setText("")
        self.widthPlanePoint.setText("")

    def accept(self):
        if not self.rail1Point.text():
            QMessageBox.critical(self, "Не заполнены поля",
                                 "Не заполнено поле: {0}".format(self.ui.label_3.text()))
        elif not self.ui.rail2Point.text():
            QMessageBox.critical(self, "Не заполнены поля",
                                 "Не заполнено поле: {0}".format(self.ui.label_4.text()))
        elif not self.widthPlanePoint.text():
            QMessageBox.critical(self, "Не заполнены поля",
                                 "Не заполнено поле: {0}".format(self.ui.label_5.text()))
        else:
            point = PlanePoint()
            point.pointPosition = int(self.planePoint.currentText())
            point.heightRailOne = int(self.rail1Point.text())
            point.heightRailTwo = int(self.rail2Point.text())
            point.widthPlane = int(self.widthPlanePoint.text())

            if self.parent.cheme.checkHeightPoint(point):
                self.parent.cheme.addHeightPoint(point)
                super().accept()
            else:
                res = QMessageBox.question(
                    self,
                    "Подтверждение действия",
                    "В схеме найдена точка с позицией: {0}.\nЗаменить?".format(
                        self.planePoint.currentText()),
                    QMessageBox.Yes,
                    QMessageBox.No
                )

                if res == QMessageBox.Yes:
                    self.parent.cheme.replaceHeightPoint(point)
                    super().accept()
                else:
                    del(point)
                    super().reject()

    def reject(self):
        super().reject()
