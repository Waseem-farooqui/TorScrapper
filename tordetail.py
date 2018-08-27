from flask import Flask, request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)


@app.route('/tor')
def get_tor():
    result = get_tor_detail(request.args['ip'], request.args['date'])
    if result is None:
        return "No Record", 204
    response = app.response_class(
        response=result,
        status=200,
        mimetype='application/json'
    )
    return response


def get_tor_detail(ip, time):
    page = requests.get("https://exonerator.torproject.org/?ip=%s&timestamp=%s&lang=en" % (ip, time))
    soup = BeautifulSoup(page.content, 'html.parser')

    success = soup.find('div', attrs={'class': 'panel-success'})
    if success is not None:
        data = {}
        header = []
        child = []

        table = soup.find('table', attrs={'class': 'table'})
        table_head = table.find('thead')
        head_row = table_head.find('tr')
        head_cols = head_row.find_all('th')

        for head in head_cols:
            header.append(head.text.strip())

        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            i = 0
            for row in cols:
                data[header[i]] = row
                i += 1
            child.append(data)
            # print ([ele for ele in cols if ele]) # Get rid of empty values

        json_data = json.dumps(child)

        return json_data
    return None


if __name__ == '__main__':
    app.run(host = '0.0.0.0')
