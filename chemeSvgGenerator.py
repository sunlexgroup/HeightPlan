# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET


class PointDifferents():
    def __init__(self):
        self.differentWidth = 0
        self.differentRailOne = 0
        self.differentRailTwo = 0


class ChemeSvgGenerator():
    def __init__(self, chemeObject=None) -> None:
        self.listPointXCoordinates = []  # Список координат точек
        self.__startCoordinatesX = 130  # Начальная координата по Х
        self.__endCoordinatesX = 837  # Конечная координата по Х
        self.__cheme = chemeObject  # Входной объект схемы
        self.__minHeight = None  # Минимальное значение высоты из списка точек
        self.__textPointValues = []  # Вычисленные значения для каждой из высотных точек ?
        self.__stepX = 0
        #self.path = os.path.join(os.path.abspath(os.path.dirname(__file__)), self.tempSvgFileName)

        self.__addXCoordinates()
        self.__getMinHeight()

        # Создаем шаблонный файл, с предварительной базовой моделью SVG файла
        self.tempSvgFileName = ".temp.svg"  # Имя файла
        tempSvgFile = open(self.tempSvgFileName, "w+",
                           encoding="UTF-8")  # Создаем файл
        tempSvgFile.write('<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="848" height="497" viewBox="0 0 850 500" xml:space="preserve"><defs><style>.cls-1,.cls-12,.cls-17,.cls-2,.cls-3,.cls-8{fill:none}.cls-1,.cls-2,.cls-3,.cls-4,.cls-7,.cls-8,.cls-9{stroke:#1d1d1b;}.cls-1,.cls-11,.cls-12,.cls-17,.cls-2,.cls-3,.cls-4,.cls-7,.cls-8,.cls-9{stroke-miterlimit:10}.cls-2{stroke-linecap:round}.cls-3,.cls-4,.cls-7,.cls-8,.cls-9{stroke-width:0.5px}.cls-11,.cls-4,.cls-9{fill:#fff;}.cls-10,.cls-13,.cls-14,.cls-15,.cls-16,.cls-18,.cls-19,.cls-20,.cls-5,.cls-6{isolation: isolate}.cls-20,.cls-5,.cls-6{font-size:13.34px}.cls-5{fill:#be1622;}.cls-10,.cls-14,.cls-15,.cls-16,.cls-18,.cls-19,.cls-20,.cls-5,.cls-6{font-family:Arial-ItalicMT, Arial; font-style:italic; text-align: center;}.cls-6,.cls-7{fill:#1d1d1b;}.cls-8,.cls-9{stroke-linecap: square}.cls-10,.cls-16{font-size:10.67px}.cls-10{fill:#575756;}.cls-11,.cls-12 {stroke:#9d9d9c;}.cls-14,.cls-15,.cls-18,.cls-19{font-size: 8px}.cls-14,.cls-15,.cls-16{fill:#9d9d9c;}.cls-15,.cls-19{letter-spacing:-0.01em}.cls-17{stroke:#b2b2b2;}.cls-18,.cls-19{fill:#878787;}.cls-20{fill:#00a19a;}</style></defs><g id="base-layer"></g><g id="position-layer"></g><g id="ferm-layer"></g><g id="crane-layer"></g><g id="text-layer"></g></svg>')  # Записываем в файл начальный шаблон SVG файла
        tempSvgFile.close()  # Закрываем файл

    def __deleteTempFile(self):
        """
        Удаляет файл схемы temp
        """
        pass

    def __addXCoordinates(self):
        """
        Вычисляет координаты X для всех загруженных точек
        """
        stepX = (self.__endCoordinatesX - self.__startCoordinatesX) / \
            (self.__cheme.totalPoints-1)
        self.__stepX = stepX
        x = self.__startCoordinatesX
        for i in range(0, self.__cheme.totalPoints):
            if i == 0:
                x = self.__startCoordinatesX
            else:
                x += stepX
            self.listPointXCoordinates.append(round(x))

    def __getMinHeight(self):
        """
        Вычисляет самую высокую отметку из замеров плана
        """
        heightPoints = []
        for point in self.__cheme.planePointList:
            heightPoints.append(point.heightRailOne)
            heightPoints.append(point.heightRailTwo)
        self.__minHeight = min(heightPoints)

    def __calcPointPosition(self):
        """
        Проходим по каждой точке и производим необходимые вычисления. Заносим данные в виде объекта в список __textPointValues
        """
        for i in range(0, self.__totalPoints):
            pointText = PointDifferents()
            pointText.differentRailOne = abs(
                self.__cheme.planePointList[i].heightRailOne - self.__minHeight)
            pointText.differentRailTwo = abs(
                self.__cheme.planePointList[i].heightRailTwo - self.__minHeight)
            pointText.differentWidth = self.__cheme.pathWidth - \
                self.__cheme.planePointList[i].widthPlane
            self.__textPointValues.append(pointText)

    def saveSVGFile(self, defcheme=False):
        """
        Сохраняет файл картинки с нужным типом и названием
        """
        fileName = ""
        if defcheme:
            fileName = "{0} {1} - Deffects.svg".format(
                self.__cheme.calcNumber, self.__cheme.owner)
        else:
            fileName = "{0} {1} - Cheme.svg".format(
                self.__cheme.calcNumber, self.__cheme.owner)

        f = open(self.tempSvgFileName, 'r')
        file_data = f.read()
        f.close()

        fw = open(fileName, "w+")
        fw.write(file_data)
        fw.close()

    def generate(self):
        """
        Конвейер создания картинок схем.
        """
        self.addBaseTemplate()
        # Добавляем тормозные фермы к схему
        for ferm in self.__cheme.fermList:
          # Перебираем список ферм в объекте схемы
            currentXcoortdinate = self.listPointXCoordinates[ferm.pointPositionFerm - 1]
            fermPosition = ferm.fermPointSide
            self.addFerm(x=currentXcoortdinate, ferm_position=fermPosition)

        # Добавляем краны в схему
        for crane in self.__cheme.craneList:
            currentXcoortdinate = self.listPointXCoordinates[crane.pointPositionCrane - 1]
            zav_number = str(crane.numberCrane)
            capacity = str(crane.liftingCapacityCrane)
            cabinePosition = crane.cabinePosition
            self.addCran(x=currentXcoortdinate, number=zav_number,
                         Q=capacity, cabine_position=cabinePosition)

        # Добавляем точки замеров
        for point in self.__cheme.planePointList:
            currentXcoortdinate = self.listPointXCoordinates[self.__cheme.planePointList.index(
                point)]
            item = point.pointPosition
            self.addPosition(x=currentXcoortdinate, item=item)

        # Сохраняем схему дефектов
        self.saveSVGFile(defcheme=True)

        # Добавляем значения к точкам замеров
        for point in self.__cheme.planePointList:
            currentXcoortdinate = self.listPointXCoordinates[self.__cheme.planePointList.index(
                point)]
            dimensionRailOne = point.heightRailOne - self.__minHeight
            dimensionRailTwo = point.heightRailTwo - self.__minHeight
            width = int(point.widthPlane) - int(self.__cheme.pathWidth)
            if width > 0:
                width = "+{0}".format(width)
            else:
                width = "{}".format(width)
            self.addPointText(x=currentXcoortdinate, width=width,
                              dimensionRailOne=dimensionRailOne, dimensionRailTwo=dimensionRailTwo)
        self.saveSVGFile(defcheme=False)

        # Удаляем темп файл
        path = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), self.tempSvgFileName)
        os.remove(path)
        return True

    def addBaseTemplate(self):
        """
        Добавляет базовый шаблон в файл
        """
        layer = "base-layer"
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        tree = ET.parse(self.tempSvgFileName)
        root = tree.getroot()
        for layout in root.findall('{http://www.w3.org/2000/svg}g'):
            if layout.attrib['id'] == layer:
                # line rail-top
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "rail-top")
                elem.set("class", "cls-1")
                elem.set("x1", "837")
                elem.set("y1", "116")
                elem.set("x2", "130")
                elem.set("y2", "116")
                # line buffer-left-top
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "buffer-left-top")
                elem.set("class", "cls-2")
                elem.set("x1", "130")
                elem.set("y1", "120")
                elem.set("x2", "130")
                elem.set("y2", "112")
                # line buffer-right-top
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "buffer-right-top")
                elem.set("class", "cls-2")
                elem.set("x1", "837")
                elem.set("y1", "120")
                elem.set("x2", "837")
                elem.set("y2", "112")
                # line rail-buttom
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "rail-buttom")
                elem.set("class", "cls-1")
                elem.set("x1", "837")
                elem.set("y1", "367")
                elem.set("x2", "130")
                elem.set("y2", "367")
                # line buffer-left-buttom
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "buffer-left-buttom")
                elem.set("class", "cls-2")
                elem.set("x1", "130")
                elem.set("y1", "371")
                elem.set("x2", "130")
                elem.set("y2", "364")
                # line buffer-right-buttom
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "buffer-right-buttom")
                elem.set("class", "cls-2")
                elem.set("x1", "837")
                elem.set("y1", "371")
                elem.set("x2", "837")
                elem.set("y2", "364")
                # line axis-end
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "axis-end")
                elem.set("class", "cls-3")
                elem.set("x1", "837")
                elem.set("y1", "367")
                elem.set("x2", "837")
                elem.set("y2", "486")
                # circle axis-end-circle
                elem = ET.SubElement(layout, 'circle')
                elem.set("id", "axis-end-circle")
                elem.set("class", "cls-4")
                elem.set("cx", "837")
                elem.set("cy", "486")
                elem.set("r", "11")
                # axis-end-text
                elem = ET.SubElement(layout, 'text')
                elem.set("id", "axis-end-text")
                elem.set("class", "cls-5")
                elem.set("transform", "translate(829 491)")
                elem.text = str(self.__cheme.pathCancelName)
                # line axis-start
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "axis-start")
                elem.set("class", "cls-3")
                elem.set("x1", "130")
                elem.set("y1", "367")
                elem.set("x2", "130")
                elem.set("y2", "486")
                # circle axis-start-circle
                elem = ET.SubElement(layout, 'circle')
                elem.set("id", "axis-start-circle")
                elem.set("class", "cls-4")
                elem.set("cx", "130")
                elem.set("cy", "486")
                elem.set("r", "11")
                # axis-start-text
                elem = ET.SubElement(layout, 'text')
                elem.set("id", "axis-start-text")
                elem.set("class", "cls-5")
                elem.set("transform", "translate(123 491)")
                elem.text = str(self.__cheme.pathStartName)
                # length-pointer
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "length-pointer")
                elem.set("class", "cls-3")
                elem.set("x1", "130")
                elem.set("y1", "459")
                elem.set("x2", "837")
                elem.set("y2", "459")
                # length
                elem = ET.SubElement(layout, 'text')
                elem.set("id", "length")
                elem.set("class", "cls-6")
                elem.set("transform", "translate(461 456)")
                elem.text = str(self.__cheme.pathLength)
                # axis-a
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "axis-a")
                elem.set("class", "cls-3")
                elem.set("x1", "130")
                elem.set("y1", "116")
                elem.set("x2", "11")
                elem.set("y2", "116")
                # circle axis-a-circle
                elem = ET.SubElement(layout, 'circle')
                elem.set("id", "axis-a-circle")
                elem.set("class", "cls-4")
                elem.set("cx", "11")
                elem.set("cy", "116")
                elem.set("r", "11")
                # axis-a-text
                elem = ET.SubElement(layout, 'text')
                elem.set("id", "axis-a-text")
                elem.set("class", "cls-5")
                elem.set("transform", "translate(6 120)")
                elem.text = str(self.__cheme.railOneName)
                # axis-b
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "axis-b")
                elem.set("class", "cls-3")
                elem.set("x1", "130")
                elem.set("y1", "367")
                elem.set("x2", "11")
                elem.set("y2", "367")
                # circle axis-b-circle
                elem = ET.SubElement(layout, 'circle')
                elem.set("id", "axis-b-circle")
                elem.set("class", "cls-4")
                elem.set("cx", "11")
                elem.set("cy", "367")
                elem.set("r", "11")
                # axis-b-text
                elem = ET.SubElement(layout, 'text')
                elem.set("id", "axis-b-text")
                elem.set("class", "cls-5")
                elem.set("transform", "translate(6 372)")
                elem.text = str(self.__cheme.railTwoName)
                # width-pointer
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "width-pointer")
                elem.set("class", "cls-3")
                elem.set("x1", "37")
                elem.set("y1", "116")
                elem.set("x2", "37")
                elem.set("y2", "367")
                # top-line
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "top-line")
                elem.set("class", "cls-3")
                elem.set("x1", "837")
                elem.set("y1", "105")
                elem.set("x2", "130")
                elem.set("y2", "105")
                # button-line
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "button-line")
                elem.set("class", "cls-3")
                elem.set("x1", "837")
                elem.set("y1", "379")
                elem.set("x2", "130")
                elem.set("y2", "379")
                # width
                elem = ET.SubElement(layout, 'text')
                elem.set("id", "width")
                elem.set("class", "cls-6")
                elem.set("transform", "translate(41 223) rotate(90)")
                elem.text = str(self.__cheme.pathWidth)
                # poligon strelca
                elem = ET.SubElement(layout, 'polygon')
                elem.set("class", "cls-7")
                elem.set("points", "33 128 37 116 41 128 37 127 33 128")
                # poligon strelca
                elem = ET.SubElement(layout, 'polygon')
                elem.set("class", "cls-7")
                elem.set("points", "41 355 37 367 33 355 37 356 41 355")
                # poligon strelca
                elem = ET.SubElement(layout, 'polygon')
                elem.set("class", "cls-7")
                elem.set("points", "143 463 130 459 143 456 141 459 143 463")
                # poligon strelca
                elem = ET.SubElement(layout, 'polygon')
                elem.set("class", "cls-7")
                elem.set("points", "825 456 837 459 825 463 826 459 825 456")
        tree.write(self.tempSvgFileName,
                   encoding='utf-8', xml_declaration=True)

    def addCran(self, x=0, number="000", Q="0,00", cabine_position=[0, 1, 1, 0, 0]):
        """
        Добавляет кран в файл
        """
        layer = "crane-layer"
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        tree = ET.parse(self.tempSvgFileName)
        root = tree.getroot()
        for layout in root.findall('{http://www.w3.org/2000/svg}g'):
            if layout.attrib['id'] == layer:
                # cabine position right bottom
                # top balka
                elem = ET.SubElement(layout, 'rect')
                elem.set("class", "cls-11")
                elem.set("x", str(x-15))
                elem.set("y", "112")
                elem.set("width", "30")
                elem.set("height", "17")
                # bottom balka
                elem = ET.SubElement(layout, 'rect')
                elem.set("class", "cls-11")
                elem.set("x", str(x-15))
                elem.set("y", "354")
                elem.set("width", "30")
                elem.set("height", "17")
                # line 1 most
                elem = ET.SubElement(layout, 'line')
                elem.set("class", "cls-12")
                elem.set("x1", str(x+11))
                elem.set("y1", "129")
                elem.set("x2", str(x+11))
                elem.set("y2", "354")
                # line 2 most
                elem = ET.SubElement(layout, 'line')
                elem.set("class", "cls-12")
                elem.set("x1", str(x-11))
                elem.set("y1", "129")
                elem.set("x2", str(x-11))
                elem.set("y2", "354")
                # crane_text
                elem = ET.SubElement(layout, 'text')
                elem.set("class", "cls-14")
                elem.set(
                    "transform", "translate({0} 197) rotate(90)".format(x-3))
                elem.text = "Q={0} тн., Зав.№ {1}".format(Q, number)
                if "".join(map(str, cabine_position)) == "01100":
                    # add cabine right bottom
                    # cabine rect
                    elem = ET.SubElement(layout, 'rect')
                    elem.set("class", "cls-11")
                    elem.set("x", str(x+9))
                    elem.set("y", "316")
                    elem.set("width", "19")
                    elem.set("height", "30")
                    # cabine_text
                    elem = ET.SubElement(layout, 'text')
                    elem.set("class", "cls-16")
                    elem.set(
                        "transform", "translate({0} 328) rotate(90)".format(x+15))
                    elem.text = "K"
                if "".join(map(str, cabine_position)) == "01010":
                    # add cabine right center
                    # cabine rect
                    elem = ET.SubElement(layout, 'rect')
                    elem.set("class", "cls-11")
                    elem.set("x", str(x+9))
                    elem.set("y", "227")
                    elem.set("width", "19")
                    elem.set("height", "30")
                    # cabine_text
                    elem = ET.SubElement(layout, 'text')
                    elem.set("class", "cls-16")
                    elem.set(
                        "transform", "translate({0} 239) rotate(90)".format(x+15))
                    elem.text = "K"
                if "".join(map(str, cabine_position)) == "01001":
                    # add cabine right top
                    # cabine rect
                    elem = ET.SubElement(layout, 'rect')
                    elem.set("class", "cls-11")
                    elem.set("x", str(x+9))
                    elem.set("y", "137")
                    elem.set("width", "19")
                    elem.set("height", "30")
                    # cabine_text
                    elem = ET.SubElement(layout, 'text')
                    elem.set("class", "cls-16")
                    elem.set(
                        "transform", "translate({0} 149) rotate(90)".format(x+15))
                    elem.text = "K"
                if "".join(map(str, cabine_position)) == "10001":
                    # add cabine left top
                    # cabine rect
                    elem = ET.SubElement(layout, 'rect')
                    elem.set("class", "cls-11")
                    elem.set("x", str(x-28))
                    elem.set("y", "137")
                    elem.set("width", "19")
                    elem.set("height", "30")
                    # cabine_text
                    elem = ET.SubElement(layout, 'text')
                    elem.set("class", "cls-16")
                    elem.set(
                        "transform", "translate({0} 149) rotate(90)".format(x-22))
                    elem.text = "K"
                if "".join(map(str, cabine_position)) == "10010":
                    # add cabine left center
                    # cabine rect
                    elem = ET.SubElement(layout, 'rect')
                    elem.set("class", "cls-11")
                    elem.set("x", str(x-28))
                    elem.set("y", "227")
                    elem.set("width", "19")
                    elem.set("height", "30")
                    # cabine_text
                    elem = ET.SubElement(layout, 'text')
                    elem.set("class", "cls-16")
                    elem.set(
                        "transform", "translate({0} 239) rotate(90)".format(x-22))
                    elem.text = "K"
                if "".join(map(str, cabine_position)) == "10100":
                    # add cabine left bottom
                    # cabine rect
                    elem = ET.SubElement(layout, 'rect')
                    elem.set("class", "cls-11")
                    elem.set("x", str(x-28))
                    elem.set("y", "316")
                    elem.set("width", "19")
                    elem.set("height", "30")
                    # cabine_text
                    elem = ET.SubElement(layout, 'text')
                    elem.set("class", "cls-16")
                    elem.set(
                        "transform", "translate({0} 328) rotate(90)".format(x-22))
                    elem.text = "K"
        tree.write(self.tempSvgFileName,
                   encoding='utf-8', xml_declaration=True)

    def addFerm(self, x=0, ferm_position=[0, 1]):
        """
        Добавляет тормозную ферму в файл
        """
        layer = "ferm-layer"
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        tree = ET.parse(self.tempSvgFileName)
        root = tree.getroot()
        for layout in root.findall('{http://www.w3.org/2000/svg}g'):
            if layout.attrib['id'] == layer:
                if "".join(map(str, ferm_position)) == "10":
                    # line 1 top left ferm
                    elem = ET.SubElement(layout, 'line')
                    elem.set("class", "cls-3")
                    elem.set("x1", str(x-5))
                    elem.set("y1", "125")
                    elem.set("x2", str((x-self.__stepX)+5))
                    elem.set("y2", "105")
                    # line 2 top left ferm
                    elem = ET.SubElement(layout, 'line')
                    elem.set("class", "cls-3")
                    elem.set("x1", str(x-5))
                    elem.set("y1", "105")
                    elem.set("x2", str((x-self.__stepX)+5))
                    elem.set("y2", "125")
                    # line 1 bottom left ferm
                    elem = ET.SubElement(layout, 'line')
                    elem.set("class", "cls-3")
                    elem.set("x1", str(x-5))
                    elem.set("y1", "379")
                    elem.set("x2", str((x-self.__stepX)+5))
                    elem.set("y2", "359")
                    # line 2 bottom left ferm
                    elem = ET.SubElement(layout, 'line')
                    elem.set("class", "cls-3")
                    elem.set("x1", str(x-5))
                    elem.set("y1", "359")
                    elem.set("x2", str((x-self.__stepX)+5))
                    elem.set("y2", "379")
                if "".join(map(str, ferm_position)) == "01":
                    # line 1 top right ferm
                    elem = ET.SubElement(layout, 'line')
                    elem.set("class", "cls-3")
                    elem.set("x1", str(x+5))
                    elem.set("y1", "125")
                    elem.set("x2", str((x+self.__stepX)-4))
                    elem.set("y2", "105")
                    # line 2 top rigth ferm
                    elem = ET.SubElement(layout, 'line')
                    elem.set("class", "cls-3")
                    elem.set("x1", str(x+5))
                    elem.set("y1", "105")
                    elem.set("x2", str((x+self.__stepX)-4))
                    elem.set("y2", "125")
                    # line 1 bottom right ferm
                    elem = ET.SubElement(layout, 'line')
                    elem.set("class", "cls-3")
                    elem.set("x1", str(x+5))
                    elem.set("y1", "379")
                    elem.set("x2", str((x+self.__stepX)-4))
                    elem.set("y2", "359")
                    # line 2 bottom right ferm
                    elem = ET.SubElement(layout, 'line')
                    elem.set("class", "cls-3")
                    elem.set("x1", str(x+5))
                    elem.set("y1", "359")
                    elem.set("x2", str((x+self.__stepX)-4))
                    elem.set("y2", "379")
        tree.write(self.tempSvgFileName,
                   encoding='utf-8', xml_declaration=True)

    def addPosition(self, x=0, item=1):
        """
        Добавляет точку в файл
        """
        layer = "position-layer"
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        tree = ET.parse(self.tempSvgFileName)
        root = tree.getroot()
        for layout in root.findall('{http://www.w3.org/2000/svg}g'):
            if layout.attrib['id'] == layer:
                # position-support-bottom
                elem = ET.SubElement(layout, 'rect')
                elem.set("id", "position-support-bottom")
                elem.set("class", "cls-8")
                elem.set("x", str(x-5))
                elem.set("y", "359")
                elem.set("width", "10")
                elem.set("height", "20")
                # position-support-top
                elem = ET.SubElement(layout, 'rect')
                elem.set("id", "position-support-top")
                elem.set("class", "cls-8")
                elem.set("x", str(x-5))
                elem.set("y", "105")
                elem.set("width", "10")
                elem.set("height", "20")
                # position-axis-support-bottom
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "position-axis-support-bottom")
                elem.set("class", "cls-8")
                elem.set("x1", str(x))
                elem.set("y1", "282")
                elem.set("x2", str(x))
                elem.set("y2", "359")
                # position-axis-support-top
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "position-axis-support-top")
                elem.set("class", "cls-8")
                elem.set("x1", str(x))
                elem.set("y1", "125")
                elem.set("x2", str(x))
                elem.set("y2", "200")
                # position-axis-top
                elem = ET.SubElement(layout, 'line')
                elem.set("id", "position-axis-support-top")
                elem.set("class", "cls-8")
                elem.set("x1", str(x))
                elem.set("y1", "9")
                elem.set("x2", str(x))
                elem.set("y2", "65")
                # position-circle
                elem = ET.SubElement(layout, 'circle')
                elem.set("id", "position-axis-support-top")
                elem.set("class", "cls-9")
                elem.set("cx", str(x))
                elem.set("cy", "9")
                elem.set("r", "9")
                # position-text
                elem = ET.SubElement(layout, 'text')
                elem.set("id", "position-text")
                elem.set("class", "cls-10")
                elem.set("transform", "translate({} 12)".format(x-5))
                elem.text = str(item)
        tree.write(self.tempSvgFileName,
                   encoding='utf-8', xml_declaration=True)

    def addPointText(self, x=0, width="0", dimensionRailOne=1, dimensionRailTwo=1):
        """
        Добавляет текст точки в файл
        """
        layer = "text-layer"
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        tree = ET.parse(self.tempSvgFileName)
        root = tree.getroot()
        for layout in root.findall('{http://www.w3.org/2000/svg}g'):
            if layout.attrib['id'] == layer:
                # position-point-width-center
                elem = ET.SubElement(layout, 'text')
                elem.set("id", "position-point-width-center")
                elem.set("class", "cls-20")
                elem.set("transform", "translate({0} 248)".format(x-3))
                elem.text = str(width)
                # position-point-height-top
                elem = ET.SubElement(layout, 'text')
                elem.set("id", "position-point-height-top")
                elem.set("class", "cls-20")
                elem.set("transform", "translate({0} 96)".format(x-3))
                elem.text = str(dimensionRailOne)
                # position-point-height-bottom
                elem = ET.SubElement(layout, 'text')
                elem.set("id", "position-point-height-bottom")
                elem.set("class", "cls-20")
                elem.set("transform", "translate({0} 395)".format(x-3))
                elem.text = str(dimensionRailTwo)
        tree.write(self.tempSvgFileName,
                   encoding='utf-8', xml_declaration=True)
