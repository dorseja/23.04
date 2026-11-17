# ================================================================
#  УЧЕБНЫЙ ПРОЕКТ: «НЕМЕЦКИЙ СЛОВАРИК» (Deutsch-Woerterbuch)
#  Консольная программа для изучения базовой немецкой лексики.
#  Этот же файл работает и на сайте: браузер импортирует его
#  через Pyodide и вызывает функции из раздела 11.
#  Используются только пройденные темы курса Python.
# ================================================================

# ---------------- 1. ПОДКЛЮЧЕНИЕ БИБЛИОТЕК ----------------
import random      # случайные слова для теста
import csv         # табличные данные: файл .csv для Excel
import os          # проверка, существует ли файл
import json        # обмен данными с сайтом (список ↔ текст)

# ---------------- 2. НАСТРОЙКИ (имена файлов) ----------------
FAJL_TXT = "slovarik.txt"    # основной файл словаря
FAJL_CSV = "slovarik.csv"    # таблица для Excel

# ---------------- 3. БАЗА СЛОВ (таблица = список списков) ----------------
# Одна строка таблицы = список из трёх элементов:
# [немецкое слово, перевод, тема]
# Слова записаны маленькими буквами — так проще сравнивать ответы.
bazovye_slova = [
    # Тема 1. Животные (Tiere)
    ["der hund", "собака", "Животные"],
    ["die katze", "кошка", "Животные"],
    ["der vogel", "птица", "Животные"],
    ["der fisch", "рыба", "Животные"],
    ["das pferd", "лошадь", "Животные"],
    ["die kuh", "корова", "Животные"],
    ["das schwein", "свинья", "Животные"],
    ["das schaf", "овца", "Животные"],
    ["der hase", "заяц", "Животные"],
    ["der bär", "медведь", "Животные"],
    ["der wolf", "волк", "Животные"],
    ["der fuchs", "лиса", "Животные"],
    ["die maus", "мышь", "Животные"],
    ["der löwe", "лев", "Животные"],
    ["der tiger", "тигр", "Животные"],
    ["der elefant", "слон", "Животные"],
    ["die ente", "утка", "Животные"],
    ["das huhn", "курица", "Животные"],
    ["der hahn", "петух", "Животные"],
    ["die ziege", "коза", "Животные"],
    ["das kamel", "верблюд", "Животные"],
    ["die schlange", "змея", "Животные"],
    ["der affe", "обезьяна", "Животные"],
    ["der hirsch", "олень", "Животные"],
    ["das reh", "косуля", "Животные"],
    ["der igel", "ёж", "Животные"],
    ["die biene", "пчела", "Животные"],
    ["der schmetterling", "бабочка", "Животные"],
    ["die spinne", "паук", "Животные"],
    # Тема 2. Еда и напитки (Essen und Trinken)
    ["das brot", "хлеб", "Еда и напитки"],
    ["die milch", "молоко", "Еда и напитки"],
    ["das wasser", "вода", "Еда и напитки"],
    ["der käse", "сыр", "Еда и напитки"],
    ["der apfel", "яблоко", "Еда и напитки"],
    ["die banane", "банан", "Еда и напитки"],
    ["das fleisch", "мясо", "Еда и напитки"],
    ["die kartoffel", "картофель", "Еда и напитки"],
    ["der reis", "рис", "Еда и напитки"],
    ["der kaffee", "кофе", "Еда и напитки"],
    ["der tee", "чай", "Еда и напитки"],
    ["der zucker", "сахар", "Еда и напитки"],
    ["das ei", "яйцо", "Еда и напитки"],
    ["die suppe", "суп", "Еда и напитки"],
    ["der salat", "салат", "Еда и напитки"],
    ["das gemüse", "овощи", "Еда и напитки"],
    ["das obst", "фрукты", "Еда и напитки"],
    ["die tomate", "помидор", "Еда и напитки"],
    ["die gurke", "огурец", "Еда и напитки"],
    ["die wurst", "колбаса", "Еда и напитки"],
    ["der schinken", "ветчина", "Еда и напитки"],
    ["das hähnchen", "курица (блюдо)", "Еда и напитки"],
    ["der fisch", "рыба", "Еда и напитки"],
    ["der kuchen", "торт, пирог", "Еда и напитки"],
    ["die schokolade", "шоколад", "Еда и напитки"],
    ["das eis", "мороженое", "Еда и напитки"],
    ["der saft", "сок", "Еда и напитки"],
    ["das salz", "соль", "Еда и напитки"],
    ["der pfeffer", "перец", "Еда и напитки"],
    ["die butter", "масло", "Еда и напитки"],
    # Тема 3. Семья (Familie)
    ["die mutter", "мать", "Семья"],
    ["der vater", "отец", "Семья"],
    ["der bruder", "брат", "Семья"],
    ["die schwester", "сестра", "Семья"],
    ["die großmutter", "бабушка", "Семья"],
    ["der großvater", "дедушка", "Семья"],
    ["der sohn", "сын", "Семья"],
    ["die tochter", "дочь", "Семья"],
    ["die familie", "семья", "Семья"],
    ["das kind", "ребёнок", "Семья"],
    ["die eltern", "родители", "Семья"],
    ["die geschwister", "братья и сёстры", "Семья"],
    ["der onkel", "дядя", "Семья"],
    ["die tante", "тётя", "Семья"],
    ["der cousin", "кузен (двоюродный брат)", "Семья"],
    ["die cousine", "кузина (двоюродная сестра)", "Семья"],
    ["der enkel", "внук", "Семья"],
    ["die enkelin", "внучка", "Семья"],
    ["der mann", "муж, мужчина", "Семья"],
    ["die frau", "жена, женщина", "Семья"],
    ["das baby", "младенец", "Семья"],
    ["der junge", "мальчик", "Семья"],
    ["das mädchen", "девочка", "Семья"],
    ["der freund", "друг", "Семья"],
    ["die freundin", "подруга", "Семья"],
    ["der nachbar", "сосед", "Семья"],
    ["die hochzeit", "свадьба", "Семья"],
    # Тема 4. Тело и здоровье (Koerper und Gesundheit)
    ["der kopf", "голова", "Тело и здоровье"],
    ["die hand", "рука (кисть)", "Тело и здоровье"],
    ["das auge", "глаз", "Тело и здоровье"],
    ["das bein", "нога", "Тело и здоровье"],
    ["der mund", "рот", "Тело и здоровье"],
    ["das herz", "сердце", "Тело и здоровье"],
    ["der zahn", "зуб", "Тело и здоровье"],
    ["das haar", "волос(ы)", "Тело и здоровье"],
    ["der fuß", "стопа", "Тело и здоровье"],
    ["der körper", "тело", "Тело и здоровье"],
    ["der arm", "рука (плечо до кисти)", "Тело и здоровье"],
    ["das ohr", "ухо", "Тело и здоровье"],
    ["die nase", "нос", "Тело и здоровье"],
    ["der finger", "палец руки", "Тело и здоровье"],
    ["der rücken", "спина", "Тело и здоровье"],
    ["der bauch", "живот", "Тело и здоровье"],
    ["das gesicht", "лицо", "Тело и здоровье"],
    ["die stirn", "лоб", "Тело и здоровье"],
    ["die schulter", "плечо", "Тело и здоровье"],
    ["das knie", "колено", "Тело и здоровье"],
    ["der arzt", "врач", "Тело и здоровье"],
    ["das fieber", "температура, жар", "Тело и здоровье"],
    ["der husten", "кашель", "Тело и здоровье"],
    ["die erkältung", "простуда", "Тело и здоровье"],
    ["die schmerzen", "боли", "Тело и здоровье"],
    ["gesund", "здоровый", "Тело и здоровье"],
    ["krank", "больной", "Тело и здоровье"],
    ["die tablette", "таблетка", "Тело и здоровье"],
    ["die apotheke", "аптека", "Тело и здоровье"],
    ["das krankenhaus", "больница", "Тело и здоровье"],
    # Тема 5. Одежда (Kleidung)
    ["das hemd", "рубашка", "Одежда"],
    ["die hose", "брюки", "Одежда"],
    ["das kleid", "платье", "Одежда"],
    ["die jacke", "куртка", "Одежда"],
    ["der schuh", "ботинок", "Одежда"],
    ["die mütze", "шапка", "Одежда"],
    ["der mantel", "пальто", "Одежда"],
    ["die bluse", "блузка", "Одежда"],
    ["der pullover", "свитер", "Одежда"],
    ["die socke", "носок", "Одежда"],
    ["das t-shirt", "футболка", "Одежда"],
    ["der rock", "юбка", "Одежда"],
    ["die jeans", "джинсы", "Одежда"],
    ["die shorts", "шорты", "Одежда"],
    ["die handschuhe", "перчатки", "Одежда"],
    ["der schal", "шарф", "Одежда"],
    ["die stiefel", "сапоги", "Одежда"],
    ["die sandale", "сандалия", "Одежда"],
    ["der gürtel", "ремень", "Одежда"],
    ["die brille", "очки", "Одежда"],
    ["der hut", "шляпа", "Одежда"],
    ["das kostüm", "костюм", "Одежда"],
    ["der anzug", "костюм (мужской)", "Одежда"],
    ["der ring", "кольцо", "Одежда"],
    ["die tasche", "сумка", "Одежда"],
    ["der regenschirm", "зонт", "Одежда"],
    ["die unterhose", "трусы, нижнее бельё", "Одежда"],
    # Тема 6. Дом и квартира (Haus und Wohnung)
    ["das haus", "дом", "Дом и квартира"],
    ["die tür", "дверь", "Дом и квартира"],
    ["das fenster", "окно", "Дом и квартира"],
    ["die wand", "стена", "Дом и квартира"],
    ["der tisch", "стол", "Дом и квартира"],
    ["der stuhl", "стул", "Дом и квартира"],
    ["das bett", "кровать", "Дом и квартира"],
    ["die lampe", "лампа", "Дом и квартира"],
    ["der teppich", "ковёр", "Дом и квартира"],
    ["die küche", "кухня", "Дом и квартира"],
    ["das bad", "ванная", "Дом и квартира"],
    ["das zimmer", "комната", "Дом и квартира"],
    ["das wohnzimmer", "гостиная", "Дом и квартира"],
    ["das schlafzimmer", "спальня", "Дом и квартира"],
    ["der balkon", "балкон", "Дом и квартира"],
    ["die treppe", "лестница", "Дом и квартира"],
    ["der aufzug", "лифт", "Дом и квартира"],
    ["der schlüssel", "ключ", "Дом и квартира"],
    ["die möbel", "мебель", "Дом и квартира"],
    ["der schrank", "шкаф", "Дом и квартира"],
    ["das regal", "полка, стеллаж", "Дом и квартира"],
    ["der spiegel", "зеркало", "Дом и квартира"],
    ["der kühlschrank", "холодильник", "Дом и квартира"],
    ["der ofen", "печь, плита", "Дом и квартира"],
    ["die dusche", "душ", "Дом и квартира"],
    ["die toilette", "туалет", "Дом и квартира"],
    ["der garten", "сад", "Дом и квартира"],
    ["das stockwerk", "этаж", "Дом и квартира"],
    ["die miete", "аренда, квартплата", "Дом и квартира"],
    ["umziehen", "переезжать", "Дом и квартира"],
    # Тема 7. Школа и образование (Schule und Bildung)
    ["die schule", "школа", "Школа и образование"],
    ["der lehrer", "учитель", "Школа и образование"],
    ["der schüler", "ученик", "Школа и образование"],
    ["das buch", "книга", "Школа и образование"],
    ["der stift", "карандаш, ручка", "Школа и образование"],
    ["das heft", "тетрадь", "Школа и образование"],
    ["die tafel", "доска", "Школа и образование"],
    ["das lineal", "линейка", "Школа и образование"],
    ["die aufgabe", "задание", "Школа и образование"],
    ["das wort", "слово", "Школа и образование"],
    ["die universität", "университет", "Школа и образование"],
    ["der student", "студент", "Школа и образование"],
    ["die klasse", "класс", "Школа и образование"],
    ["die stunde", "урок, час", "Школа и образование"],
    ["die pause", "перемена", "Школа и образование"],
    ["das fach", "предмет", "Школа и образование"],
    ["die mathematik", "математика", "Школа и образование"],
    ["die geschichte", "история", "Школа и образование"],
    ["die physik", "физика", "Школа и образование"],
    ["die chemie", "химия", "Школа и образование"],
    ["die biologie", "биология", "Школа и образование"],
    ["die prüfung", "экзамен", "Школа и образование"],
    ["die note", "оценка", "Школа и образование"],
    ["die hausaufgabe", "домашнее задание", "Школа и образование"],
    ["das papier", "бумага", "Школа и образование"],
    ["der radiergummi", "ластик", "Школа и образование"],
    ["die zeitschrift", "журнал", "Школа и образование"],
    ["die bibliothek", "библиотека", "Школа и образование"],
    ["lernen", "учиться, учить", "Школа и образование"],
    ["verstehen", "понимать", "Школа и образование"],
    # Тема 8. Природа и погода (Natur und Wetter)
    ["die sonne", "солнце", "Природа и погода"],
    ["der mond", "луна", "Природа и погода"],
    ["der stern", "звезда", "Природа и погода"],
    ["der baum", "дерево", "Природа и погода"],
    ["die blume", "цветок", "Природа и погода"],
    ["der berg", "гора", "Природа и погода"],
    ["das meer", "море", "Природа и погода"],
    ["der fluss", "река", "Природа и погода"],
    ["der regen", "дождь", "Природа и погода"],
    ["der schnee", "снег", "Природа и погода"],
    ["der wind", "ветер", "Природа и погода"],
    ["die wolke", "облако", "Природа и погода"],
    ["der wald", "лес", "Природа и погода"],
    ["die wiese", "луг", "Природа и погода"],
    ["der see", "озеро", "Природа и погода"],
    ["der himmel", "небо", "Природа и погода"],
    ["die erde", "земля", "Природа и погода"],
    ["der strand", "пляж", "Природа и погода"],
    ["die insel", "остров", "Природа и погода"],
    ["das feuer", "огонь", "Природа и погода"],
    ["das eis", "лёд", "Природа и погода"],
    ["der sturm", "буря, шторм", "Природа и погода"],
    ["das gewitter", "гроза", "Природа и погода"],
    ["der nebel", "туман", "Природа и погода"],
    ["der regenbogen", "радуга", "Природа и погода"],
    ["die temperatur", "температура", "Природа и погода"],
    ["der sommer", "лето", "Природа и погода"],
    ["der winter", "зима", "Природа и погода"],
    ["der frühling", "весна", "Природа и погода"],
    ["der herbst", "осень", "Природа и погода"],
    # Тема 9. Профессии (Berufe)
    ["der arzt", "врач", "Профессии"],
    ["der lehrer", "учитель", "Профессии"],
    ["der koch", "повар", "Профессии"],
    ["der polizist", "полицейский", "Профессии"],
    ["der fahrer", "водитель", "Профессии"],
    ["der ingenieur", "инженер", "Профессии"],
    ["der verkäufer", "продавец", "Профессии"],
    ["der künstler", "художник", "Профессии"],
    ["der sänger", "певец", "Профессии"],
    ["der schriftsteller", "писатель", "Профессии"],
    ["die ärztin", "врач (женщина)", "Профессии"],
    ["die lehrerin", "учительница", "Профессии"],
    ["der anwalt", "юрист, адвокат", "Профессии"],
    ["der friseur", "парикмахер", "Профессии"],
    ["die krankenschwester", "медсестра", "Профессии"],
    ["der feuerwehrmann", "пожарный", "Профессии"],
    ["der bauer", "фермер", "Профессии"],
    ["der mechaniker", "механик", "Профессии"],
    ["der journalist", "журналист", "Профессии"],
    ["der fotograf", "фотограф", "Профессии"],
    ["der pilot", "пилот", "Профессии"],
    ["die sekretärin", "секретарь", "Профессии"],
    ["der postbote", "почтальон", "Профессии"],
    ["der programmierer", "программист", "Профессии"],
    ["der musiker", "музыкант", "Профессии"],
    ["der zahnarzt", "стоматолог", "Профессии"],
    ["der übersetzer", "переводчик", "Профессии"],
    ["die arbeit", "работа", "Профессии"],
    ["der beruf", "профессия", "Профессии"],
    ["das gehalt", "зарплата", "Профессии"],
    # Тема 10. Путешествия и транспорт (Reise und Transport)
    ["das auto", "машина", "Путешествия и транспорт"],
    ["der zug", "поезд", "Путешествия и транспорт"],
    ["das flugzeug", "самолёт", "Путешествия и транспорт"],
    ["das schiff", "корабль", "Путешествия и транспорт"],
    ["das fahrrad", "велосипед", "Путешествия и транспорт"],
    ["der bus", "автобус", "Путешествия и транспорт"],
    ["die straße", "улица", "Путешествия и транспорт"],
    ["die reise", "путешествие", "Путешествия и транспорт"],
    ["der bahnhof", "вокзал", "Путешествия и транспорт"],
    ["der flughafen", "аэропорт", "Путешествия и транспорт"],
    ["das ticket", "билет", "Путешествия и транспорт"],
    ["die stadt", "город", "Путешествия и транспорт"],
    ["das motorrad", "мотоцикл", "Путешествия и транспорт"],
    ["die u-bahn", "метро", "Путешествия и транспорт"],
    ["das taxi", "такси", "Путешествия и транспорт"],
    ["die fahrkarte", "проездной билет", "Путешествия и транспорт"],
    ["die grenze", "граница", "Путешествия и транспорт"],
    ["der pass", "паспорт", "Путешествия и транспорт"],
    ["der koffer", "чемодан", "Путешествия и транспорт"],
    ["das hotel", "отель", "Путешествия и транспорт"],
    ["die jugendherberge", "хостел", "Путешествия и транспорт"],
    ["die karte", "карта", "Путешествия и транспорт"],
    ["der weg", "путь, дорога", "Путешествия и транспорт"],
    ["die brücke", "мост", "Путешествия и транспорт"],
    ["reisen", "путешествовать", "Путешествия и транспорт"],
    ["abfahren", "отправляться, уезжать", "Путешествия и транспорт"],
    ["ankommen", "прибывать", "Путешествия и транспорт"],
    ["der urlaub", "отпуск, каникулы", "Путешествия и транспорт"],
    ["das ausland", "зарубежье", "Путешествия и транспорт"],
    ["die fahrtrichtung", "направление движения", "Путешествия и транспорт"],
    # Тема 11. Цвета (Farben)
    ["rot", "красный", "Цвета"],
    ["blau", "синий", "Цвета"],
    ["grün", "зелёный", "Цвета"],
    ["gelb", "жёлтый", "Цвета"],
    ["schwarz", "чёрный", "Цвета"],
    ["weiß", "белый", "Цвета"],
    ["braun", "коричневый", "Цвета"],
    ["grau", "серый", "Цвета"],
    ["orange", "оранжевый", "Цвета"],
    ["rosa", "розовый", "Цвета"],
    ["lila", "фиолетовый", "Цвета"],
    ["gold", "золотой", "Цвета"],
    ["silbern", "серебряный", "Цвета"],
    ["hellblau", "светло-голубой", "Цвета"],
    ["dunkelgrün", "тёмно-зелёный", "Цвета"],
    ["hell", "светлый", "Цвета"],
    ["dunkel", "тёмный", "Цвета"],
    ["bunt", "разноцветный", "Цвета"],
    ["die farbe", "цвет, краска", "Цвета"],
    ["der farbton", "оттенок", "Цвета"],
    # Тема 12. Время и дни недели (Zeit und Wochentage)
    ["der montag", "понедельник", "Время и дни недели"],
    ["der dienstag", "вторник", "Время и дни недели"],
    ["der mittwoch", "среда", "Время и дни недели"],
    ["der donnerstag", "четверг", "Время и дни недели"],
    ["der freitag", "пятница", "Время и дни недели"],
    ["der samstag", "суббота", "Время и дни недели"],
    ["der sonntag", "воскресенье", "Время и дни недели"],
    ["der morgen", "утро", "Время и дни недели"],
    ["der abend", "вечер", "Время и дни недели"],
    ["die nacht", "ночь", "Время и дни недели"],
    ["die stunde", "час", "Время и дни недели"],
    ["die minute", "минута", "Время и дни недели"],
    ["die sekunde", "секунда", "Время и дни недели"],
    ["der tag", "день", "Время и дни недели"],
    ["die woche", "неделя", "Время и дни недели"],
    ["der monat", "месяц", "Время и дни недели"],
    ["das jahr", "год", "Время и дни недели"],
    ["das frühjahr", "весна (начало года)", "Время и дни недели"],
    ["die uhr", "часы", "Время и дни недели"],
    ["der moment", "момент", "Время и дни недели"],
    ["heute", "сегодня", "Время и дни недели"],
    ["morgen", "завтра", "Время и дни недели"],
    ["gestern", "вчера", "Время и дни недели"],
    ["jetzt", "сейчас", "Время и дни недели"],
    ["immer", "всегда", "Время и дни недели"],
    ["nie", "никогда", "Время и дни недели"],
    ["oft", "часто", "Время и дни недели"],
    ["manchmal", "иногда", "Время и дни недели"],
    ["der winter", "зима", "Время и дни недели"],
    ["die jahreszeit", "время года", "Время и дни недели"],
    # Тема 13. Эмоции и качества (Gefuehle und Eigenschaften)
    ["glücklich", "счастливый", "Эмоции и качества"],
    ["traurig", "грустный", "Эмоции и качества"],
    ["müde", "усталый", "Эмоции и качества"],
    ["wütend", "злой", "Эмоции и качества"],
    ["lustig", "весёлый", "Эмоции и качества"],
    ["groß", "большой", "Эмоции и качества"],
    ["klein", "маленький", "Эмоции и качества"],
    ["schön", "красивый", "Эмоции и качества"],
    ["neu", "новый", "Эмоции и качества"],
    ["alt", "старый", "Эмоции и качества"],
    ["gut", "хороший", "Эмоции и качества"],
    ["schlecht", "плохой", "Эмоции и качества"],
    ["freundlich", "дружелюбный", "Эмоции и качества"],
    ["höflich", "вежливый", "Эмоции и качества"],
    ["ehrlich", "честный", "Эмоции и качества"],
    ["stark", "сильный", "Эмоции и качества"],
    ["schwach", "слабый", "Эмоции и качества"],
    ["klug", "умный", "Эмоции и качества"],
    ["dumm", "глупый", "Эмоции и качества"],
    ["langsam", "медленный", "Эмоции и качества"],
    ["schnell", "быстрый", "Эмоции и качества"],
    ["die angst", "страх", "Эмоции и качества"],
    ["die freude", "радость", "Эмоции и качества"],
    ["die hoffnung", "надежда", "Эмоции и качества"],
    ["die liebe", "любовь", "Эмоции и качества"],
    ["der ärger", "досада, раздражение", "Эмоции и качества"],
    ["die überraschung", "удивление", "Эмоции и качества"],
    ["sich freuen", "радоваться", "Эмоции и качества"],
    ["weinen", "плакать", "Эмоции и качества"],
    ["lachen", "смеяться", "Эмоции и качества"],
]

