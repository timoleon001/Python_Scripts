import os
import shutil  # Importing shutil for rmtree


def remove_directories(root_directory, keywords):
    """
    Remove directories that are either empty or contain specific keywords in their names, including all their contents.
    :param root_directory: The root directory to start the removal process from.
    :param keywords: A list of keyword strings. If a directory name contains any of these keywords, or it's empty, it will be removed along with all its contents.
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
    root_directory = "D:\\OSPanel\\domains\\ekburg.tv"
    keywords = ["feed", "fshare", "%3f"]

    try:
        remove_directories(root_directory, keywords)
        print("Target directories removed successfully.")
    except Exception as e:
        print(f"Error: {e}")
