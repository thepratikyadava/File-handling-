from pathlib import Path
import os

def createfile():
    try:   
        name = input("Tell the name of your file you want to create:-")
        path = Path(name)
        if path.exists():
            print("Thore se app kam dimaag wale ho kya file already exist karta hai us naam ka")
        else:
            with open(path,"w") as cc:
                data = input("If you want to add something in your file provide:-")
                cc.write(data)
            print(f"File name {name} created successfully")
    except Exception as errr:
      print(f"an error occurred as {errr}")
  

def updatefile():
    try:
       path = Path(input("Name of file you want to update:-"))
       if path.exists():
          print("FOR ADDING CONTENT ENTER 1")
          print("FOR RENAMING FILE ENTER 2" )
          print("FOR OVERWRITINNG CONTENT ENTER 3")
          gg = int(input("Now just tell what do you want to do:-"))
          if gg ==1:
             with open(path,"a") as frt:
                deta = input("ENTER THE CONTENT YOU Want to add :- ")
                frt.write("\n" + deta )
             print(f"Successfully added content in file{path}")
          elif gg==2:
             inh = input("New name of your file")
             new_name = Path(inh)
             if not new_name.exists():
                path.rename(new_name)
                print(f"File {path} renamed to {inh} successfully")
             else:
                print(f"File with provide name {inh} exist")
          elif gg==3:
             with open(path,"w") as fde:
                vg = input("Enter the content :- ")
                fde.write(vg)
                print(f"Successfully overwrited")
       else:
          print("Sorry file dorsn't exist")       
    except Exception as fr:
       print(f"An error occured as {fr}")

def readfile():
    try:
        name = input("Tell name of your file to which you want to read:-")
        path = Path(name)
        if path.exists():
          with open(path ,"r") as fff :
            k = fff.read()
            print(f"Content of your file {name} is \n {k}")
        else:
            print(f"file with name {name} doesn't exist ")
    except Exception as free:
       print(f"An error occurred as {free}")
def deletefile():
 try:
        ju = Path(input("Name the file you want to delete :- "))
        if ju.exists():
            ju.unlink()
            print("File deleted successfully")
        else:
            print("File doesn't exist")
 except Exception as fcv:
    print(f"An error occurred as {fcv}")
print("Press 1 for creating a file ")
print("Press 2 for reading a file ")
print("Press 3 for updating a file ")
print("Press 4 for deleting a file ")
io = int(input("\n Tell your response :-"))
if io == 1:
   createfile()
elif io == 3:
   updatefile()
elif io == 2:
   readfile()
elif io == 4:
   deletefile()
else:
   print("Invalid entry")
