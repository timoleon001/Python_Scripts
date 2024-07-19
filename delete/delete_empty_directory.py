import os
import shutil  # Importing shutil for rmtree


def remove_directories(root_directory, keywords):
    """
    Удалите каталоги, которые либо пусты, либо содержат определенные ключевые слова в своих именах, включая все их содержимое.
 :param root_directory: Корневой каталог, из которого следует начать процесс удаления.
 :param ключевые слова: список строк ключевых слов. Если имя каталога содержит любое из этих ключевых слов или оно пустое,
 оно будет удалено вместе со всем своим содержимым.
    """
    for root, dirs, files in os.walk(root_directory, topdown=False):
        for dir_name in dirs:
            current_dir = os.path.join(root, dir_name)
            if not os.listdir(current_dir) or any(keyword in dir_name for keyword in keywords):
                try:
                    shutil.rmtree(current_dir)
                    print(f"Removing directory: {current_dir}")
                except Exception as e:
                    print(f"Failed to remove {current_dir}: {e}")


if __name__ == "__main__":
    root_directory = "D:\\OSPanel\\domains\\vokzal-simferopol.info"
    keywords = ["feed", "fshare", "%3f"]

    try:
        remove_directories(root_directory, keywords)
        print("Target directories removed successfully.")
    except Exception as e:
        print(f"Error: {e}")
