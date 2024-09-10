from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Создаем Flask приложение
app = Flask(__name__)

# Настройки приложения
app.config['SECRET_KEY'] = 'your_secret_key'  # Ключ для сессий и флеш-сообщений
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # База данных SQLite

# Инициализация базы данных
db = SQLAlchemy(app)

# Определение модели пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Идентификатор (первичный ключ)
    name = db.Column(db.String(50), nullable=False)  # Имя пользователя (обязательно для заполнения)
    city = db.Column(db.String(50), nullable=True)  # Город пользователя
    hobby = db.Column(db.String(50), nullable=True)  # Хобби пользователя
    age = db.Column(db.Integer, nullable=False)  # Возраст пользователя (обязательно для заполнения)

    # Метод для удобного отображения объектов User
    def __repr__(self):
        return f'<User {self.name}>'

# Главная страница с формой
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form.get('name')
        city = request.form.get('city')
        hobby = request.form.get('hobby')
        age = request.form.get('age')

        # Проверка данных: имя не пустое, возраст — это число
        if not name or not age.isdigit():
            flash('Имя и возраст обязательны. Возраст должен быть числом.', 'danger')  # Показать ошибку
        else:
            # Сохраняем пользователя в базу данных
            user = User(name=name, city=city, hobby=hobby, age=int(age))
            db.session.add(user)  # Добавляем нового пользователя
            db.session.commit()  # Сохраняем изменения
            flash('Данные успешно сохранены!', 'success')  # Показать сообщение об успехе
            return redirect(url_for('index'))  # Перенаправляем на главную страницу для обновления формы

    # Извлекаем всех пользователей из базы данных для отображения на странице
    users = User.query.all()
    return render_template('index.html', users=users)

# Основной блок для запуска приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаем таблицы в базе данных, если они еще не существуют
    app.run(debug=True)  # Запускаем приложение с режимом отладки

