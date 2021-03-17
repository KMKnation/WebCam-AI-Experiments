import requests

url = "https://in.bookmyshow.com/nm-api/is/book"

payload = {
  "quantity": 10,
  "selectedSeats": [
    {
      "areaIndex": 0,
      "rowIndex": 15,
      "areaNumber": "1",
      "cinemaSeatNumber": "95",
      "rowId": "16",
      "AreaCode": "AC00000184",
      "rowNumber": "RR",
      "seatIndex": 3,
      "seatNumber": "04"
    },
    {
      "areaIndex": 0,
      "rowIndex": 15,
      "areaNumber": "1",
      "cinemaSeatNumber": "96",
      "rowId": "16",
      "AreaCode": "AC00000184",
      "rowNumber": "RR",
      "seatIndex": 4,
      "seatNumber": "05"
    },
    {
      "areaIndex": 0,
      "rowIndex": 15,
      "areaNumber": "1",
      "cinemaSeatNumber": "97",
      "rowId": "16",
      "AreaCode": "AC00000184",
      "rowNumber": "RR",
      "seatIndex": 5,
      "seatNumber": "06"
    },
    {
      "areaIndex": 0,
      "rowIndex": 15,
      "areaNumber": "1",
      "cinemaSeatNumber": "98",
      "rowId": "16",
      "AreaCode": "AC00000184",
      "rowNumber": "RR",
      "seatIndex": 6,
      "seatNumber": "07"
    },
    {
      "areaIndex": 0,
      "rowIndex": 15,
      "areaNumber": "1",
      "cinemaSeatNumber": "99",
      "rowId": "16",
      "AreaCode": "AC00000184",
      "rowNumber": "RR",
      "seatIndex": 7,
      "seatNumber": "08"
    },
    {
      "areaIndex": 0,
      "rowIndex": 15,
      "areaNumber": "1",
      "cinemaSeatNumber": "100",
      "rowId": "16",
      "AreaCode": "AC00000184",
      "rowNumber": "RR",
      "seatIndex": 8,
      "seatNumber": "09"
    },
    {
      "areaIndex": 0,
      "rowIndex": 15,
      "areaNumber": "1",
      "cinemaSeatNumber": "101",
      "rowId": "16",
      "AreaCode": "AC00000184",
      "rowNumber": "RR",
      "seatIndex": 9,
      "seatNumber": "10"
    },
    {
      "areaIndex": 0,
      "rowIndex": 15,
      "areaNumber": "1",
      "cinemaSeatNumber": "102",
      "rowId": "16",
      "AreaCode": "AC00000184",
      "rowNumber": "RR",
      "seatIndex": 10,
      "seatNumber": "11"
    },
    {
      "areaIndex": 0,
      "rowIndex": 15,
      "areaNumber": "1",
      "cinemaSeatNumber": "103",
      "rowId": "16",
      "AreaCode": "AC00000184",
      "rowNumber": "RR",
      "seatIndex": 11,
      "seatNumber": "12"
    },
    {
      "areaIndex": 0,
      "rowIndex": 15,
      "areaNumber": "1",
      "cinemaSeatNumber": "104",
      "rowId": "16",
      "AreaCode": "AC00000184",
      "rowNumber": "RR",
      "seatIndex": 12,
      "seatNumber": "13"
    }
  ],
  "lngTransId": "",
  "venueCode": "SPSM",
  "sessionID": "10038",
  "ticketType": "T319",
  "ticketsArr": [

  ],
  "commands": [
    "INITTRANS",
    "ADDSEATS",
    "SETSELECTEDSEATS"
  ],
  "UID": "",
  "LSID": "YU53QUZXMRINHN8XPGPQ",
  "MEMBERID": "99819489",
  "isUserLock": True,
  "appCode": "WEB"
}

#F BAY https://in.bookmyshow.com/ahmedabad/sports/2nd-t20-india-vs-england/seat-layout/selectionview/ET00306202/SPSM/10038/AC00000199
#Aerial View https://in.bookmyshow.com/ahmedabad/sports/2nd-t20-india-vs-england/seat-layout/aerialview/ET00306202/SPSM/10038
#C 5 https://in.bookmyshow.com/ahmedabad/sports/2nd-t20-india-vs-england/seat-layout/selectionview/ET00306202/SPSM/10038/AC00000184
headers = {
    'cf-cache-status': "DYNAMIC",
    'cf-ray': "62b23c0fed002e59-BOM",
    'cf-request-id': "08a343ddf000002e59852ed000000001",
    'content-length': "455",
    'content-type': "application/json",
    'referer': "https://in.bookmyshow.com/ahmedabad/sports/2nd-t20-india-vs-england/seat-layout/selectionview/ET00306202/SPSM/10038/AC00000184",
    'sec-ch-ua': "\"Chromium\";v=\"88\", \"Google Chrome\";v=\"88\", \";Not A Brand\";v=\"99\"",
    'sec-ch-ua-mobile': "70",
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    'cache-control': "no-cache"
    }

import time
for i in range(1000000):
    response = requests.request("POST", url, data=payload, headers=headers)
    print("{} -  {} ".format(response.status_code, response.reason))
    time.sleep(60)
