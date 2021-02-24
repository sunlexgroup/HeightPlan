from PyQt5.QtWidgets import QMessageBox
from chemeObj import Ferm
import sys
from PyQt5 import QtWidgets, uic


class addFermDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        """
        Инициализация диалогового окна добавления крана к списку 
        """
        super(addFermDialog, self).__init__(parent)
        self.parent = parent
        self.ui = uic.loadUi("./ui/HeightPlan-Add_ferm.ui", self)

        self.updatePlanePointsOptions()

    def updatePlanePointsOptions(self):
        self.ui.PlanePoint.clear()  # очищаем комбобокс
        # Заполняем сомбобокс списком точек замеров
        for i in range(1, (int(self.parent.cheme.totalPoints)+1)):
            self.ui.PlanePoint.addItem(str(i))

    def accept(self):
        """
        docstring
        """
        # Создаем объект фермы
        ferm = Ferm()
        ferm.pointPositionFerm = int(self.ui.PlanePoint.currentText())
        if self.ui.RightSide.isChecked():
            ferm.fermPointSide[1] = 1
        else:
            ferm.fermPointSide[1] = 0
        if self.ui.LeftSide.isChecked():
            ferm.fermPointSide[0] = 1
        else:
            ferm.fermPointSide[0] = 0

        # Проверяем нет ли на этом месте фермы если нет вносим в схему ферму
        if self.parent.cheme.checkFerm(ferm):
            self.parent.cheme.addFerm(ferm)
            super().accept()
        else:
            QMessageBox.critical(
                self, "Ошибка добавления фермы", "На этой позиции уже есть ферма.")

    def reject(self):
        """
        Обработчик нажатия на кнопку Cancel очищаем список точек
        """
        self.ui.PlanePoint.clear()
        super().reject()