slovar = []   # рабочий словарь: заполняется при запуске программы или сайта


# ---------------- 4. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------------
# def — объявление функции, в скобках параметры, return — результат.

def norm(tekst):
    """Приводит текст к единому виду: без лишних пробелов, с маленькой буквы."""
    tekst = tekst.strip()             # убрать пробелы по краям
    tekst = tekst.lower()             # все буквы маленькие
    tekst = " ".join(tekst.split())   # лишние пробелы внутри заменить одним
    return tekst


def est_artikul(slovo):
    """True, если слово начинается с артикля der, die или das."""
    return slovo.startswith("der ") or slovo.startswith("die ") or slovo.startswith("das ")


def najti_indeks(slovo):
    """Ищет немецкое слово. Возвращает номер строки или -1 (не найдено)."""
    for i in range(len(slovar)):      # перебор номеров строк таблицы
        if slovar[i][0] == slovo:     # [i][0] — строка i, столбец 0
            return i
    return -1


def spisok_tem():
    """Список тем по алфавиту, без повторов."""
    temy = set()                      # множество хранит только уникальные значения
    for stroka in slovar:
        temy.add(stroka[2])           # .add — добавить в множество
    return sorted(temy)               # sorted — сортировка, результат список


def vibrat_temu():
    """Показывает темы и просит выбрать номер. Enter — все темы."""
    temy = spisok_tem()
    if len(temy) == 0:
        return ""
    print("\nТемы словаря:")
    for i in range(len(temy)):
        print(" ", i + 1, "—", temy[i])
    while True:                       # повторяем, пока ввод не будет правильным
        otvet = input("Номер темы (Enter — все темы): ").strip()
        if otvet == "":
            return ""
        if otvet.isdigit() and 1 <= int(otvet) <= len(temy):
            return temy[int(otvet) - 1]   # int() — строку в число
        print("Ошибка: введи номер из списка или нажми Enter.")


