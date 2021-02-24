from chemeObj import Crane
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMessageBox


class addCraneDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        """
        Инициализация диалогового окна добавления крана к списку 
        """
        super(addCraneDialog, self).__init__(parent)
        self.parent = parent
        self.ui = uic.loadUi("./ui/HeightPlan-Add_crane.ui", self)

        self.ui.CraneNumber.setText("")
        self.ui.LiftingCapacity.setText("")

        liftingCapasityValidator = QDoubleValidator(0.00, 1000.00, 2, self)
        self.ui.LiftingCapacity.setValidator(liftingCapasityValidator)

        self.updatePlanePointsOptions()

    def updatePlanePointsOptions(self):
        self.ui.PlanePoint.clear()  # очищаем комбобокс
        # Заполняем сомбобокс списком точек замеров
        for i in range(1, (int(self.parent.cheme.totalPoints)+1)):
            self.ui.PlanePoint.addItem(str(i))

    def accept(self):
        """
        Проверяешь тут то, что хотел, если все хорошо вызываешь
        super().accept(), если нет, не вызываешь и выводишь подсказку
        """
        # Проверяем не пусто ли поле зав.№
        if not self.ui.CraneNumber.text():
            QMessageBox.critical(self, "Не заполнены поля",
                                 "Не заполнено поле: Зав.№")
        elif not self.ui.LiftingCapacity.text():
            QMessageBox.critical(self, "Не заполнены поля",
                                 "Не заполнено поле: Грузоподъемность Q,тн.")
        else:
            # Вносим кран в модель cheme
            # Проверяем нет ли в списке кранов крана с таким же заводским номером
            crane = Crane()
            crane.numberCrane = self.ui.CraneNumber.text()
            crane.liftingCapacityCrane = self.ui.LiftingCapacity.text()
            crane.pointPositionCrane = int(self.ui.PlanePoint.currentText())

            if self.ui.LeftAxisCrane.isChecked():
                crane.cabinePosition[0] = 1
            else:
                crane.cabinePosition[0] = 0

            if self.ui.RightAxisCrane.isChecked():
                crane.cabinePosition[1] = 1
            else:
                crane.cabinePosition[1] = 0

            if self.ui.ByStairs.isChecked():
                crane.cabinePosition[2] = 1
            else:
                crane.cabinePosition[2] = 0

            if self.ui.ByCenter.isChecked():
                crane.cabinePosition[3] = 1
            else:
                crane.cabinePosition[3] = 0

            if self.ui.OtherSide.isChecked():
                crane.cabinePosition[4] = 1
            else:
                crane.cabinePosition[4] = 0

            if self.parent.cheme.checkCrane(crane):
                self.parent.cheme.addCrane(crane)
                super().accept()
            else:
                QMessageBox.critical(self, "Ошибка добавления крана",
                                     "Кран с таким заводским номером уже добавлен, или добавляемый кран занимает чужую позицию.")

    def reject(self):
        # Очищаем поля и закрываем окно
        self.ui.CraneNumber.setText("")
        self.ui.LiftingCapacity.setText("")
        self.ui.PlanePoint.clear()
        super().reject()
