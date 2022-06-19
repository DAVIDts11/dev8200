import http
import json
import uvicorn
from fastapi import FastAPI
import http.client

from starlette.responses import HTMLResponse
from tabulate import tabulate

"""
A parser api script, using fast-api.

Author:
Date: 19/06/22
"""


class ParserAPI:
    """
    parms:
    _user_list: a set of users.
    _top_consumers: a list of 5 command at most.
    _csv_file_name: a name of the csv file.
    """

    def __init__(self):
        """
        important note, we can consider creating an entry class and parse details to it,
        but it will be very RAM consuming so i prefer spend time over space here, and
        parse only the essential individual details.
        """
    def get_top5_api(self):
        try:
            conn = http.client.HTTPSConnection("v3.football.api-sports.io")

            headers = {
                'x-rapidapi-host': "v3.football.api-sports.io",
                'x-rapidapi-key':  "b1035ff6831d179f86481c028bcf0836"
            }

            conn.request("GET", "/players/topscorers?season=2018&league=61", headers=headers)

            res = conn.getresponse()
            data = res.read()

            json_data = json.loads(data.decode("utf-8"))
            json_resp = json_data["response"]
            return json_resp
        except Exception as e:
            return e.__str__()

    def print_top5_byGOALS(self):
        try:

            json_resp = self.get_top5_api()
            # print(json.dumps(json_resp, indent=4, sort_keys=True))d
            res = []
            for i in range(5):
                player_details = []
                # print(json.dumps(json_resp[i], indent=4, sort_keys=True))
                print(json.dumps(json_resp[i]["player"]["name"], indent=4, sort_keys=True))
                player_details.append(json.dumps(json_resp[i]["player"]["name"], indent=4, sort_keys=True))
                print(json.dumps(json_resp[i]["statistics"][0]["team"]["name"], indent=4, sort_keys=True))
                player_details.append(
                    json.dumps(json_resp[i]["statistics"][0]["team"]["name"], indent=4, sort_keys=True))
                print(json.dumps(json_resp[i]["statistics"][0]["goals"]["total"], indent=4, sort_keys=True))
                player_details.append(
                    json.dumps(json_resp[i]["statistics"][0]["goals"]["total"], indent=4, sort_keys=True))
                print(json.dumps(json_resp[i]["player"]["photo"], indent=4, sort_keys=True))
                image_link = json.dumps(json_resp[i]["player"]["photo"], indent=4, sort_keys=True)

                image = f"<img src={image_link}>"


                player_details.append(image)
                res.append(player_details)

            return res
        except Exception as e:
            return e.__str__()


app = FastAPI()
parser = ParserAPI()


@app.get("/")
def read_root():
    return {"greetings": "Sports app"}


@app.get("/top5")
def getTopComsuming5():
    return create_table()

def create_table():
    table = parser.print_top5_byGOALS()
    table_html = tabulate(table, tablefmt = 'html')
    response = f"""
    <html>
        <head>
            <title></title>
            {table_html}
        </head>
        <body>
        </body>
    </html>
    """

    return HTMLResponse(content=response, status_code=200)

if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")
    print("Finished.")
