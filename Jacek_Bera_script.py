from pandas.io.json import json_normalize
import json
import matplotlib.pyplot as plt
import os
import pandas as pd
import tarfile


def extract_archive():
    """
    Function for extracting tar archive with exception handling
    """
    try:
        package = tarfile.open("interview_fse_data.tar.gz", "r:gz")
        package.extractall()
    except IOError:
        print("File not found!")
    finally:
        package.close()


def conv2pandas():
    """
    Function for converting files to pandas DataFrame
    """
    global result_df
    result_df = pd.DataFrame()
    indir = os.getcwd() + '\out'
    for root, dirs, filenames in os.walk(indir):
        # Loop for checking each file
        for f in filenames:
            print("Reading file:", f)
            fullpath = os.path.join(indir, f)
            my_list = []
            # Open file with JSON objects
            try:
                with open(fullpath, encoding='utf8') as f:
                    for line in f:
                        line = line.replace('\\', '')
                        my_list.append(json.loads(line))

                result_temp = json_normalize(my_list)
                # Convert time parameters
                result_temp['eventHeader.timeStamp'] = pd.to_datetime(result_temp['eventHeader.timeStamp'], unit='ms')
                result_temp['eventBody.targetCreationTime'] = pd.to_datetime(result_temp['eventBody.targetCreationTime'], unit='ms')
                result_df = result_df.append(result_temp, ignore_index=True)
            except IOError:
                print("File not found!")


def plot_actions():
    """
    Function for displaying statistics of actions
    """
    result_temp = result_df['eventBody.action'].value_counts(ascending=True)
    print(result_temp)
    result_temp.plot(kind='bar', color='b')
    plt.title("Plot of actions")
    plt.show(block=True)


def plot_users():
    """
    Function for displaying statistics of users - TOP 50
    """
    result_temp = result_df['eventBody.userId'].value_counts(ascending=True).iloc[-50:]
    print(result_temp)
    result_temp.plot(kind='bar', color='g')
    plt.title("Plot of users")
    plt.show(block=True)


def plot_workgroups():
    """
    Function for displaying statistics of workgroups - TOP 50
    """
    result_temp = result_df['eventHeader.workgroupID'].value_counts(ascending=True).iloc[-50:]
    print(result_temp)
    result_temp.plot(kind='bar', color='r')
    plt.title("Plot of workgroups")
    plt.show(block=True)


def plot_lang():
    """
    Function for displaying user keyboard statistics
    """
    result_temp = result_df['eventHeader.userAgent'].str.split().str.get(3)
    result_temp = result_temp[result_temp.str.contains('^(?=.*[a-z])(?=.*[A-Z])(?=.*_).+$', na=False)]
    result_temp = result_temp.value_counts(ascending=True)
    print(result_temp)
    result_temp.plot(kind='bar', color='k')
    plt.title("Plot of languages")
    plt.show(block=True)


def check_missing():
    """
    Function for displaying missing values
    """
    print("Missing values per row:")
    print(result_df.apply(num_missing, axis=0))  # axis=1 defines that function is to be applied on each row


def num_missing(x):
    """
    Function for checking for missing values
    """
    return sum(x.isnull())


def check_duplicates():
    """
    Function for checking for duplicates
    """
    result_temp = result_df[result_df.duplicated]
    if result_temp.empty:
        print("There are no duplicates")
    else:
        print(result_temp)


def choose():
    """
    Function for operating the script
    """
    print("Welcome to data statistics interface.")
    print("Lets try to extract file and convert to DataFrame")
    if os.path.exists('./out'):  # os.path.exists(os.path.join(os.getcwd(), 'out')):
        print("File already extracted")
    else:
        print("Extracting file")
        extract_archive()
        print("File extracted")
    conv2pandas()
    print("Data imported")
    answer = None
    while answer != '0':
        answer = input("""
        - Press 1 for simple row
        - Press 2 for general info
        - Press 3 for data and plot of actions
        - Press 4 for data and plot of 50 most active users
        - Press 5 for data and plot of 50 most active workgroups
        - Press 6 for data and plot of user keyboard langauges
        - Press 7 if you want to check data for missing values
        - Press 8 if you want to check data for duplicates
        
        - Press 0 for exit.   
        """)
        if answer == '1':
            print("Simple row of file (transposed)")
            print(result_df.loc[0].T)
        elif answer == '2':
            print("Dataset general info")
            print(result_df.info())
        elif answer == '3':
            print("Actions: data and plot")
            plot_actions()
        elif answer == '4':
            print("TOP 50 most active users: data and plot")
            plot_users()
        elif answer == '5':
            print("TOP 50 most active workgroups: data and plot")
            plot_workgroups()
        elif answer == '6':
            print("Keyboard language (users nationality) data and plot")
            plot_lang()
        elif answer == '7':
            print("Checking for missing data (NaN and None)")
            check_missing()
        elif answer == '8':
            print("Checking for duplicates")
            check_duplicates()
        elif answer == '0':
            print("See you later")

choose()