def otbor_po_teme(tema):
    """Новая таблица только с выбранной темой (или вся, если tema = '')."""
    rezultat = []
    for stroka in slovar:
        if tema == "" or stroka[2] == tema:
            rezultat.append(stroka)   # append — добавить в конец списка
    return rezultat


def sprosit_chislo(vopros, minimum, maksimum):
    """Просит целое число в диапазоне. Не даёт ввести ерунду."""
    while True:
        otvet = input(vopros).strip()
        if otvet.isdigit():           # isdigit — в строке только цифры?
            n = int(otvet)
            if minimum <= n <= maksimum:
                return n
        print("Нужно ввести число от", minimum, "до", maksimum)


def proverit(otvet, etalon):
    """Сравнивает ответ с эталоном. Возвращает True или False."""
    # «е/ё» и «ß/ss» не считаем ошибкой
    otvet = otvet.replace("ё", "е").replace("ß", "ss")
    etalon = etalon.replace("ё", "е").replace("ß", "ss")
    if otvet == etalon:
        return True
    for variant in etalon.split(","):     # "торт, пирог" — два верных варианта
        if otvet == norm(variant):
            return True
    if est_artikul(etalon) and otvet == etalon[4:]:   # ответ без артикля тоже верный
        return True
    return False


def otsenka(procent):
    """Переводит процент правильных ответов в оценку."""
    if procent >= 90:
        return "отлично (5)"
    elif procent >= 75:
        return "хорошо (4)"
    elif procent >= 50:
        return "удовлетворительно (3)"
    else:
        return "нужно повторить (2)"


