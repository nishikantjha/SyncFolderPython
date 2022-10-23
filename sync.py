
import os
from hashlib import md5
from datetime import datetime as dt
import time
import logging


print('Press Just "Enter" for default values')
LogFile = input('Default log path (./log.txt) or Please enter your own log path: ').strip() or 'log.txt'

logging.basicConfig(filename=LogFile, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='[%Y-%m-%d %H:%M:%S]', level=logging.DEBUG)

while True:
    try:
        syncInterval = int(input('Default: 30 or Please enter Time Interval you need for Synchronization(in seconds): ') or 30)
    except ValueError:
        print("\nPlease only use integers")
        continue
    break

#Compare Files
def compareFiles(file1, file2):
    
    f1 = md5(open(file1, 'rb').read()).hexdigest()
    f2 = md5(open(file2, 'rb').read()).hexdigest() 
    if f1==f2:
        return True
    else:
        return False

#Compare Folders checking all the files present in backup folder as in source folder
def compareFolder(folder, backup):

    #List all files in source and backup folder
    files = os.listdir(folder)
    files_backup = os.listdir(backup)
    #compare listed files length
    if len(files) != len(files_backup):
        return False

    #compare each file's hash is identical inside the folders

    for file in files:
        if file in files_backup:
            if not compareFiles(folder+'/'+file, backup+'/'+file):
                return False
        else:
            return False
    return True

def checkFolder(folder, name):
    # check if folder is exist
    if os.path.isdir(folder):
        print(f'{name} path: OK')
        logging.info(f'{name} path: OK')
    else:
        logging.error(f'{name} path: DOES NOT Exists')
        print(f'{name} path does not exists')
        print(f'Please check if the {name} path is correct')
        exit() 

def writeConfig(source, backup):
    with open('config.txt', 'w') as f:
        f.write('folder:'+source)
        f.write('\n')
        f.write('backup:'+backup)   

if __name__=="__main__":
    logging.info('Begin')

    if os.path.isfile('config.txt'):
        print(f"\nconfig file: Present at {os.getcwd()}")
        os.system("cat config.txt")
        logging.info(f'config file: Present')

        print("\n\nTo change the config file with new source and folder paths: ")
        print('\nPress Just "Enter" for default paths for source and backup')
        with open('config.txt', 'r') as f:
            lines = f.readlines()
            source = input('Input your source folder path:').strip() or lines[0].split(':')[1].strip() 
            # check if source folder exists
            checkFolder(source, 'source')
            backup = input('Input your backup folder path:').strip() or lines[1].split(':')[1].strip()
            # check if backup folder exists
            checkFolder(backup, 'backup')
            # Update config.txt
            writeConfig(source, backup)
            print(f'config.txt file is changed and created at {os.getcwd()}')
            logging.info('config file: Changed')
        
    else:
        logging.error('config file: NOT FOUND')
        print("config file: NOT FOUND")
        # register folder
        print("To create config file: ")
        source = input('Input your source folder path:')
        # check if folder is exist
        checkFolder(source, 'source')

        backup = input('Input your backup folder path:')
        # check if backup is exist
        checkFolder(backup, 'backup')
        # write config
        writeConfig(source, backup)
        print(f'config.txt file is created at {os.getcwd()}')
        logging.info('config file: CREATED')

    # run loop every 30 seconds by default(or input interval)

    while True:

        # Compare Source Folder with Backup
        if compareFolder(source, backup):
            # check folder
            now = dt.now().isoformat(' ', 'seconds')
            print(f'[{now}] file is up to date')
            logging.info('file is up to date')
            # sleep for 30 sec by default(or input interval)
            time.sleep(syncInterval)
            continue    

        # check file hash in folder and compare with backup
        createdFile = 0
        updatedFile = 0
        deletedFile = 0
        similarFile = 0

        # get all file in folder
        files = os.listdir(source)
        # get all file in backup
        files_backup = os.listdir(backup)
        # compare 2 list
        for file in files_backup:
            if file in files:
                if compareFiles(source+'/'+file, backup+'/'+file):
                    similarFile += 1
                    print(f'{file} is up to date')
                    logging.info(f'{file} is up to date')
                else:
                    # copy file from folder to backup
                    updatedFile += 1
                    os.remove(backup+'/'+file)
                    os.system('cp "'+source+'/'+file+'" '+backup)
                    print(f'{file} is updated')
                    logging.info(f'{file} is updated')
            if file not in files:
                # delete file in backup
                print(f'{file} is deleted')
                logging.info(f'{file} is deleted')
                deletedFile += 1
                os.remove(backup+'/'+file)

        for file in files:
            if file not in files_backup:
                # copy file from folder to backup
                createdFile += 1
                print(f'{file} is created')
                logging.info(f'{file} is created')
                os.system('cp "'+source+'/'+file+'" '+backup)



        now = dt.now().isoformat(' ', 'seconds')
        print(f'[{now}] newlyCreatedFile: {createdFile}; updated: {updatedFile}; deleted: {deletedFile}; uptoDate: {similarFile}')

        # sleep for 30 sec by default(or input interval)
        time.sleep(syncInterval)

    
