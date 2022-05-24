from pathlib import Path
from PIL import Image
from config import Config
from datetime import datetime,timedelta
import shutil
import os

UPLOAD_FOLDER=Config.UPLOAD_FOLDER

c=[0,0,0] # will store average r,g,b values for each pf_block i.e pf*pf

def remove_directory():  # will remove puzzle 2 from today

    remove_date=datetime.strftime(datetime.now() - timedelta(2), '%m-%d-%Y')
    path=UPLOAD_FOLDER+ remove_date
    try:
        shutil.rmtree(path)
    except OSError:
        print ("del of the directory %s failed" % path)
        return False
    else:
        print ("del of the directory succeeded %s " % path)
        return True

def create_directory():
    today=datetime.strftime(datetime.now(), '%m-%d-%Y')
    path=os.getcwd()+'/app/static/images/'+ str(today)

    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
        return False
    else:
        print ("Successfully created the directory %s " % path)
        return True
    pass
def create_new_puzzle():

    today=datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%Y')
    remove_directory()
    create_directory()
    #image=[(img path,today)]pull image frmo db using (today)
    #populate_directories(image)
    

def get_dates():
    dates=[]

    yesterday=datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%Y') 
    dates.append(yesterday)
    
    today=datetime.strftime(datetime.now(), '%m-%d-%Y')
    dates.append(today)
    tomorrow=datetime.strftime(datetime.now() + timedelta(1), '%m-%d-%Y') 
    dates.append(tomorrow)

    return dates

def create_directories():
    dates=get_dates()
    for date in dates:
        path=UPLOAD_FOLDER+ date
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)
    
def avg(l,k):
    return l//(k*k)

def iterateThroughKbox(k,Xoffset,Yoffset,pix):
    for i in range (k):
        for j in range (k):
            c[0]+=pix[i+Xoffset,j+Yoffset][0]
            c[1]+=pix[i+Xoffset,j+Yoffset][1]
            c[2]+=pix[i+Xoffset,j+Yoffset][2]
    return (avg(c[0],k),avg(c[1],k),avg(c[2],k))


def assignAvg(k,Xoffset,Yoffset,pix,avg):
    for i in range (k):
        for j in range (k):
            pix[i+Xoffset,j+Yoffset]=tuple(avg)
            
            
def doShit(k,i,j,pix):
    avg=iterateThroughKbox(k,i*k,j*k,pix)
    assignAvg(k,(i*k),j*k,pix,avg)
    c[0]=0
    c[1]=0
    c[2]=0

def get_images(dates):
    images=[]
    for date in dates:
        # pull image from db
        #image= (imagePath,date,pf)
        pass

    return []




def populate_directories(images):
    if len(images)==1: 
        pass
    else:
        print('im here')
        pixelelate(images)

def initialiseGame():
    dates=get_dates
    create_directories() # create 3 directories with yesterday,today's, and tomorrow's dates in that order
    #images=get_images(dates)# return a list of tuples in the format (path to image,date associated with image,pixelFactor)
    images=[ ('bmo.png','05-24-2022',[2,4,6,8,10]),
            ('finn.png','05-25-2022',[2,4,6,8,10]),
            ('has.jpg','05-26-2022',[2,4,6,8,10])

    ]
    populate_directories(images) # populate directories with pixelated images
   


def pixelelate(images): #@params list of tupples [(image name(string),date(string),pixel factor(lst of ints))]
    print('in pixel')
    for image in images:
        image_name=image[0]
        image_date=image[1]
        pixel_factor=image[2]
        img_path= UPLOAD_FOLDER+'images/'+image_name
        print(img_path)
        im = Image.open(img_path)

        pix = im.load()
        row=im.size[0]
        col= im.size[1]
        count=len(pixel_factor)+1
        for pf in pixel_factor:
            if pf!=0:
                block_row=row//pf # creating a block of area pf*pf to go through the image
                block_col=col//pf
                for i in range(block_row):
                    for j in range(block_col):
                        doShit(pf,i,j,pix)
            count-=1
            print(image_date)
            destination=UPLOAD_FOLDER+image_date+'/'+str(count)+image_name[-4:] #UPLOAD_FOLDER+image_date+'/'+str(count)+image_name[-4:]
            print(destination)
            im.save(destination)


#create_directories()
#remove_directory()
#initialiseGame()