# ---------------- 5. РАБОТА С ФАЙЛАМИ ----------------

def sohranit():
    """Записывает словарь в текстовый файл: слово|перевод|тема."""
    f = open(FAJL_TXT, "w", encoding="utf-8")   # "w" — запись
    for stroka in slovar:
        f.write(stroka[0] + "|" + stroka[1] + "|" + stroka[2] + "\n")
    f.close()                                   # файл обязательно закрываем
    print("Сохранено записей:", len(slovar), "→ файл", FAJL_TXT)


def zagruzit():
    """Читает словарь из текстового файла обратно в список."""
    if not os.path.exists(FAJL_TXT):   # exists — существует ли файл
        print("Файл", FAJL_TXT, "не найден.")
        return
    f = open(FAJL_TXT, "r", encoding="utf-8")   # "r" — чтение
    stroki = f.readlines()                      # список всех строк файла
    f.close()
    slovar.clear()                              # очищаем текущий словарь
    for stroka in stroki:
        stroka = stroka.strip()                 # убираем перенос строки
        if stroka == "":
            continue                            # continue — пропустить шаг цикла
        chasti = stroka.split("|")              # режем строку по разделителю
        if len(chasti) == 3:
            slovar.append([norm(chasti[0]), norm(chasti[1]), chasti[2].strip()])
    print("Загружено записей:", len(slovar))


