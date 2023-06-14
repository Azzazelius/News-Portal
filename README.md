English version.

                                                    Graduation work: News portal

                                                        Development stack:
- Python 3.8
  - IDE: PYcharm,
- pSQL database
  - Dbeaver for SQL query
- Redis
- Celery
- HTML
- CSS


                                                            Functional:
- The site is running on a local server

**Users**
- Available simple registration and through a google account
- Configured access levels. 
  - Part of the functionality is available only to registered users
  - Another part is limited to the “authors” group

**News**
- The main page displays news from the database.
     - Pagination works
- The filter censoring Russian “curses”. 
See file custom_filters.py
- You can open the full text, where you can edit and delete news.
- You can add news in the following ways:
   - On the site through the Create page, where you can edit the news
     	- Only available to registered users from the authors group.
   - Through the site admin panel, login admin, password admin, (never tell anyone your password)
   - In the file ** command_file.py ** set to fill through the terminal of filling tables.

**Subscription**
- There are several types of mailing lists:
     - Newsletter once a week comes a selection of new articles from selected subscription categories.
     - When there are new posts from these categories.
     - Upon registration, you will receive a welcome email.
     - Newsletters work only in test mode. EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


                                                            In development::
- Functional like / dislike and  leave comments
  - Already implemented in the database, but not on the site.
- News list caching.
- Delete the second type of posts. “articles” (**Article**) - extra entity


                                                             Known Bugs:
- Unauthorized user is shown buttons for editing the news, but when pressed, an error occurs
- Search by title does not work.
- In the search, categories are selected only with ctrl pressed, should be by a simple click
- Both registration options are signed “Sign UP with social Account”. It is necessary to change the inscription or separate the registration on different pages.
- Layout not configured



<hr>            
Russian version

                                                  
                                                  Учебная работа: новостной портал

                                                        Что использовалось:
- База данных на SQLite. (файл db.sqlite3)
  - Для SQL запросов использовался Dbeaver.
- Сайт сделан на Django
- Redis и Celery использовались для рассылки 
- HTML, CSS
- IDE PyCharm

                                                        Доступный функционал
- Сайт работает на локальном сервере

Пользователи 
 - Доступна простая регистрация и через аккаунт google
 - Настроены уровни доступа. Часть функционала доступна только зарегистрированным пользователям
    - Ещё часть ограничена группой “authors”
  
Новости
- На главной странице выводятся новости из БД. 
    - Работает пагинация
- Работает фильтр цензурующий ругательства из фильма Джентльмены удачи.
- Можно открыть полный текст, где можно редактировать и удалять новости.
- Добавлять новости можно такими способами:
  - На сайте через страницу Create, там же можно редактировать новость
    - Доступно только для зарегистрированных пользователей из группы authors.
  - Через админку сайта, логин admin, пароль admin, (никогда никому не сообщайте свой пароль)
  - В файле** command_file.py** набор для заполнения через терминал заполнения таблиц.

Рассылка
- Есть несколько видов рассылок:
    - Рассылка раз в неделю приходит подборка новых статей из выбранных категорий подписки.
    - Когда появляются новые постов из этих категорий.
    - При регистрации приходит письмо с приветствием.
    - Рассылки работают только в тестовом режиме. EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


                                                            Что ещё в разработке:
- Возможность ставить лайки/дизлайки, оставлять комментарии
- Уже реализовано в БД, но не на сайте.
- Кэширование списка новостей.
- Удалить второй тип постов. “статьи” (**Article**) - лишняя сущность
- Локализация сайта

                                                            Известные ошибки:
- Не авторизованному пользователю показываются кнопки редактирования новости, но при нажатии происходит ошибка
- Не работает поиск по заголовку.
- В поиске категории выбираются только с зажатым ctrl, должно простым кликом
- Оба варианта регистрации подписаны “Sign UP with social Account”. Надо изменить надпись или разнести регистрацию по разным страницам.
- Не настроена вёрстка
