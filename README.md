# SyncFolderPython
One-way synchronization of two folders: source and backup with logging

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

There will be 3 input that needs to be provided after you run the python file.

- Log file Path : Input the path to the log file if needed; else, **log.txt** will be created automatically in the current folder..
- Synchronization Period : Enter the time interval(in seconds) in which you need to sync the folders or by default, it will take **30 seconds**.

#### When you run the Python file for the first time, config.txt will be created in the current folder with the source and backup values you entered. Thereafter, it will be updated each time you run the program and enter new source and backup values; if you don't enter any source or backup values, it will use the values from config.txt.

- Source and Backup folder path : (**Default** of which will be present in **config.txt** file after the first run)
