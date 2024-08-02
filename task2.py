import multiprocessing
import os

def search_keywords_in_file(file_path, keywords, queue):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            found_keywords = {keyword for keyword in keywords if keyword in content}
            if found_keywords:
                queue.put((file_path, found_keywords))
    except Exception as e:
        print(f"Помилка при читанні файлу {file_path}: {e}")

def process_files(file_paths, keywords, queue):
    for file_path in file_paths:
        search_keywords_in_file(file_path, keywords, queue)

def main():
    directory = 'test_files'  # шлях до каталогу
    keywords = {'keyword1', 'keyword2'}  # ключові слова
    queue = multiprocessing.Queue()
    
    # Отримати всі текстові файли в каталозі
    file_paths = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    
    # Перевірка кількості файлів
    num_files = len(file_paths)
    num_processes = 4  # Кількість процесів

    if num_files == 0:
        print("Не знайдено текстових файлів у каталозі.")
        return

    if num_files < num_processes:
        num_processes = num_files

    chunk_size = max(num_files // num_processes, 1)
    chunks = [file_paths[i:i + chunk_size] for i in range(0, num_files, chunk_size)]

    # Обробка файлів у паралельних процесах
    processes = []
    for chunk in chunks:
        process = multiprocessing.Process(target=process_files, args=(chunk, keywords, queue))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()

    # Збір результатів з черги
    results = {}
    while not queue.empty():
        file_path, found_keywords = queue.get()
        results[file_path] = found_keywords

    # Виведення результатів
    print("Результати пошуку:")
    for file_path, found_keywords in results.items():
        print(f"Файл: {file_path}, Ключові слова: {', '.join(found_keywords)}")

if __name__ == '__main__':
    main()
