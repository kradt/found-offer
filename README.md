# "Found-Offer" - Платформа для Ефективного Пошуку Вакансій

## Проблема:
На українському ринку праці інформація про вакансії розташована на різних веб-сайтах. Це може бути не завжди зручно для кандидатів, які шукають роботу, та роботодавців, які розміщують вакансії.

## Рішення:
"Found-Offer" забезпечує зручність, збираючи всю інформацію про вакансії з різних сайтів та пропонуючи її в одному місці. Кандидатам не потрібно бігати по різних сайтах - вони можуть легко знайти роботу на одній платформі. Крім того, користувачі можуть налаштувати автоматичний пошук вакансій за вказаними критеріями, що спрощує їхній пошук та заощаджує час.

## Особливості
- Пошук та Фільтрація Вакансій: Користувачі можуть легко знаходити вакансії, використовуючи різні фільтри, такі як назва, зарплата, місто. Це допомагає знайти вакансії, які відповідають їхнім потребам та очікуванням.
- Сортування за Зарплатою: Користувачі можуть сортувати вакансії за рівнем зарплати, що допомагає їм знайти найвигідніші пропозиції.
- Спаршені та Користувацькі Вакансії: Платформа включає в себе як спаршені вакансії з різних джерел, так і ті, які користувачі можуть додати самостійно. Це забезпечує широкий вибір можливостей.
- Авторизація через Google OAuth: Користувачі можуть швидко та безпечно увійти в систему використовуючи свій обліковий запис Google.
- Управління Профілем та Паролем: Користувачі можуть змінювати свій пароль та налаштовувати свій профіль.
- Автоматичний Пошук: Система автоматичного пошуку постійно відслідковує базу даних на наявність нових вакансій, які відповідають потребам користувачів, і надсилає їх на електронну пошту користувача.

## Використані Технології
У проекті "Found-Offer" використовуються сучасні технології для оптимізації функціоналу та зручності користувачів, такі як:

- Flask: Веб-додаток побудований на фреймворку Flask, який надає гнучкість та швидкість розробки веб-сервісів.
- MongoDB: В якості бази даних використовується MongoDB, що дозволяє зберігати та опрацьовувати великі обсяги структурованої та неструктурованої інформації.
- Celery: Для асинхронного виконання завдань, таких як парсинг та відправка повідомлень, використовується Celery. Цей сервіс допомагає ефективно розподіляти завдання та уникати блокування сервера.
- Redis: Redis використовується як брокер для Celery для зберігання та розподілу завдань. Також Redis використовується для зберігання кодів для відновлення паролів користувачів та інших завдань.
- Google OAuth: Додаток надає можливість користувачам авторизуватися через Google OAuth, що забезпечує безпечний та зручний спосіб входу.
- Тестування: Проект покритий тестами для забезпечення стабільності та надійності функціональності.
- Docker-Compose: Додаток обгорнутий в Docker-контейнери для легкої розгортання та масштабування.

## Висновок

Проект "Found-Offer" вирішує актуальну проблему пошуку роботи, роблячи цей процес більш зручним та ефективним для користувачів. Використовуючи сучасні технології, цей додаток дозволяє:

- Зручний Пошук Роботи: Користувачі можуть легко знаходити вакансії, використовуючи фільтри та сортування за різними критеріями.
- Автоматичний Пошук: Автоматична система пошуку стежить за новими вакансіями та надсилає їх користувачам, що допомагає зекономити час при пошуку роботи.
- Безпечна Авторизація: Використання Google OAuth забезпечує безпечний та зручний спосіб входу в систему.
- Управління Профілем: Користувачі можуть легко налаштовувати свій профіль та додавати нові вакансії.

Цей проект підтверджує мої навички у веб-розробці, використанні баз даних (MongoDB), чергах задач (Celery та Redis), інтеграції з зовнішніми сервісами (Google OAuth), тестуванні та контейнеризації (Docker-Compose). Він демонструє мою здатність розв'язувати складні завдання та створювати високоякісні веб-додатки, які відповідають потребам користувачів.

# Quick Start

Для швидкого запуску та налаштування додатку, виконайте наступні кроки:


## Крок 1: Налаштування .env файлу

Створіть файл .env у корені проекту з наступними змінними середовища:
```
SECRET_KEY=mysecretkey
MONGO_URI=mongodb://username:password@mongo:27017/dbname
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-email-password
OAUTHLIB_INSECURE_TRANSPORT=1
REDIS_URL=redis://redis:6379
```
- SECRET_KEY: Це секретний ключ, який використовується для підпису сесій та інших даних в додатку. Це має бути випадковим рядком для забезпечення безпеки.
- MONGO_URI: Адреса підключення до бази даних MongoDB. Ви повинні вказати ім'я користувача, пароль, хост та порт бази даних, а також ім'я бази даних.
- CLIENT_ID і CLIENT_SECRET: Це дані, які ви отримуєте при створенні додатка у службі автентифікації, наприклад, Google OAuth. Вони дозволяють вашому додатку взаємодіяти зі службою автентифікації.
- MAIL_USERNAME і MAIL_PASSWORD: Це дані вашої поштової скриньки для надсилання листів через електронну пошту.
- OAUTHLIB_INSECURE_TRANSPORT: Це параметр, який може бути встановлений в 1, якщо ви використовуєте незахищений транспорт (HTTP), і 0, якщо ви використовуєте захищений транспорт (HTTPS). Встановлення його в 1 використовується в режимі розробника для тестування без HTTPS.
- REDIS_URL: Адреса підключення до Redis, яка використовується як брокер для асинхронних завдань.

## Крок 2: Запуск

Виконайте команду docker-compose up для запуску додатку.

`docker-compose up`

# Приклад Використання
https://vimeo.com/manage/videos/865273646

