import time

def init():
#db
    global old_time_list
    old_time_list = None

    global old_time_dict
    old_time_dict = None

    global list_all_coins
    list_all_coins = []

    global dic_all_coins
    dic_all_coins = {}

def time_confirmation(old_time):
    print("time_confirmation")
    return old_time is not None and time.time() - old_time < 3600

def time_update():
    print("time_update")
    return time.time()

