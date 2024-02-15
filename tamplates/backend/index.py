# Імпортуємо модуль `flask`
from flask import Flask

# Створюємо об'єкт веб-фреймворку Flask
app = Flask(__name__)

# Дефініємо маршрут для сторінки "Привіт, світ!"
@app.route("/")
def hello_world():
    return """
    <html>
        <head>
            <title>Привіт, світ!</title>
        </head>
        <body>
            <div class="devices">
                <button type="button" id="add-device">Додати пристрій</button>
                <button type="button" id="delete-device">Видалити пристрій</button>
            </div>
            <script>
                document.getElementById("add-device").addEventListener("click", function() {
                    alert("Пристрій доданий!");
                });

                document.getElementById("delete-device").addEventListener("click", function() {
                    alert("Пристрій видалений!");
                });
            </script>
        </body>
    </html>
    """

# Запускаємо веб-сервер
app.run(debug=True)