def export_csv():
    """Выгружает таблицу в .csv — открывается в Excel."""
    f = open(FAJL_CSV, "w", encoding="utf-8-sig", newline="")
    tablitsa = csv.writer(f, delimiter=";")     # ; — чтобы Excel делал столбцы
    tablitsa.writerow(["Немецкое слово", "Перевод", "Тема"])   # шапка
    for stroka in slovar:
        tablitsa.writerow(stroka)
    f.close()
    print("Таблица для Excel сохранена:", FAJL_CSV)


# ---------------- 6. ПРОСМОТР СЛОВАРЯ ----------------

def pechat_tablitsy(spisok):
    """Печатает список слов ровными столбцами."""
    if len(spisok) == 0:
        print("Слов не найдено.")
        return
    print("-" * 74)                             # строка * число = повтор символа
    # {:<24} — поле шириной 24 символа, выравнивание влево
    print(f"{'№':<5}{'Немецкое слово':<24}{'Перевод':<26}{'Тема'}")
    print("-" * 74)
    for i in range(len(spisok)):
        s = spisok[i]
        print(f"{i + 1:<5}{s[0]:<24}{s[1]:<26}{s[2]}")
    print("-" * 74)
    print("Всего записей:", len(spisok))


def pokazat_slova():
    """Пункт 1: все слова или слова одной темы."""
    tema = vibrat_temu()
    pechat_tablitsy(otbor_po_teme(tema))


def poisk():
    """Пункт 8: поиск по части слова или перевода."""
    chast = norm(input("Введи слово или его часть: "))
    if chast == "":
        print("Пустой запрос.")
        return
    rezultat = []
    for stroka in slovar:
        if chast in stroka[0] or chast in stroka[1]:   # in — «содержится внутри»
            rezultat.append(stroka)
    pechat_tablitsy(rezultat)


# ---------------- 7. ИЗМЕНЕНИЕ СЛОВАРЯ ----------------

