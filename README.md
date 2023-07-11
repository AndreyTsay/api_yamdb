<h1 class="code-line" data-line-start="0" data-line-end="1"><a id="API_FINAL_YATUBE_0"></a>API_YAMDB</h1>
<p class="has-line-data" data-line-start="4" data-line-end="5">Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв. Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.</p>
<h2 class="code-line" data-line-start="31" data-line-end="32"><a id="Tech_31"></a>Tech</h2>
<p class="has-line-data" data-line-start="33" data-line-end="34">API_YAMDB использует следующие технологии:</p>
<p class="has-line-data" data-line-start="35" data-line-end="39">Python 3.11,<br>
Django 3.8,<br>
DRF,<br>
JWT + Djoser</p>
<h2 class="code-line" data-line-start="41" data-line-end="42"><a id="Installation_41"></a>Installation</h2>
<p class="has-line-data" data-line-start="43" data-line-end="57">Клонировать репозиторий и перейти в него в командной строке.<br>
Установите и активируйте виртуальное окружение<br>
python -m venv venv<br>
source venv/Scripts/activate<br>
python -m pip install --upgrade pip<br>
Затем нужно установить все зависимости из файла requirements.txt<br>
cd yatube_api<br>
pip install -r requirements.txt<br>
Выполняем миграции:<br>
python <a href="http://manage.py">manage.py</a> migrate<br>
Импортируем файл csv:<br>
python3 manage.py import_csv<br>
Создаем суперпользователя:<br>
python <a href="http://manage.py">manage.py</a> createsuperuser<br>
Запускаем проект:<br>
python <a href="http://manage.py">manage.py</a> runserver</p>
<h2 class="code-line" data-line-start="41" data-line-end="42"><a id="Creators"></a>Creators</h2>
<p class="has-line-data" data-line-start="43" data-line-end="57">Над данным проектом работала команда студентов Яндекс Практикума.<br>
Цай Андрей | AndreyTsay <br>
Ольга Белова | blwolhppt <br>
Ян Свиридов | YanSv15<br>