import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.parse import quote
import multiprocessing
import shutil

project_path = os.getcwd()
session_folder_path = os.path.join(project_path, "session")

message = "🫣"
encoded_message = quote(message.encode("utf-8"))

SECONDS_WAIT_FOR_USER_AUTHORIZADE = 300
WHATSAPP_URL = "https://web.whatsapp.com/"
MESSAGE_FOR_SPAM = "hi"
ENCODED_FOR_SPAM = quote(MESSAGE_FOR_SPAM.encode("utf-8"))


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
        WebDriverWait(driver, SECONDS_WAIT_FOR_USER_AUTHORIZADE).until_not(
            EC.presence_of_element_located((By.ID, "wa_web_initial_startup")))
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


def open_and_spam(name_profile: str, list_numbers: list) -> None:
    """Открывает профиль и делает рассылку по list_numbers"""
    profile = webdriver.ChromeOptions()
    profile.add_argument(f"user-data-dir={session_folder_path}/{name_profile}")  # путь к профилю
    for number in list_numbers:
        try:
            driver = webdriver.Chrome(options=profile)
            send_msg_url = f"https://web.whatsapp.com/send?phone={number}&text={ENCODED_FOR_SPAM}"
            driver.get(send_msg_url)
            # ожидание загрузки
            time.sleep(7)
            # Отправляем сообщением нажатием enter
            webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(2)
            driver.quit()
        except Exception as ex:
            print(f"Ошибка отправки на номер: {number}. {ex}")


def numbers() -> list:
    """Открывает файл с номерами и парсит их"""
    with open("target_numbers.txt", "r", encoding="utf8") as f:
        numbers_data = [i.strip() for i in f.readlines() if i != "\n"]
        return numbers_data


def get_number_for_spam(target_numbers: list, count_profiles: int) -> list:
    """Возвращает номера для одного профиля, исходя из количества доступных профилей"""
    count_numbers_for_profile = len(target_numbers) // count_profiles
    cursor = 0
    while cursor < len(target_numbers):
        yield target_numbers[cursor:cursor + count_numbers_for_profile + 1]
        cursor += count_numbers_for_profile


def start_spam():
    data_targets = numbers()
    data_session = os.listdir(session_folder_path)
    if not len(data_targets):
        print("[+] Необходимо заполнить файл target_numbers.")
        return -1
    if not len(data_session):
        print("[+] Необходимо добавить сессии.")
        return -1
    i = get_number_for_spam(data_targets, len(data_session))
    processes = []
    for session in data_session:
        p = multiprocessing.Process(target=open_and_spam, args=(session, next(i)))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    else:
        print("[+] Все аккаунты успешно завершили свою работу.")


def main() -> None:
    while True:
        action = input(
            f"""Меню:
1. Необходимо удалить все профили и добавить новые.
2. Добавить к существующим.
3. Запустить спам.\n""")
        if action not in {"1", "2", "3"}:
            print("[+] Неправильное значение. Выбери 1-3")
            continue
        break

    if action == "1":
        clear_session_folder()
        append_profiles()
    elif action == "2":
        append_profiles()
    elif action == "3":
        start_spam()


if __name__ == "__main__":
    main()