def dobavit():
    """Пункт 5: добавить новое слово."""
    slovo = norm(input("Немецкое слово: "))
    perevod = norm(input("Перевод: "))
    if slovo == "" or perevod == "":
        print("Слово и перевод не могут быть пустыми.")
        return
    if najti_indeks(slovo) != -1:
        print("Такое слово уже есть в словаре.")
        return
    print("Выбери тему для нового слова:")
    tema = vibrat_temu()
    if tema == "":
        tema = "Мои слова"
    slovar.append([slovo, perevod, tema])
    print("Добавлено:", slovo, "—", perevod, "(", tema, ")")
    sohranit()


def udalit():
    """Пункт 6: удалить слово."""
    slovo = norm(input("Какое немецкое слово удалить? "))
    i = najti_indeks(slovo)
    if i == -1:
        print("Такого слова нет.")
        return
    print("Найдено:", slovar[i][0], "—", slovar[i][1])
    otvet = norm(input("Точно удалить? (да/нет): "))
    if otvet == "да":
        slovar.pop(i)                   # pop(i) — удалить элемент по номеру
        print("Удалено.")
        sohranit()
    else:
        print("Удаление отменено.")


def redaktirovat():
    """Пункт 7: исправить слово или перевод."""
    slovo = norm(input("Какое слово исправить? "))
    i = najti_indeks(slovo)
    if i == -1:
        print("Такого слова нет.")
        return
    print("Сейчас:", slovar[i][0], "—", slovar[i][1], "|", slovar[i][2])
    novoe_slovo = norm(input("Новое немецкое слово (Enter — оставить): "))
    novyj_perevod = norm(input("Новый перевод (Enter — оставить): "))
    if novoe_slovo != "":
        slovar[i][0] = novoe_slovo      # запись нового значения в ячейку таблицы
    if novyj_perevod != "":
        slovar[i][1] = novyj_perevod
    print("Теперь:", slovar[i][0], "—", slovar[i][1])
    sohranit()


# ---------------- 8. ТЕСТЫ ----------------

def mini_test(napravlenie):
    """Тест на перевод: 1 — нем→рус, 2 — рус→нем."""
    tema = vibrat_temu()
    spisok = otbor_po_teme(tema)
    if len(spisok) == 0:
        print("Нет слов для теста.")
        return
    kolichestvo = sprosit_chislo("Сколько вопросов? (1-" + str(len(spisok)) + "): ", 1, len(spisok))
    voprosy = random.sample(spisok, kolichestvo)   # случайные слова без повторов
    pravilno = 0                        # счётчик правильных ответов
    oshibki = []                        # список ошибок
    for i in range(len(voprosy)):
        s = voprosy[i]
        if napravlenie == 1:
            vopros = s[0]
            etalon = s[1]
            print("\nВопрос", i + 1, "из", kolichestvo, "| Переведи на русский:", vopros)
        else:
            vopros = s[1]
            etalon = s[0]
            print("\nВопрос", i + 1, "из", kolichestvo, "| Переведи на немецкий:", vopros)
        otvet = norm(input("Твой ответ: "))
        if proverit(otvet, etalon):
            pravilno = pravilno + 1
            print("Верно!")
        else:
            print("Ошибка. Правильный ответ:", etalon)
            oshibki.append([vopros, etalon, otvet])
    procent = round(pravilno / kolichestvo * 100, 1)   # round — округление
    print("\n" + "=" * 40)
    print("Правильных ответов:", pravilno, "из", kolichestvo)
    print("Результат:", procent, "%   Оценка:", otsenka(procent))
    print("Прогресс: " + "#" * pravilno + "." * (kolichestvo - pravilno))
    if len(oshibki) > 0:
        print("\nПовтори эти слова:")
        for o in oshibki:
            print("  ", o[0], "→", o[1], "(твой ответ:", o[2] + ")")


def test_artikley():
    """Тест: подставить правильный артикль der / die / das."""
    spisok = []
    for stroka in slovar:
        if est_artikul(stroka[0]):
            spisok.append(stroka)
    if len(spisok) == 0:
        print("Нет слов с артиклями.")
        return
    kolichestvo = sprosit_chislo("Сколько вопросов? (1-" + str(len(spisok)) + "): ", 1, len(spisok))
    voprosy = random.sample(spisok, kolichestvo)
    pravilno = 0
    for i in range(len(voprosy)):
        s = voprosy[i]
        artikul = s[0][:3]              # срез: первые 3 символа
        slovo_bez = s[0][4:]            # срез: всё после 4-го символа
        print("\n", i + 1, ") ___", slovo_bez, "   (", s[1], ")")
        otvet = norm(input("Артикль (der/die/das): "))
        if otvet == artikul:
            pravilno = pravilno + 1
            print("Верно!")
        else:
            print("Ошибка. Правильно:", artikul, slovo_bez)
    procent = round(pravilno / kolichestvo * 100, 1)
    print("\nПравильных артиклей:", pravilno, "из", kolichestvo, "=", procent, "%")
    print("Оценка:", otsenka(procent))


# ---------------- 9. СТАТИСТИКА ----------------

def statistika():
    """Статистика словаря: числа, множества, таблица по темам."""
    if len(slovar) == 0:
        print("Словарь пуст.")
        return
    unikalnye = set()                   # множество всех немецких слов
    povtory = set()                     # слова, встретившиеся больше одного раза
    for stroka in slovar:
        if stroka[0] in unikalnye:
            povtory.add(stroka[0])
        unikalnye.add(stroka[0])
    temy = spisok_tem()
    summa_dlin = 0
    samoe_dlinnoe = ""
    s_artiklem = 0
    for stroka in slovar:
        dlina = len(stroka[0])          # len строки = количество символов
        summa_dlin = summa_dlin + dlina
        if dlina > len(samoe_dlinnoe):
            samoe_dlinnoe = stroka[0]
        if est_artikul(stroka[0]):
            s_artiklem = s_artiklem + 1
    srednyaya = round(summa_dlin / len(slovar), 2)
    print("\n===== СТАТИСТИКА СЛОВАРЯ =====")
    print("Всего записей:          ", len(slovar))
    print("Уникальных слов:        ", len(unikalnye))
    print("Слов в нескольких темах:", len(povtory))
    print("Количество тем:         ", len(temy))
    print("Существительных с артиклем:", s_artiklem)
    print("Остальных слов:         ", len(slovar) - s_artiklem)
    print("Средняя длина слова:    ", srednyaya, "символов")
    print("Самое длинное слово:    ", samoe_dlinnoe)
    print("\nСлов по темам:")
    print(f"{'Тема':<28}{'Слов':>6}")   # {:>6} — выравнивание вправо
    print("-" * 34)
    for tema in temy:
        k = 0
        for stroka in slovar:
            if stroka[2] == tema:
                k = k + 1
        print(f"{tema:<28}{k:>6}")
    if len(povtory) > 0:
        print("\nСлова в двух темах:", ", ".join(sorted(povtory)))


