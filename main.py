import time
import fake_useragent
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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

SECONDS_WAIT_FOR_USER_AUTHORIZADE = 300
WHATSAPP_URL = "https://web.whatsapp.com/"

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


def is_authorized(driver) -> bool:
    """Возвращает True, если авторизация была пройдена успешно"""
    try:
        # Ожидаем исчезновения тега с id="wa_web_initial_startup"
        WebDriverWait(driver, SECONDS_WAIT_FOR_USER_AUTHORIZADE).until_not(EC.presence_of_element_located((By.ID, "wa_web_initial_startup")))
        time.sleep(7)
        if driver.current_url == WHATSAPP_URL:
            return True
        return False
    except Exception as ex:
        print(f"[+] Ошибка при авторизации: {ex}")
        return False
    finally:
        driver.quit()


def create_profile(num: int) -> None:
    """Создание профиля"""
    try:
        profile = webdriver.ChromeOptions()
        profile.add_argument(f"user-data-dir={session_folder_path}/profile{num}")
        driver = webdriver.Chrome(options=profile)
        driver.get(WHATSAPP_URL)
        if not is_authorized(driver):
            raise
        print("[+] Авторизация пройдена успешно. Профиль создан.")
    except Exception as ex:
        print(f"Ошибка при создании профиля: {ex}")
    finally:
        driver.quit()


def append_profiles() -> None:
    """Создание новых профилей и верификация"""
    counter_profiles = len(os.listdir(session_folder_path))
    count_new_profiles = int(input("[+] Введите количество профилей : \n"))

    for i in range(counter_profiles + 1, counter_profiles + count_new_profiles + 1):
        create_profile(i)


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


def open_and_spam(name_profile: str, list_numbers: list) -> None:
    """Открывает профиль и делает рассылку по list_numbers"""
    profile = webdriver.ChromeOptions()
    profile.add_argument(f"user-data-dir={session_folder_path}/{name_profile}")
    driver = webdriver.Chrome(options=profile)
    driver.get(WHATSAPP_URL)


clear_session_folder()
# create_profile(1)

# append_profiles()

# clear_session_folder()
