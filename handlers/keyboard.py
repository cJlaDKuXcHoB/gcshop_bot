from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bck= KeyboardButton("Главное Меню")


mainmenu_kypc1 = KeyboardButton("Курс Юаня💹")
mainmenu_kypc2 = KeyboardButton("Курс Доллара💲")
mainmenu_zakaz = KeyboardButton("Рассчитать стоимость заказа💸")
kat_men = KeyboardButton('Каталог Товаров')

mainmenu = ReplyKeyboardMarkup(resize_keyboard=True).add(mainmenu_kypc1, mainmenu_kypc2, mainmenu_zakaz, kat_men)



zakaz_k1 = KeyboardButton("Обувь👟")
zakaz_k2 = KeyboardButton("Прочее")
zakaz_k3 = KeyboardButton("Одежда")
zakaz_k4= KeyboardButton("Аксессуар")

zakazmenu = ReplyKeyboardMarkup(resize_keyboard=True).add(zakaz_k1, zakaz_k2, zakaz_k3, zakaz_k4, bck)





adm_1 = KeyboardButton("Рассылка")
adm_2 = KeyboardButton('Курс юсд')
adm_3 = KeyboardButton('курс юаня')

adminmenu = ReplyKeyboardMarkup(resize_keyboard=True).add(adm_1, adm_2, adm_3, bck)




sel_1 = KeyboardButton("Бренд")
sel_2 = KeyboardButton("Формат")
sel_3 = KeyboardButton("Обувь")
selmenu = ReplyKeyboardMarkup(resize_keyboard=True).add(sel_1, sel_2, sel_3, bck)



brnd_1 = KeyboardButton("Nike")
brnd_2 = KeyboardButton("Bape")
brnd_3 = KeyboardButton("Adidas")
brnd_4 = KeyboardButton("Jordan")
brnd_5 = KeyboardButton("DC shoes")
brnd_6 = KeyboardButton("MLB New Era")
brnd_7 = KeyboardButton("ollieskate")

brndmenu = ReplyKeyboardMarkup(resize_keyboard=True).add(brnd_1, brnd_2, brnd_3, brnd_4, brnd_5, brnd_6, brnd_7, bck)

clthh_1= KeyboardButton("Верх")
clthh_2= KeyboardButton("Низ")

clthhmenu = ReplyKeyboardMarkup(resize_keyboard=True).add(clthh_1, clthh_2, bck)

shoes1= KeyboardButton("Кеды/Кроссовки")
shoes2= KeyboardButton("Тапки")
shoes3= KeyboardButton("Спортивные")

shoesmenu=ReplyKeyboardMarkup(resize_keyboard=True).add(shoes1,shoes2,shoes3,bck)