# ---------------- 10. КОНСОЛЬНОЕ МЕНЮ ----------------

def menu():
    """Печатает пункты меню."""
    print("\n" + "=" * 46)
    print("        НЕМЕЦКИЙ СЛОВАРИК — МЕНЮ")
    print("=" * 46)
    print(" 1  — Показать слова (все или по теме)")
    print(" 2  — Мини-тест: немецкий → русский")
    print(" 3  — Мини-тест: русский → немецкий")
    print(" 4  — Тест на артикли der / die / das")
    print(" 5  — Добавить слово")
    print(" 6  — Удалить слово")
    print(" 7  — Редактировать слово")
    print(" 8  — Поиск слова")
    print(" 9  — Статистика словаря")
    print(" 10 — Сохранить словарь в файл")
    print(" 11 — Загрузить словарь из файла")
    print(" 12 — Экспорт в CSV (таблица для Excel)")
    print(" 0  — Выход")
    print("=" * 46)


def start():
    """Приветствие и загрузка слов при запуске."""
    print("=" * 46)
    print("   ДОБРО ПОЖАЛОВАТЬ В «НЕМЕЦКИЙ СЛОВАРИК»!")
    print("   Учим немецкие слова: 13 тем, тесты, свой словарь")
    print("=" * 46)
    if os.path.exists(FAJL_TXT):
        zagruzit()
    if len(slovar) == 0:
        for stroka in bazovye_slova:
            slovar.append(stroka[:])    # [:] — копия строки таблицы
        print("Создан базовый словарь:", len(slovar), "записей.")
    slovo_dnya = random.choice(slovar)  # choice — один случайный элемент
    print("Слово дня:", slovo_dnya[0], "—", slovo_dnya[1])


def main():
    """Главный цикл меню: работает, пока пользователь не выберет 0."""
    start()
    while True:
        menu()
        punkt = input("Выбери пункт меню: ").strip()
        if punkt == "1":
            pokazat_slova()
        elif punkt == "2":
            mini_test(1)
        elif punkt == "3":
            mini_test(2)
        elif punkt == "4":
            test_artikley()
        elif punkt == "5":
            dobavit()
        elif punkt == "6":
            udalit()
        elif punkt == "7":
            redaktirovat()
        elif punkt == "8":
            poisk()
        elif punkt == "9":
            statistika()
        elif punkt == "10":
            sohranit()
        elif punkt == "11":
            zagruzit()
        elif punkt == "12":
            export_csv()
        elif punkt == "0":
            sohranit()
            print("Словарь сохранён. До свидания! Viel Erfolg!")
            break                       # break — выход из цикла
        else:
            print("Ошибка: такого пункта нет. Введи число от 0 до 12.")
        input("\nНажми Enter, чтобы вернуться в меню...")


# ================================================================
#  РАЗДЕЛ 11. API ДЛЯ САЙТА (мост между Python и браузером)
#  Эти функции ничего не печатают: они ВОЗВРАЩАЮТ данные сайту.
#  json.dumps превращает список в текст, json.loads — обратно.
#  ensure_ascii=False нужен, чтобы русские и немецкие буквы
#  оставались буквами, а не превращались в \u043a.
# ================================================================

def api_start(dannye):
    """Заполняет словарь: из сохранённых данных сайта или из базовой базы."""
    slovar.clear()
    if dannye != "":
        for stroka in json.loads(dannye):   # текст JSON → список списков
            slovar.append(stroka)
    else:
        for stroka in bazovye_slova:
            slovar.append(stroka[:])
    return json.dumps([len(slovar)], ensure_ascii=False)


def api_sohranit():
    """Отдаёт весь словарь сайту для записи в память браузера."""
    return json.dumps(slovar, ensure_ascii=False)


def api_temy():
    """Список тем для выпадающих меню сайта."""
    return json.dumps(spisok_tem(), ensure_ascii=False)


def api_slova(tema, poisk):
    """Строки таблицы с фильтром и поиском: [найдено, всего, строки]."""
    poisk = norm(poisk)
    stroki = []
    for i in range(len(slovar)):
        s = slovar[i]
        if tema != "" and s[2] != tema:
            continue                        # не та тема — пропускаем
        if poisk != "" and poisk not in s[0] and poisk not in s[1]:
            continue                        # подстрока не найдена — пропускаем
        stroki.append([i, s[0], s[1], s[2]])  # i — номер строки в общем словаре
    return json.dumps([len(stroki), len(slovar), stroki], ensure_ascii=False)


def api_slovo_dnya():
    """Одно случайное слово для шапки сайта."""
    s = random.choice(slovar)
    return json.dumps([s[0], s[1]], ensure_ascii=False)


def api_dobavit(slovo, perevod, tema):
    """Добавляет слово: [успех 1/0, сообщение]."""
    slovo = norm(slovo)
    perevod = norm(perevod)
    if slovo == "" or perevod == "":
        return json.dumps([0, "Слово и перевод не могут быть пустыми"], ensure_ascii=False)
    if najti_indeks(slovo) != -1:
        return json.dumps([0, "Такое слово уже есть в словаре"], ensure_ascii=False)
    if tema == "":
        tema = "Мои слова"
    slovar.append([slovo, perevod, tema])
    return json.dumps([1, "Добавлено: " + slovo + " — " + perevod], ensure_ascii=False)


