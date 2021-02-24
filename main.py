# -*- coding: utf-8 -*-
from chemeSvgGenerator import ChemeSvgGenerator
import sys
import os
import re
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem, QMainWindow, QFileDialog
from PyQt5 import uic
from PyQt5.QtSvg import QSvgWidget

from addCraneDialog import addCraneDialog
from addFermDialog import addFermDialog
from addHeightPointDialog import addHeightPointDialog

from chemeObj import ChemeObject


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class App(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.initUi()

        self.cheme = ChemeObject()
        # Переменные для хранения индексов на удаление
        self.craneListItem = [0]
        self.fermListItem = [0]

        # инициализация диалоговых окон
        self.addCraneWindow = addCraneDialog(self)
        self.addFermWindow = addFermDialog(self)
        self.addHeightPointWindow = addHeightPointDialog(self)

        # Биндинги полей формы к объекту
        self.ui.CalcNumber.setText(str(self.cheme.calcNumber))
        self.ui.Owner.setText(str(self.cheme.owner))
        self.ui.PathLength.setText(str(self.cheme.pathLength))
        self.ui.PathWidth.setText(str(self.cheme.pathWidth))
        self.ui.DimentionStep.setText(str(self.cheme.dimentionStep))
        self.ui.RailName1.setText(str(self.cheme.railOneName))
        self.ui.RailName2.setText(str(self.cheme.railTwoName))
        self.ui.PathStartName.setText(str(self.cheme.pathStartName))
        self.ui.PathCancelName.setText(str(self.cheme.pathCancelName))

        # Инициализация таблицы высотных отметок
        self.tablePlanePoint = self.ui.TablePlanePoint
        self.tablePlanePoint.setColumnCount(4)
        self.tablePlanePoint.setRowCount(0)

        self.tablePlanePoint.setHorizontalHeaderLabels([
            "№№ \n точек",
            "Условная\nотметка\nрельс {0}".format(
                self.ui.RailName1.text()),
            "Условная\nотметка\nрельс {0}".format(self.ui.RailName2.text()),
            "Колея\n+- 15 мм."
        ])
        self.updatePlanePointTable()
        self.tablePlanePoint.verticalHeader().hide()

    def initUi(self):
        """
        Инициализация интерфейса пользователя
        """
        # Подключение файла формы
        self.ui = uic.loadUi("./ui/HeightPlan-Main.ui")

        # Нажатие на кнопку генерации картинок
        self.ui.GenerateCheme.clicked.connect(self.generateCheme)

        # Кнопки вызова диалоговых окон
        self.ui.AddCrane.clicked.connect(self.addCraneDialog)
        self.ui.AddFerm.clicked.connect(self.addFermDialog)
        self.ui.AddPlanePoint.clicked.connect(self.addPlanePointDialog)

        # Кнопки для работы со списком кранов
        self.ui.ClearCraneList.clicked.connect(self.clearChemeCran)
        self.ui.DeleteCrane.clicked.connect(self.deleteSelectedCrane)

        # Кнопки для работы со списком ферм
        self.ui.ClearFermList.clicked.connect(self.clearChemeFerm)
        self.ui.DeleteFerm.clicked.connect(self.deleteSelectedFerm)

        # Кнопки для работы с таблицей точек
        self.ui.ClearPlanePoint.clicked.connect(self.clearPlanePoint)

        pathLengtValidator = QIntValidator(0, 3000000, self)
        pathWidthValidator = QIntValidator(0, 150000, self)
        dimentionStepValidator = QIntValidator(0, 25000, self)

        self.ui.PathLength.setValidator(pathLengtValidator)
        self.ui.PathWidth.setValidator(pathWidthValidator)
        self.ui.DimentionStep.setValidator(dimentionStepValidator)
        # Вызов слота после окончания ввода значения, перекидываем значение в объект
        self.ui.CalcNumber.editingFinished.connect(self.__updateCalcNumber)
        self.ui.Owner.editingFinished.connect(self.__updateOwner)
        self.ui.PathLength.editingFinished.connect(self.__updatePathLength)
        self.ui.PathWidth.editingFinished.connect(self.__updatePathWidth)
        self.ui.DimentionStep.editingFinished.connect(
            self.__updateDimentionStep)
        self.ui.RailName1.editingFinished.connect(self.__updateRailName1)
        self.ui.RailName2.editingFinished.connect(self.__updateRailName2)
        self.ui.PathStartName.editingFinished.connect(
            self.__updatePathStartName)
        self.ui.PathCancelName.editingFinished.connect(
            self.__updatePathCancelName)

        # Сигналы списков
        self.ui.CraneList.itemClicked.connect(self.craneListSelectItem)
        self.ui.FermList.itemClicked.connect(self.fermListSelectItem)

        # Инициализация SVG графики
        self.shemePreviewLayout = self.ui.ChemePreviewLayout
        self.defectShemePreviewLayout = self.ui.DefectChemePreviewLayout

        # Показываем окно пользователю
        self.ui.show()

    def generateCheme(self):
        chemes = ChemeSvgGenerator(self.cheme)
        chemes.generate()
        self.shemeSvgShemeWidget = QSvgWidget("{0} {1} - Deffects.svg".format(
            self.cheme.calcNumber, self.cheme.owner))
        self.shemeSvgShemeWidget.setGeometry(500, 500, 850, 850)
        self.shemePreviewLayout.addWidget(self.shemeSvgShemeWidget)
        self.shemeSvgShemePreviewWidget = QSvgWidget("{0} {1} - Cheme.svg".format(
            self.cheme.calcNumber, self.cheme.owner))
        self.shemeSvgShemePreviewWidget.setGeometry(500, 500, 850, 850)
        self.defectShemePreviewLayout.addWidget(self.shemeSvgShemeWidget)

    def checkPoints(self):
        if self.cheme.totalPoints == len(self.cheme.planePointList):
            return True
        else:
            return False

    def updateCraneList(self):
        """
        Метод обновляет список кранов
        """
        self.ui.CraneList.clear()
        if self.cheme.craneList:
            for crane in self.cheme.craneList:
                self.ui.CraneList.addItem(
                    "№поз.: <{2}> \tЗав.№ {0} \t Грузоподъемность: {1}".format(crane.numberCrane, crane.liftingCapacityCrane, crane.pointPositionCrane))

            self.ui.ClearCraneList.setEnabled(True)
        else:
            self.ui.DeleteCrane.setEnabled(False)
            self.ui.ClearCraneList.setEnabled(False)

    def craneListSelectItem(self, item):
        """
        Обработчик выделения
        """
        position = str(re.findall(r'<\d{1,3}>', item.text()))
        self.craneListItem[0] = int(position[3: -3])
        self.ui.DeleteCrane.setEnabled(True)

    def deleteSelectedCrane(self):
        """
        Удаление выделенный кра из списка кранов
        """
        for crane in self.cheme.craneList:
            if crane.pointPositionCrane == int(self.craneListItem[0]):
                self.cheme.craneList.remove(crane)
                self.ui.DeleteCrane.setEnabled(False)
        self.updateCraneList()

    def clearChemeCran(self):
        """
        Обработчик кнопки очистки списка кранов
        """
        self.cheme.craneList.clear()
        self.updateCraneList()

    def addCraneDialog(self):
        """
        Открывает модальное окно с добавлением крана в схему
        """
        self.addCraneWindow.updatePlanePointsOptions()
        self.addCraneWindow.show()
        res = self.addCraneWindow.exec_()

        if res == QDialog.Accepted:
            # Обновляем список кранов
            self.updateCraneList()

    def updateFermList(self):
        """
        Метод обновляет список ферм
        """
        self.ui.FermList.clear()
        if self.cheme.fermList:
            for ferm in self.cheme.fermList:
                self.ui.FermList.addItem(
                    "№поз.: <{0}>\tФерма тормозная".format(
                        ferm.pointPositionFerm))
            self.ui.ClearFermList.setEnabled(True)
        else:
            self.ui.DeleteFerm.setEnabled(False)
            self.ui.ClearFermList.setEnabled(False)

    def fermListSelectItem(self, item):
        """
        Обработчик выделения фермы
        """
        position = str(re.findall(r'<\d{1,3}>', item.text()))
        self.fermListItem[0] = int(position[3: -3])
        self.ui.DeleteFerm.setEnabled(True)

    def deleteSelectedFerm(self):
        """
        Удаление выделенную ферму из списка ферм
        """
        for ferm in self.cheme.fermList:
            if ferm.pointPositionFerm == int(self.fermListItem[0]):
                self.cheme.fermList.remove(ferm)
                self.ui.DeleteFerm.setEnabled(False)
        self.updateFermList()

    def clearChemeFerm(self):
        """
        Обработчик кнопки очистки списка ферм
        """
        self.cheme.fermList.clear()
        self.updateFermList()

    def addFermDialog(self):
        """
        Открывает модальное окно с добавлением ферм в схему
        """
        self.addFermWindow.updatePlanePointsOptions()
        self.addFermWindow.show()
        res = self.addFermWindow.exec_()
        if res == QDialog.Accepted:
            self.updateFermList()

    def clearPlanePoint(self):
        """
        Полностью очищает весь список точек
        """
        self.cheme.planePointList.clear()
        self.updatePlanePointTable()

    def updatePlanePointTable(self):
        """
        Обновляет отображение данных в таблице высотных отметок
        """
        self.tablePlanePoint.setRowCount(len(self.cheme.planePointList))
        for i in range(0, len(self.cheme.planePointList)):
            self.tablePlanePoint.setItem(
                i, 0, QTableWidgetItem(str(self.cheme.planePointList[i].pointPosition)))
            self.tablePlanePoint.setItem(
                i, 1, QTableWidgetItem(str(self.cheme.planePointList[i].heightRailOne)))
            self.tablePlanePoint.setItem(
                i, 2, QTableWidgetItem(str(self.cheme.planePointList[i].heightRailTwo)))
            self.tablePlanePoint.setItem(
                i, 3, QTableWidgetItem(str(self.cheme.planePointList[i].widthPlane)))
        self.tablePlanePoint.resizeColumnsToContents()

    def addPlanePointDialog(self):
        """
        Открывает модальное окно с добавлением точки в схему
        """
        self.addHeightPointWindow.updatePlanePointsOptions()
        self.addHeightPointWindow.show()
        res = self.addHeightPointWindow.exec_()
        if res == QDialog.Accepted:
            self.updatePlanePointTable()
            self.ui.ClearPlanePoint.setEnabled(True)
            if self.checkPoints():
                self.ui.GenerateCheme.setEnabled(True)
            else:
                self.ui.GenerateCheme.setEnabled(False)

    def openFileDialog(self):
        """
        Открытие ранее сохраненного файла со схемой
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл схемы", "", "Все файлы (*);; Файл схемы (*.hep)")

    @ pyqtSlot()
    def __updateCalcNumber(self):
        """
        Слот обновляет поле CalcNumber в объекте cheme
        """
        self.cheme.calcNumber = self.ui.CalcNumber.text()

    @ pyqtSlot()
    def __updateOwner(self):
        """
        Слот обновляет поле CalcNumber в объекте cheme
        """
        self.cheme.owner = self.ui.Owner.text()

    @ pyqtSlot()
    def __updatePathLength(self):
        """
        Слот обновляет длину пути в объекте cheme
        """
        if int(self.ui.PathLength.text()) <= self.cheme.dimentionStep:
            QMessageBox.warning(
                self, "Ошибка.", "Длинна пути не может быть меньше шага замера. Измените длину пути или шаг измерения.")
        else:
            self.cheme.pathLength = self.ui.PathLength.text()

    @ pyqtSlot()
    def __updatePathWidth(self):
        """
        Слот обновляет ширину пролета в объекте cheme
        """
        self.cheme.pathWidth = self.ui.PathWidth.text()

    @ pyqtSlot()
    def __updateDimentionStep(self):
        """
        Слот обновляет шаг измерения в объекте cheme
        """
        if int(self.ui.DimentionStep.text()) > self.cheme.pathLength:
            QMessageBox.warning(
                self, "Ошибка.", "Шаг замера не может быть Больше длинны пути. Измените длину пути или шаг измерения.")
        else:
            self.cheme.dimentionStep = self.ui.DimentionStep.text()

    @ pyqtSlot()
    def __updateRailName1(self):
        """
        Слот обновляет имя первой ости рельс в объекте cheme
        """
        self.cheme.railOneName = self.ui.RailName1.text()

    @ pyqtSlot()
    def __updateRailName2(self):
        """
        Слот обновляет имя второй оси рельс в объекте cheme
        """
        self.cheme.railTwoName = self.ui.RailName2.text()

    @ pyqtSlot()
    def __updatePathStartName(self):
        """
        Слот обновляет название стартовой оси в объекте cheme
        """
        self.cheme.pathStartName = self.ui.PathStartName.text()

    @ pyqtSlot()
    def __updatePathCancelName(self):
        """
        Слот обновляет название конечной оси в объекте cheme
        """
        self.cheme.pathCancelName = self.ui.PathCancelName.text()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = App()
    sys.exit(app.exec_())
