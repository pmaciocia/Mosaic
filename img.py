import Image
import os
import math
import psyco
psyco.full()


def mosaic(src,dir,resize=(320,240),ratio=25):
    try:
        img = Image.open(src)
    except IOError,e :
        print e
        return
   
    images = load_dir(dir,resize)
    seg = seg_src(src,resize,ratio)

    s = seg[-1][0]
    #s = (s[0]+resize[0],s[1]+resize[1])
    mos = Image.new('RGB',s)
    
    for x,y in seg:
        mos.paste(min([(reldist(y,z),w) for w,z in images])[1],x)
    #mos = Image.new('RGB',(resize[0]*(img.size[0]/ratio),resize[1]*(img.size[1]/ratio)))
    #mos.save('mosaic.jpg','jpeg')
    return mos

def load_dir(dir, resize=(320,240)):
    files = [os.path.join(dir,x) for x in os.listdir(dir) if not x.endswith('.db')]
    images = []
    for f in files:
        print f
        img = Image.open(f)
        img = img.resize(resize)
        img = img.convert('RGB')
        images.append((img,avg(img)))
        
    return images

def avg_dir(dir):
    files = [os.path.join(dir,x) for x in os.listdir(dir)]
    avgs = [(x,avg(x)) for x in files]
    return avgs 

def seg_src(path,img_size=(320,240),ratio=25):
    try:
        img = Image.open(path)
    except IOError,e :
        print e
        return

    width, height = img.size
    if not img.mode is 'RGB':
        img = img.convert('RGB')
    
    segs = []
    
    wr = width/ratio
    hr = height/ratio
    
    sx = img_size[0]/wr
    sy = img_size[1]/hr

    for x in xrange(0,width,wr):
        for y in xrange(0,height,hr):
            #segs.append(((x*img_size[0])/wr,(y*img_size[1])/hr),avg(img,(x,y,min(x+wr,width),min(y+hr,height)))))
            segs.append(((x*sx,y*sy),avg(img,(x,y,min(x+wr,width),min(y+hr,height)))))
    
    return segs


def avg(img,area=None,path=None):
    if not img:
        try:
            img = Image.open(path)
        except IOError,e :
            print e
            return

    width, height = img.size
    if not img.mode is 'RGB':
        img = img.convert('RGB')
    
    if area is None:
        area = (0,0,width,height)

    avg = [0] * len(Image._MODEINFO[img.mode][2])
    for xy in iterarea(area):
        p = img.getpixel(xy)
        #for x in xrange(len(avg)):
            #avg[x] += p[x]
        avg = map(sum,zip(avg,list(p)))
    
    size = (area[3]-area[1])*(area[2]-area[0])
    return tuple([x/size for x in avg])

def reldist(a,b):
    #total = 0
    #for x,y in enumerate(a):
        #total += (y-b[x])**2
    
    #return total

    return sum((a[x]-b[x])**2 for x in xrange(len(a))]))

def pixdist(a,b):
    return math.sqrt(sum([(a[x]-b[x])**2 for x in xrange(len(a))])))

def iterarea(area):
    for x in xrange(area[0],area[2]):
        for y in xrange(area[1],area[3]):
            yield (x,y)

    