def api_udalit(indeks):
    """Удаляет строку по её номеру."""
    indeks = int(indeks)
    if indeks < 0 or indeks >= len(slovar):
        return json.dumps([0, "Строка не найдена"], ensure_ascii=False)
    slovo = slovar[indeks][0]
    slovar.pop(indeks)
    return json.dumps([1, "Удалено: " + slovo], ensure_ascii=False)


def api_izmenit(indeks, slovo, perevod):
    """Меняет слово и перевод в выбранной строке."""
    indeks = int(indeks)
    slovo = norm(slovo)
    perevod = norm(perevod)
    if indeks < 0 or indeks >= len(slovar):
        return json.dumps([0, "Строка не найдена"], ensure_ascii=False)
    if slovo == "" or perevod == "":
        return json.dumps([0, "Пустые поля — не сохраняю"], ensure_ascii=False)
    slovar[indeks][0] = slovo
    slovar[indeks][1] = perevod
    return json.dumps([1, "Изменено: " + slovo], ensure_ascii=False)


def api_voprosy(rezhim, tema, kolichestvo):
    """Вопросы теста: [сколько, [[вопрос, эталон, подсказка], ...]]."""
    spisok = []
    for s in slovar:
        if tema != "" and s[2] != tema:
            continue
        if rezhim == "artikli" and not est_artikul(s[0]):
            continue                        # для артиклей только существительные
        spisok.append(s)
    if len(spisok) == 0:
        return json.dumps([0, []], ensure_ascii=False)
    kolichestvo = int(kolichestvo)
    if kolichestvo < 1:
        kolichestvo = 1
    if kolichestvo > len(spisok):
        kolichestvo = len(spisok)
    vybrannye = random.sample(spisok, kolichestvo)   # случайные слова без повторов
    voprosy = []
    for s in vybrannye:
        if rezhim == "artikli":
            voprosy.append([s[0][4:], s[0][:3], s[1]])   # слово, артикль, перевод
        elif rezhim == "ru-de":
            voprosy.append([s[1], s[0], "тема: " + s[2]])
        else:
            voprosy.append([s[0], s[1], "тема: " + s[2]])
    return json.dumps([len(voprosy), voprosy], ensure_ascii=False)


def api_proverit(otvet, etalon):
    """Проверяет ответ: [1 — верно / 0 — ошибка, правильный ответ]."""
    otmetka = 0
    if proverit(norm(otvet), etalon):
        otmetka = 1
    return json.dumps([otmetka, etalon], ensure_ascii=False)


def api_itog(pravilno, kolichestvo):
    """Считает процент и оценку: [процент, оценка]."""
    pravilno = int(pravilno)
    kolichestvo = int(kolichestvo)
    procent = round(pravilno / kolichestvo * 100, 1)
    return json.dumps([procent, otsenka(procent)], ensure_ascii=False)


def api_statistika():
    """Статистика: [числа, темы с количеством, повторы]."""
    if len(slovar) == 0:
        return json.dumps([[0, 0, 0, 0, 0, 0, 0, ""], [], ""], ensure_ascii=False)
    unikalnye = set()                       # множество уникальных слов
    povtory = set()                         # слова, встретившиеся дважды
    summa_dlin = 0
    samoe_dlinnoe = ""
    s_artiklem = 0
    for s in slovar:
        if s[0] in unikalnye:
            povtory.add(s[0])
        unikalnye.add(s[0])
        summa_dlin = summa_dlin + len(s[0])
        if len(s[0]) > len(samoe_dlinnoe):
            samoe_dlinnoe = s[0]
        if est_artikul(s[0]):
            s_artiklem = s_artiklem + 1
    temy = spisok_tem()
    srednyaya = round(summa_dlin / len(slovar), 2)
    karta = [len(slovar), len(unikalnye), len(temy), len(povtory),
             s_artiklem, len(slovar) - s_artiklem, srednyaya, samoe_dlinnoe]
    po_temam = []
    for t in temy:
        k = 0
        for s in slovar:
            if s[2] == t:
                k = k + 1
        po_temam.append([t, k])
    return json.dumps([karta, po_temam, ", ".join(sorted(povtory))], ensure_ascii=False)


def api_csv():
    """Текст таблицы CSV (разделитель ; — для Excel)."""
    tekst = "Немецкое слово;Перевод;Тема\n"
    for s in slovar:
        tekst = tekst + s[0] + ";" + s[1] + ";" + s[2] + "\n"
    return json.dumps([tekst], ensure_ascii=False)


def api_txt():
    """Текст файла в формате слово|перевод|тема."""
    tekst = ""
    for s in slovar:
        tekst = tekst + s[0] + "|" + s[1] + "|" + s[2] + "\n"
    return json.dumps([tekst], ensure_ascii=False)


def api_import(tekst):
    """Читает загруженный TXT: [успех, количество, сообщение]."""
    novye = []
    for stroka in tekst.split("\n"):
        stroka = stroka.strip()
        if stroka == "":
            continue
        chasti = stroka.split("|")
        if len(chasti) == 3:
            novye.append([norm(chasti[0]), norm(chasti[1]), chasti[2].strip()])
    if len(novye) == 0:
        return json.dumps([0, 0, "В файле нет строк формата слово|перевод|тема"], ensure_ascii=False)
    slovar.clear()
    for s in novye:
        slovar.append(s)
    return json.dumps([1, len(novye), "Загружено записей: " + str(len(novye))], ensure_ascii=False)


def api_sbros():
    """Возвращает базовый словарь."""
    slovar.clear()
    for s in bazovye_slova:
        slovar.append(s[:])
    return json.dumps([len(slovar)], ensure_ascii=False)


# ================================================================
#  РАЗДЕЛ 12. ТОЧКА ВХОДА
#  Файл запустили напрямую (Jupyter, python slovarik.py) — меню.
#  Файл импортировал сайт — меню не запускается, сайт сам
#  вызывает функции из раздела 11.
# ================================================================
if __name__ == "__main__":
    main()