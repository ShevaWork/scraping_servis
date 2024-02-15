from flask import Flask, request, render_template
from func import check_and_write_text, delete_row_by_string, remove_newline_from_end, add_text_to_devices

app = Flask(__name__)

@app.route('/add', methods=['GET'])
def add_text():
    text_to_save = request.args.get('text')

    if text_to_save is not None:
        response_message = check_and_write_text(text_to_save)
        add_text_to_devices()
        remove_newline_from_end()
        return response_message
    else:
        return "Отримано невірний або відсутній параметр 'text'.", 400


@app.route('/remote', methods=['GET'])
def remote_text():
    text_to_save = request.args.get('text')

    if text_to_save is not None:
        response_message = delete_row_by_string(text_to_save)
        add_text_to_devices()
        remove_newline_from_end()
        return response_message
    else:
        return "Отримано невірний або відсутній параметр 'text'.", 400


@app.route('/load', methods=['GET'])
def load():
    text_to_save = request.args.get('text')

    if text_to_save is not None:
        response_message = text_to_save
        add_text_to_devices()
        remove_newline_from_end()
        return response_message
    else:
        return "Отримано невірний або відсутній параметр 'text'.", 400



@app.route('/hello')
def hello():
    return render_template('hello.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)