import duckdb
import argparse
import os

def merge_big_tables(file1, file2, output, how='left'):
    """
    Быстрый merge двух больших parquet таблиц по item_id с помощью DuckDB.
    
    :param file1: путь к первому parquet файлу
    :param file2: путь ко второму parquet файлу
    :param output: путь к parquet файлу результата
    :param how: тип join — left / inner / right / full (default: left)
    """
    # Проверяем наличие файлов
    if not os.path.exists(file1):
        raise FileNotFoundError(f"Не найден файл: {file1}")
    if not os.path.exists(file2):
        raise FileNotFoundError(f"Не найден файл: {file2}")

    print(f"📥 Чтение: {file1} ({os.path.getsize(file1)/1e9:.2f} GB)")
    print(f"📥 Чтение: {file2} ({os.path.getsize(file2)/1e9:.2f} GB)")
    print(f"🪄 Тип объединения: {how}")

    # Создаем подключение
    con = duckdb.connect()

    # Формируем SQL
    query = f"""
        SELECT *
        FROM '{file1}' t1
        {how.upper()} JOIN '{file2}' t2
        USING (user_id, item_id)
    """

    # Выполняем join и сразу выгружаем в parquet
    con.execute(f"""
        COPY ({query})
        TO '{output}'
        (FORMAT PARQUET, COMPRESSION ZSTD);
    """)

    print(f"✅ Merge завершён. Результат: {output}")
    print(f"📦 Размер файла: {os.path.getsize(output)/1e9:.2f} GB")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge two big parquet tables by item_id using DuckDB")
    parser.add_argument("--file1", required=True, help="Путь к первому parquet файлу")
    parser.add_argument("--file2", required=True, help="Путь ко второму parquet файлу")
    parser.add_argument("--output", default="merged.parquet", help="Путь к результирующему parquet файлу")
    parser.add_argument("--how", default="left", choices=["left", "inner", "right", "full"], help="Тип join")

    args = parser.parse_args()
    merge_big_tables(args.file1, args.file2, args.output, args.how)