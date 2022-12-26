# 
1. Завантажити [Chromedriver](https://chromedriver.storage.googleapis.com/index.html). Щоб обрати коректну версію можна взяти ту, яка у вас інстальована на ПК, останні 2-3 цифри після крапки можуть не співпадати. [chrome://settings/help](chrome://settings/help)

2. Задати налаштування
2.1. "download.default_directory" > додати повний шлях до папки, куди потрібно зберігати файли зі згенерованими текстами.
2.2. "executable_path" > посилання на файл Chromedriver
2.3. "list_of_files" > посилання на папку із json файлами структури
2.4. "Serpstat API Key" > ключ API Serpstat

3. Додаткові налаштування
3.1. "options.add_argument("--headless")" — чи буде працювати Selenium у фоновому режимі. Закоментуй якщо хочеш бачити вікна. Включи якщо хочеш економити ресурс
3.2. "driver.implicitly_wait(120) # seconds" — задай час стандартного очікування появи елементів.
3.3. "p = Pool(processes=3)" — к-сть потоків.