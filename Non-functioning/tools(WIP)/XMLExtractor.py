import os , string

path = "C:\\Program Files (x86)\\ASRock Utility\\ASRRGBLED\\Model"

ReadFileList = open("XMLList.txt",'a')
if os.path.exists(path):
    for Root, Dirs, Files in os.walk(path):
        for file in Files:
            if file == "Model.xml":
                Fname = Root.rsplit("\\")[-1]
                F = os.path.join(Root,file)
                ReadF = open(F,'r')
                blankindex = [[None],[None],[None],[None],[None],[None]]
                while True:
                    line = ReadF.readline()
                    if "<Item" in line:
                        _ , Continue = line.split('Index="')
                        index , Continue = Continue.split('" ChannelId="')
                        ChannelId , Continue = Continue.split('" Name=')
                        Name , _ = Continue.split('/>')
                        try:
                            blankindex[int(ChannelId)] = Name
                        except:
                            pass
                    if line == "":
                        ReadFileList.write("%s %s \n"%(Fname,blankindex))
                        print(blankindex)
                        break
else:
    trypath = input("if you installed in a non standard location or are using a polychrome 1.x.x version please @coffeeislife in the openRGB discord \n(if you have a folder of XML files with the correct structure for polychrome the you can enter the path here)")

    if os.path.exists(trypath):
        for Root, Dirs, Files in os.walk(trypath):
            for file in Files:
                if file == "Model.xml":
                    Fname = Root.rsplit("/")[-1]
                    F = os.path.join(Root,file)
                    ReadF = open(F,'r')
                    blankindex = [[None],[None],[None],[None],[None],[None]]
                    while True:
                        line = ReadF.readline()
                        if "<Item" in line:
                            _ , Continue = line.split('Index="')
                            index , Continue = Continue.split('" ChannelId="')
                            ChannelId , Continue = Continue.split('" Name=')
                            Name , _ = Continue.split('/>')
                            try:
                                blankindex[int(ChannelId)] = Name
                            except:
                                pass
                        if line == "":
                            ReadFileList.write("%s %s \n"%(Fname,blankindex))
                            print(blankindex)
                            break
    else:
        input("it looks like you entered the wrong path")