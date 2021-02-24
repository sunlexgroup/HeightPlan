# -*- coding: utf-8 -*-
class ChemeObject:
    def __init__(self):
        """
        Объект схемы кранового пути
        """
        self.calcNumber = ""  # Номер комплексного обследования
        self.owner = None  # Вдаделец кранового пути
        self._pathLenght = 75000  # Длинна кранового пути
        self.pathWidth = 22500  # Ширина пролета кранового пути
        self._dimentionStep = 6000  # Шаг замера
        self.totalPoints = None  # Количество точек
        self.railOneName = 'А'  # Наименование оси 1 нити рельсов
        self.railTwoName = 'В'  # Наименование оси 2 нити рельсов
        self.pathStartName = '1'  # Наименование оси начала пути
        self.pathCancelName = '2'  # Наименование оси окончания пути
        self.craneList = []  # Список кранов на пути
        self.fermList = []  # Список тормозных ферм на пути
        self.planePointList = []  # Список замеров точек

        self.totalPointsCalk()

    @property
    def pathLength(self):
        return self._pathLenght

    @pathLength.setter
    def pathLength(self, value):
        self._pathLenght = int(value)
        self.totalPointsCalk()

    @property
    def dimentionStep(self):
        return self._dimentionStep

    @dimentionStep.setter
    def dimentionStep(self, value):
        self._dimentionStep = int(value)
        self.totalPointsCalk()

    def checkCrane(self, craneObj):
        """
        Проверка наличия в списке кранов передаваемого крана
        Если кран есть в списке то возвращаем False
        """
        for crane in self.craneList:
            if craneObj.numberCrane == crane.numberCrane:
                return False
            if craneObj.pointPositionCrane == crane.pointPositionCrane:
                return False
        return True

    def addCrane(self, craneObj):
        """
        Добавление крана в список кранов схемы
        Если в списке есть кран с таким же заводским номером то обновляем его значения, если нет, то добавляем в конец списка новый объект. Делов-то.
        """
        self.craneList.append(craneObj)

    def checkFerm(self, fermObj):
        """
        Проверяем не заято ли место другой фермой
        """
        for ferm in self.fermList:
            if fermObj.pointPositionFerm == ferm.pointPositionFerm:
                return False
        return True

    def addFerm(self, fermObj):
        """
        Добавление тормозной фермы в список тормозных ферм объекта схемы
        """
        self.fermList.append(fermObj)

    def replaceHeightPoint(self, planePointObj):
        """
        Заменяет переданную запись из объекта схемы
        """
        i = 0
        for point in self.planePointList:
            if planePointObj.pointPosition == point.pointPosition:
                i = planePointObj.pointPosition
                self.planePointList[i -
                                    1].heightRailOne = planePointObj.heightRailOne
                self.planePointList[i -
                                    1].heightRailTwo = planePointObj.heightRailTwo
                self.planePointList[i-1].widthPlane = planePointObj.widthPlane

    def checkHeightPoint(self, planePointObj):
        for point in self.planePointList:
            if planePointObj.pointPosition == point.pointPosition:
                return False
        return True

    def addHeightPoint(self, planePointObj):
        """
        Добавление объекта измеренной точки в список замеров точек
        """
        self.planePointList.append(planePointObj)

    def totalPointsCalk(self):
        """
        Вычисление количества контрольных точек на пути
        """
        self.totalPoints = round(self._pathLenght / self._dimentionStep)


class Crane:
    def __init__(self):
        """
        Объект крана
        """
        self.numberCrane = None  # Заводской номер крана
        self.liftingCapacityCrane = None  # Грузоподъемность крана
        self.pointPositionCrane = 1  # Номер позиции где расположен кран
        # Расположение кабины крана [<Left>, <Right>, <byStairs>, <inCenter>, <inEnd>] пример [1,0,1,0,0]
        self.cabinePosition = [0, 0, 0, 0, 0]


class Ferm:
    def __init__(self):
        """
        Объект тормозной фермы
        """
        self.pointPositionFerm = 1  # Номер позиции где расположена ферма
        # Расположение фермы относительно позиции крана [<Left>, <Right>] пример [0,1] - значит расположение фермы справа отностительно отметки
        self.fermPointSide = [0, 1]


class PlanePoint:
    def __init__(self):
        """
        Объект высотной отметки плана
        """
        self.__pointPosition = 1  # Номер позиции высотной точки
        self.__heightRailOne = 1500  # Условная высотная отметка первой нитки рельса
        self.__heightRailTwo = 1500  # Условная высотная отметка второй нитки рельса
        self.widthPlane = 22500  # Измеренная ширина колеи

    @property
    def heightRailOne(self):
        return self.__heightRailOne

    @heightRailOne.setter
    def heightRailOne(self, value):
        """
        Устанавливает и вычисляет значение перепада высот между нитками рельса по модулю
        """
        self.__heightRailOne = value

    @property
    def heightRailTwo(self):
        return self.__heightRailTwo

    @heightRailTwo.setter
    def heightRailTwo(self, value):
        """
        Устанавливает и вычисляет значение перепада высот между нитками рельса по модулю
        """
        self.__heightRailTwo = int(value)

    @property
    def pointPosition(self):
        """
        Читает номер позиции высотной отметки
        """
        return self.__pointPosition

    @pointPosition.setter
    def pointPosition(self, value):
        """
        устанавливает номер позиции. Если номер позиции равен 1, то поля __differenceByLenghtRailOne и __differenceByLenghtRailTwo устанавливаются "-"
        """
        self.__pointPosition = value
