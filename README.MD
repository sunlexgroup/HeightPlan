# Height Plan
## Назначение
Десктопное приложение предназначенное для автоматической генерации схем нивелировки крановых путей. Подходит для мостовых и козловых кранов.

Программа позволяет вводить параметры кранового пути, расположение кранов на пути. Расположение осей и привязок к конструктиву помещения. На выходе программы в папке программы генерируется схема нивелирровки в векторном формате SVG.

Для генерации схемы вам необходимо:

1. Заполнение начальных параметров пути;

![](https://github.com/sunlexgroup/HeightPlan/raw/master/img/main.png)

2. Добавление расположения кранов в схему. Добавить в схему крана с одинаковым заводским номером невозможно;

![](https://github.com/sunlexgroup/HeightPlan/raw/master/img/addcrane.png)

![](https://github.com/sunlexgroup/HeightPlan/raw/master/img/addcraneerror.png)

3. Добавление в схему тормозных ферм;

![](https://github.com/sunlexgroup/HeightPlan/raw/master/img/addferm.png)

4. Добавление в схему высотных точек;

![](https://github.com/sunlexgroup/HeightPlan/raw/master/img/addpoints.png)

5. Генерация схемы. Схему можно сгенерировать только в случае заполнения всех необходимых точек.

![](https://github.com/sunlexgroup/HeightPlan/raw/master/img/generatecheme.png)

Сгенерированные схемы сохраняются в папку с программой!

![](https://github.com/sunlexgroup/HeightPlan/raw/master/img/savedcheme.png)
