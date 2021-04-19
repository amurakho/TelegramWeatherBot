import json
import requests
import time

import const


def answer_user_bot(data):
    data = {
        'chat_id': const.MY_ID,
        'text': data
    }
    url = const.URL.format(token=const.TOKEN,
                           method=const.SEND_METH)
    _ = requests.post(url, data=data)


def parse_weather_data(data):
    weather_state = ""
    for elem in data['weather']:
        weather_state = elem['main']
    temp = round(data['main']['temp'] - 273.15, 2)
    city = data['name']
    return f'The weather in {city}: Temp is {temp}, State is {weather_state}'


def get_weather(location):
    url = const.WEATHER_URL.format(city=location,
                                   token=const.WEATHER_TOKEN)
    response = requests.get(url)
    if response.status_code != 200:
        return 'city not found'
    data = json.loads(response.content)
    return parse_weather_data(data)


def get_message(data):
    return data['message']['text']


def save_update_id(update):
    with open(const.UPDATE_ID_FILE_PATH, 'w') as file:
        file.write(str(update['update_id']))
    const.UPDATE_ID = update['update_id']
    return True


def main():
    while True:
        url = const.URL.format(token=const.TOKEN,
                               method=const.UPDATE_METH)
        content = requests.get(url).text

        data = json.loads(content)
        result = data['result'][::-1]
        needed_part = None

        for elem in result:
            if elem['message']['chat']['id'] == const.MY_ID:
                needed_part = elem
                break

        if const.UPDATE_ID != needed_part['update_id']:
            message = get_message(needed_part)
            msg = get_weather(message)
            answer_user_bot(msg)
            save_update_id(needed_part)

        time.sleep(1)


if __name__ == '__main__':
    main()
