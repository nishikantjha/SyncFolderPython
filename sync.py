import os, time, logging, shutil
from hashlib import md5
from datetime import datetime as dt


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
    files = os.listdir(source)
    files_backup = [f for f in os.listdir(backup) if os.path.isfile(os.path.join(backup, f))]
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
    # check if folder exists
    if os.path.isdir(folder):
        print(f'{name} path: OK')
        logging.info(f'{name} path: OK')
    else:
        logging.error(f'{name} path: DOES NOT Exists')
        print(f'{name} path does not exists')
        print(f'Please check if the {name} path is correct')
        exit() 

def checkLogFile(file):
    if os.path.isfile(file):
        print(f'Log path: OK')
    else:
        print(f'Log file path at "{file}": DOES NOT Exists')
        print(f'Please check if the "{file}" path is correct')
        exit() 

def writeConfig(source, backup):
    with open('config.txt', 'w') as f:
        f.write('folder:'+source)
        f.write('\n')
        f.write('backup:'+backup)   

if __name__=="__main__":
    #input log file
    LogFile = input('Please enter your log path: ').strip()
    while LogFile=="":
        print('log path cannot be empty')
        LogFile = input('Please enter your log path: ').strip()

    checkLogFile(LogFile)

    logging.basicConfig(filename=LogFile, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='[%Y-%m-%d %H:%M:%S]', level=logging.DEBUG)
   
    #Logging starts here
    logging.info('Begin')

    while True:
        try:
            syncInterval = int(input('Default: 30 or Please enter Time Interval you need for Synchronization(in seconds): ') or 30)
            print(f'Time Interval for Synchronization: {syncInterval}')
            logging.info(f'Time Interval for Synchronization: {syncInterval}')
        except ValueError:
            print("\nPlease only use integers")
            continue
        break

    if os.path.isfile('config.txt'):
        print(f"\nconfig file: Present at {os.getcwd()}")
        with open('config.txt') as f:
            lines = f.readlines()
        logging.info(f'config file: Present')

        print("\n\nTo change the config file with new source and folder paths: ")
        print('\nPress Just "Enter" for default paths for source and backup')
        with open('config.txt', 'r') as f:
            lines = f.readlines()
            default_source = lines[0].partition(':')[2].strip()
            source = input('Input your source folder path:').strip() or lines[0].partition(':')[2].strip()
            
            # check if source folder exists
            checkFolder(source, 'source')
            default_backup = lines[1].partition(':')[2].strip()
            backup = input('Input your backup folder path:').strip() or lines[1].partition(':')[2].strip()
            
            # check if backup folder exists
            checkFolder(backup, 'backup')
            
            # Update config.txt
            writeConfig(source, backup)
            if default_source==source and default_backup==backup:
                print(f'config file: OK')
                logging.info('config file: OK')
            else:
                print('config file is updated')
                logging.info('config file: Updated')
        
    else:
        logging.error('config file: NOT FOUND')
        print("config file: NOT FOUND")
        # create config folder
        print("To create config file: ")
        source = input('Input your source folder path:')
        
        # check if folder exists
        checkFolder(source, 'source')
        backup = input('Input your backup folder path:')
        
        # check if backup exist
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
        files_backup = [f for f in os.listdir(backup) if os.path.isfile(os.path.join(backup, f))]
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
                    shutil.copy(f"{source}/{file}", backup)
                    print(f'{file} is updated')
                    logging.info(f'{file} is updated')

            if file not in files:
                # delete file in backup
                os.remove(backup+'/'+file)
                print(f'{file} is deleted')
                logging.info(f'{file} is deleted')
                deletedFile += 1
                

        for file in files:
            if file not in files_backup:
                # copy file from folder to backup
                try:
                    shutil.copy(f"{source}/{file}", backup)
                    createdFile += 1
                    print(f'{file} is created')
                    logging.info(f'{file} is created')
                except IsADirectoryError:
                    print(f"Error: {file} is a directory")
                    logging.error(f"Error: {file} is a directory")
                
        
        #Removing directories in backup folder if any
        list_backup = os.listdir(backup)

        for file in list_backup:
            if os.path.isdir(backup+'/'+file):
                shutil.rmtree(backup+'/'+file)
                print(f'Deleted {file} folder of backup')
                logging.info(f'Deleted {file} folder of backup')
                deletedFile += 1
        
        now = dt.now().isoformat(' ', 'seconds')
        print(f'[{now}] newlyCreatedFile: {createdFile}; updated: {updatedFile}; deleted: {deletedFile}; uptoDate: {similarFile}')

        # sleep for 30 sec by default(or input interval)
        time.sleep(syncInterval)

    
