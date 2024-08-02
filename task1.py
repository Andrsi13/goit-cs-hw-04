import threading
import os
import time
from queue import Queue

def search_keywords_in_file(file_path, keywords, queue):
    results = {keyword: [] for keyword in keywords}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file_path)
    except Exception as e:
        print(f"Помилка при читанні файлу {file_path}: {e}")
    queue.put(results)

def process_files(file_paths, keywords, queue):
    for file_path in file_paths:
        search_keywords_in_file(file_path, keywords, queue)

def main():
    directory = 'test_files'  # шлях до каталогу
    keywords = {'keyword1', 'keyword2'}  # ключові слова
    queue = Queue()
    
    # Отримати всі текстові файли в каталозі
    file_paths = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    
    # Перевірка кількості файлів
    num_files = len(file_paths)
    num_threads = 4  # Кількість потоків

    if num_files == 0:
        print("Не знайдено текстових файлів у каталозі.")
        return

    if num_files < num_threads:
        num_threads = num_files

    chunk_size = max(num_files // num_threads, 1) 
    chunks = [file_paths[i:i + chunk_size] for i in range(0, num_files, chunk_size)]

    start_time = time.time()
    threads = []
    for chunk in chunks:
        thread = threading.Thread(target=process_files, args=(chunk, keywords, queue))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    results = {keyword: [] for keyword in keywords}
    while not queue.empty():
        partial_result = queue.get()
        for keyword, files in partial_result.items():
            results[keyword].extend(files)

    end_time = time.time()
    print(f"Час виконання: {end_time - start_time:.2f} секунд")

    # Виведення результатів
    print("Результати пошуку:")
    for keyword, files in results.items():
        print(f"Ключове слово: {keyword}, Файли: {', '.join(files)}")

if __name__ == '__main__':
    main()
