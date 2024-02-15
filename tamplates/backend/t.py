import requests

def handler(request):
  if request.method == "POST":
    # Отримуємо дані з POST-запиту
    data = request.get_json()

    # Відправляємо відповідь
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "text/plain"
    response.text = "конект є"

    return response

if __name__ == "__main__":
  # Слухаємо POST-запити на порт 8080
  app = requests.server(host="localhost", port=8080, handler=handler)
  app.serve_forever()