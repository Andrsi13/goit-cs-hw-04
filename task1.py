import threading
import os


def search_keywords_in_file(file_path, keywords, results):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            found_keywords = {keyword for keyword in keywords if keyword in content}
            if found_keywords:
                results[file_path] = found_keywords
                print(f"Знайдено ключові слова в {file_path}: {found_keywords}")
    except Exception as e:
        print(f"Помилка при читанні файлу {file_path}: {e}")


def process_files(file_paths, keywords, results):
    threads = []
    for file_path in file_paths:
        thread = threading.Thread(
            target=search_keywords_in_file, args=(file_path, keywords, results)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def main():
    directory = "test_files"
    keywords = {"keyword1", "keyword2"}  #ключові слова
    results = {}

    #текстові файли в каталозі
    file_paths = [
        os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".txt")
    ]

    # перевірка кількості файлів
    num_files = len(file_paths)
    num_threads = 4  # Кількість потоків

    if num_files == 0:
        print("Не знайдено текстових файлів у каталозі.")
        return

    if num_files < num_threads:
        num_threads = num_files

    chunk_size = max(num_files // num_threads, 1)  # Запобігаємо діленню на нуль
    chunks = [file_paths[i : i + chunk_size] for i in range(0, num_files, chunk_size)]

    print("Чекання на завершення всіх потоків...")
    # обробка файлів у паралельних потоках
    threads = []
    for chunk in chunks:
        thread = threading.Thread(target=process_files, args=(chunk, keywords, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("Усі потоки завершені.")

    # введення результатів
    print("Результати пошуку:")
    for file_path, found_keywords in results.items():
        print(f"Файл: {file_path}, Ключові слова: {', '.join(found_keywords)}")


if __name__ == "__main__":
    main()
