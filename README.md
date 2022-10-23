# SyncFolderPython
One-way synchronization of two folders: source and backup with logging

- All the files in source folder will get updated to backup folder
- All the files in backup folder which is not present in source folder will get deleted
- If the file is present in both the folder and there is some changes made in the source folder, it will get updated in the backup folder.
- As this program is designed specifically for file backup, any directories within the source folder will not be copied to the backup folder.
- Finally, all directories within the backup folder will be deleted, and any directories within the source folder will be handled by the IsADirectoryError exception.

# Requirements

  * Python 3.7

> This code makes use of the `f"..."` or [f-string
> syntax](https://docs.python.org/3/reference/lexical_analysis.html#f-strings). This syntax was
> introduced in Python 3.6.


# Sample Execution & Output

```Bash
git clone https://github.com/nishikantjha/SyncFolderPython.git
```
```Bash
cd SyncFolderPython
```

Run sync.py file

```Bash
python3 sync.py
```

#### Following the execution of the Python file, four inputs must be provided.

1. Log file path
2. Synchronization Period : Enter the time interval(in seconds) in which you need to sync the folders or by default, it will take **30 seconds**.

##### When you run the Python file for the first time, config.txt will be created in the current folder with the source and backup values you entered. Thereafter, it will be updated each time you run the program and enter new source and backup values; if you don't enter any source or backup values, it will use the values from config.txt.

3. Source folder path
4. Backup folder path

