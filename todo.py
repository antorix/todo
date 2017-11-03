#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a very simple to-do list for Android. Requires QPython3 to run (download it from Google Play Market).

from androidhelper import Android
droid = Android()

# Find absolute path on Android 
path=droid.environment()[1]["download"][:droid.environment()[1]["download"].index("/Download")] + "/qpython/scripts3/tasks.txt"

def dialog_list(options):
    """Show tasks"""
    droid.dialogCreateAlert("\ud83d\udcc3 My Tasks (%d)" % len(options))
    droid.dialogSetItems(options)
    droid.dialogSetPositiveButtonText("\u2795")
    droid.dialogSetNegativeButtonText("Exit")
    droid.dialogSetNeutralButtonText("\u2702")
    droid.dialogShow()
    return droid.dialogGetResponse()[1]
    
def dialog_text(default):
    """Show text input"""
    droid.dialogCreateInput("\u2795 New Task", "Enter a new task:", default)
    droid.dialogSetPositiveButtonText("Submit")
    droid.dialogSetNeutralButtonText("Clear")
    droid.dialogSetNegativeButtonText("Cancel")
    droid.dialogShow()
    return droid.dialogGetResponse()[1]
    
def dialog_confirm(message):
    """Confirm yes or no"""
    droid.dialogCreateAlert("Confirmation", message)
    droid.dialogSetPositiveButtonText("Yes")
    droid.dialogSetNegativeButtonText("No")
    droid.dialogShow()
    return droid.dialogGetResponse().result        

# Run main cycle
while 1:
    
    # Open file
    try:
        with open(path) as file:
            tasks=file.readlines()
    except:
        droid.makeToast("File %s not found or opening error" % path)  
        tasks=[]
    
    # Show tasks and wait for user response
    response=dialog_list(tasks)
    
    # Process response
    if "item" in response: # delete individual task
        del tasks[response["item"]]
        droid.vibrate(200)
        droid.makeToast("Дело сделано!")
        droid.ttsSpeak("Дело сделано!")
            
    elif "which" in response:
        if "neutral" in response["which"]: # delete all tasks
            choice=dialog_confirm("Are you sure you want to wipe all tasks?")
            if choice!=None and "which" in choice and choice["which"]=="positive":
                tasks=[]                 
        elif "positive" in response["which"]: # create new task
            default=""
            while 1:
                input=dialog_text(default)
                if "canceled" in input:
                    default=input["value"]
                elif "neutral" in input["which"]: # clear input
                    default=""
                elif "positive" in input["which"]: # create new task
                    tasks.append(input["value"]+"\n")
                    droid.ttsSpeak("Новое дело!")
                    break
                else:
                    break                
        else:
            exit=True
    
    # Save tasks to file
    with open(path, "w") as file:
        for i in range(len(tasks)): file.write(tasks[i])        
    
    # If user chose to exit, break cycle and quit
    if exit==True:
        break
        
# Export tasks
choice=dialog_confirm("Do you want to export tasks?")
if choice!=None and "which" in choice and choice["which"]=="positive":
    droid.sendEmail("Email", "My Tasks", ''.join(tasks), attachmentUri=None)
