import requests
import threading
import time

# 攻撃対象のURL
url = "http://127.0.0.1:8000/transactions/"

# 送信するデータ
data = {
    "datetime": "2024-06-28T12:00:00Z",
    "emp_code": "EMP001",
    "store_code": "STR001",
    "pos_no": "POS001",
    "total_amt": 1000,
    "details": [{"product_code": "1234567890123", "product_name": "Test Product", "product_price": 1000, "quantity": 1}],
}

headers = {'Content-Type': 'application/json'}


# リクエストを送信する関数
def send_request():
    while True:
        try:
            response = requests.post(url, json=data, headers=headers)
            print(f"Status Code: {response.status_code}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")


# スレッドを使ってリクエストを並行して送信
threads = []
for i in range(10):  # 10スレッドでリクエストを並行して送信
    thread = threading.Thread(target=send_request)
    thread.start()
    threads.append(thread)

# スレッドが終了するのを待つ
for thread in threads:
    thread.join()
