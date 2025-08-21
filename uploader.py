import sys
import os
from database import MapRepository
from config import TEMP_DIR

def main():
    if len(sys.argv) != 4:
        sys.exit(1)

    mapname = sys.argv[1]
    mapfile_path = f"{sys.argv[2]}"
    jsonfile_path = f"{sys.argv[3]}"
    
    if not os.path.exists(mapfile_path):
        print(f"Ошибка: Файл стилей не найден по пути: {mapfile_path}")
        sys.exit(1)
        
    if not os.path.exists(jsonfile_path):
        print(f"Ошибка: Файл данных не найден по пути: {jsonfile_path}")
        sys.exit(1)

    print(f"Загрузка карты '{mapname}' из файлов:")
    print(f"  - Картостиль: {mapfile_path}")
    print(f"  - Данные: {jsonfile_path}")

    try:
        repo = MapRepository()
        repo.create_table() 

        with open(mapfile_path, "r", encoding="utf-8") as f:
            mapstyle_content = f.read()

        with open(jsonfile_path, "r", encoding="utf-8") as f:
            gjson_content = f.read()

        original_json_filename = os.path.basename(jsonfile_path)
        original_connection = f'CONNECTION "{original_json_filename}"'
        
        target_json_filename = f"{mapname}.json"
        full_json_path = os.path.join(TEMP_DIR, target_json_filename)
        new_connection = f'CONNECTION "{full_json_path}"'
        
        modified_mapstyle_content = mapstyle_content.replace(original_connection, new_connection)
        
        if modified_mapstyle_content == mapstyle_content:
            print("Картостиль будет сохранен без изменений пути.")

        repo.upsert_map(mapname, modified_mapstyle_content, gjson_content)
        
        print("\nОперация успешно завершена!")

    except Exception as e:
        print(f"\nОшибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()