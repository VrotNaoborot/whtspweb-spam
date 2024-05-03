import time
import fake_useragent
import os
from selenium import webdriver
from urllib.parse import quote
from pyautogui import press
import shutil

project_path = os.getcwd()
session_folder_path = os.path.join(project_path, "session")

message = "🫣"
encoded_message = quote(message.encode("utf-8"))

# main_url = "https://web.whatsapp.com/"
# send_msg_url = f"https://web.whatsapp.com/send?phone=+79998616672&text={encoded_message}"
#
# profile_path = "/Users/panu/my_practice/whtsp_spam/session"
# profile_name = "profile1"
# profile = webdriver.ChromeOptions()
#
# profile.add_argument(f"user-data-dir={profile_path}/{profile_name}")
#
# driver = webdriver.Chrome(options=profile)
# driver.get("https://web.whatsapp.com/")
#
# input()
#
# driver.get(send_msg_url)
# input()
# press("enter")
# print("Энтер нажал ")
# driver.quit()


def clear_session_folder() -> bool:
    # Проверяем существует ли папка "session"
    if os.path.exists(session_folder_path):
        # Очищаем содержимое папки
        for filename in os.listdir(session_folder_path):
            file_path = os.path.join(session_folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # рекурсивное удаление содержимого папки
            except Exception as e:
                print(f"[+] Ошибка при удалении {file_path}. Вызвано: {e}")
                return False

        print("[+] Все сессии очищены")
        return True

    else:
        print("[+] Не существует директории session")
        return False


def append_profiles() -> None:
    """Создание новых профилей и верификация"""
    counter_profiles = len(os.listdir(session_folder_path))
    count_new_profiles = int(input("[+] Введите количество профилей : \n"))

    for i in range(counter_profiles+1, counter_profiles+count_new_profiles+1):
        print(f"Иммитация создания профиля с названием profile{i}")


def change_profiles():
    while True:
        action = input(
            f"[+] Введите 1, если необходимо удалить все профили и добавить новые\nВведите 2 для добавления к существующим")
        if action not in {"1", "2"}:
            print("[+] Неправильное значение")
            continue
        break

    if action == "1":
        clear_session_folder()
    append_profiles()


append_profiles()

