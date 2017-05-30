'''
Author: Ekram
Library which will store variables during run time in text files for long duration.
Can be used as volatile or permanent memory. Mainly needed as a way of communicating between
external scripts and pass around variables since python cant access permanent memory locations
easily. 
Alternatives to this library with faster fetch times but more complexity:
    -pickle
    -sqlite3
    -json
    -weakref
    -shelve
Use the above if optimization and response time is very important along with memory space.
Otherwise this library will get the job done 
'''

import os

def Store_Single_Data(memory_name, data):
    '''
    Function to store single data permanently 
    INPUTS:
        memory_name = permanent name of the memory location. Can be accessed via this
        data = the data that is going to be written to this location as a string
    '''

    Volatile_Memory_Location = (id(data))

    text_file_name = str(memory_name) + '.txt'

    with open(text_file_name, 'w') as f:
        f.write(str(data) + str(Volatile_Memory_Location))

def Read_Single_Data(memory_name):
    '''
    Function which will read from memory location
    INPUTS:
        memory_name = memory location
    OUTPUTS:
        returns memory location data as a string
    '''

    text_file_name = str(memory_name) + '.txt'

    Does_Memory_Location_Already_Exist = False

    Current_Directory_Content = os.listdir()

    for line in Current_Directory_Content:
        if line==text_file_name:
            Does_Memory_Location_Already_Exist = True

    if Does_Memory_Location_Already_Exist==False:
        raise Exception('Specified memory location does not exist. Check caps lock and make sure it is passed in as a string')

        return None

    with open(text_file_name, 'r') as f: 
        while True:
            try:
                content = f.read().splitlines() 
                content_final = content[0]
            except IndexError:
                pass
            if content_final!=None:
                break

    return (content_final)

def Destroy_Memory_Location(memory_name):
    '''
    Deletes the text file with specified memory name
    '''

    text_file_name = str(memory_name) + '.txt'    

    os.remove(text_file_name)

def Store_List_Data(memory_name, data_list): 
    '''
    Function to store a python list/array permanently 
    INPUTS:
        memory_name = permanent name of the memory location. Can be accessed via this input
        data_list = the data list that is going to be written to this location as a string line by line
    '''

    text_file_name = str(memory_name) + '.txt'

    with open(text_file_name, 'w') as f:
        for data in data_list:
            f.write(str(data) + ',')

def Read_List_Data(memory_name):
    '''
    Function which will return the list in specified memory name location
    '''

    text_file_name = str(memory_name) + '.txt'

    Does_Memory_Location_Already_Exist = False

    Current_Directory_Content = os.listdir()

    for line in Current_Directory_Content:
        if line==text_file_name:
            Does_Memory_Location_Already_Exist = True

    if Does_Memory_Location_Already_Exist==False:
        raise Exception('Specified memory location does not exist. Check caps lock and make sure it is passed in as a string')

        return None

    with open(text_file_name, 'r') as f: 
        while True:
            try:
                content = f.read().splitlines()
                content_to_split = content[0].split(',')
                content_to_split.pop(-1)

            except IndexError:
                pass
            if len(content_to_split)!=0:
                break

    return (content_to_split)



