import requests
import json
def refresh_token(login, password):
  url = "https://authnode.cdek.ru/api/auth/login"
  
  payload = json.dumps({
    "lang": "rus",
    "login": login,
    "password": password,
    "hash": login,
    "adLogin": True,
    "push": False,
    "data": [
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
      False,
      "ru-RU",
      24,
      "not available",
      1,
      12,
      [
        2560,
        1440
      ],
      [
        2560,
        1392
      ],
      -240,
      "Europe/Samara",
      True,
      True,
      True,
      False,
      False,
      "not available",
      "Win32",
      "1",
      [
        [
          "PDF Viewer",
          "Portable Document Format",
          [
            [
              "application/pdf",
              "pdf"
            ],
            [
              "text/pdf",
              "pdf"
            ]
          ]
        ],
        [
          "Chrome PDF Viewer",
          "Portable Document Format",
          [
            [
              "application/pdf",
              "pdf"
            ],
            [
              "text/pdf",
              "pdf"
            ]
          ]
        ],
        [
          "Chromium PDF Viewer",
          "Portable Document Format",
          [
            [
              "application/pdf",
              "pdf"
            ],
            [
              "text/pdf",
              "pdf"
            ]
          ]
        ],
        [
          "Microsoft Edge PDF Viewer",
          "Portable Document Format",
          [
            [
              "application/pdf",
              "pdf"
            ],
            [
              "text/pdf",
              "pdf"
            ]
          ]
        ],
        [
          "WebKit built-in PDF",
          "Portable Document Format",
          [
            [
              "application/pdf",
              "pdf"
            ],
            [
              "text/pdf",
              "pdf"
            ]
          ]
        ]
      ],
      "Google Inc. (NVIDIA)~ANGLE (NVIDIA, NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0), or similar",
      False,
      False,
      False,
      False,
      False,
      [
        0,
        False,
        False
      ],
      [
        "Arial",
        "Arial Black",
        "Arial Narrow",
        "Calibri",
        "Cambria",
        "Cambria Math",
        "Comic Sans MS",
        "Consolas",
        "Courier",
        "Courier New",
        "Georgia",
        "Helvetica",
        "Impact",
        "Lucida Console",
        "Lucida Sans Unicode",
        "Microsoft Sans Serif",
        "MS Gothic",
        "MS PGothic",
        "MS Sans Serif",
        "MS Serif",
        "Palatino Linotype",
        "Segoe Print",
        "Segoe Script",
        "Segoe UI",
        "Segoe UI Light",
        "Segoe UI Semibold",
        "Segoe UI Symbol",
        "Tahoma",
        "Times",
        "Times New Roman",
        "Trebuchet MS",
        "Verdana",
        "Wingdings"
      ],
      "swf object not loaded",
      "35.749972093850374",
      [
        "krainov.e"
      ]
    ]
  })
  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  print(response.text)
  return response.json()



def exchange_code(login, password , code):
  import requests
  import json

  url = "https://authnode.cdek.ru/api/exchangeCode"

  payload = json.dumps({
    "lang": "rus",
    "login": login,
    "password": password,
    "hash": login,
    "adLogin": True,
    "push": False,
    "code": f"{code}",
    "data": [
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
      False,
      "ru-RU",
      24,
      "not available",
      1,
      12,
      [
        2560,
        1440
      ],
      [
        2560,
        1392
      ],
      -240,
      "Europe/Samara",
      True,
      True,
      True,
      False,
      False,
      "not available",
      "Win32",
      "1",
      [
        [
          "PDF Viewer",
          "Portable Document Format",
          [
            [
              "application/pdf",
              "pdf"
            ],
            [
              "text/pdf",
              "pdf"
            ]
          ]
        ],
        [
          "Chrome PDF Viewer",
          "Portable Document Format",
          [
            [
              "application/pdf",
              "pdf"
            ],
            [
              "text/pdf",
              "pdf"
            ]
          ]
        ],
        [
          "Chromium PDF Viewer",
          "Portable Document Format",
          [
            [
              "application/pdf",
              "pdf"
            ],
            [
              "text/pdf",
              "pdf"
            ]
          ]
        ],
        [
          "Microsoft Edge PDF Viewer",
          "Portable Document Format",
          [
            [
              "application/pdf",
              "pdf"
            ],
            [
              "text/pdf",
              "pdf"
            ]
          ]
        ],
        [
          "WebKit built-in PDF",
          "Portable Document Format",
          [
            [
              "application/pdf",
              "pdf"
            ],
            [
              "text/pdf",
              "pdf"
            ]
          ]
        ]
      ],
      "Google Inc. (NVIDIA)~ANGLE (NVIDIA, NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0), or similar",
      False,
      False,
      False,
      False,
      False,
      [
        0,
        False,
        False
      ],
      [
        "Arial",
        "Arial Black",
        "Arial Narrow",
        "Calibri",
        "Cambria",
        "Cambria Math",
        "Comic Sans MS",
        "Consolas",
        "Courier",
        "Courier New",
        "Georgia",
        "Helvetica",
        "Impact",
        "Lucida Console",
        "Lucida Sans Unicode",
        "Microsoft Sans Serif",
        "MS Gothic",
        "MS PGothic",
        "MS Sans Serif",
        "MS Serif",
        "Palatino Linotype",
        "Segoe Print",
        "Segoe Script",
        "Segoe UI",
        "Segoe UI Light",
        "Segoe UI Semibold",
        "Segoe UI Symbol",
        "Tahoma",
        "Times",
        "Times New Roman",
        "Trebuchet MS",
        "Verdana",
        "Wingdings"
      ],
      "swf object not loaded",
      "35.749972093850374",
      [
        "krainov.e"
      ]
    ]
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  print(response.text)
  return response.json()



def check_login():
  pass
