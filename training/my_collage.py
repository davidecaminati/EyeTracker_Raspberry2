from PIL import Image

out = Image.new("RGB", (2000, 3000), "white")

#for line in open("myfile.txt"):
#x, y, name, pngfile = line.split()
n = 0
for y in range(10):
    for x in range(20):
        n = n + 1
        valore = '%03d' % n
        pngfile = "/home/pi/opencv-2.4.10/samples/python2/occhi_finito/" + valore + ".jpg"
        out.paste(Image.open(pngfile), (int(100*x), int(100*y)))

for y in range(10):
    for x in range(20):
        n = n + 1
        valore = '%03d' % n
        pngfile = "/home/pi/opencv-2.4.10/samples/python2/occhi_finito/" + valore + ".jpg"
        out.paste(Image.open(pngfile), (int(100*x), int(100*y+1000)))
        
        
n = n + 1

for y in range(10):
    for x in range(20):
        n = n + 1
        valore = '%03d' % n
        pngfile = "/home/pi/opencv-2.4.10/samples/python2/occhi_finito/" + valore + ".jpg"
        out.paste(Image.open(pngfile), (int(100*x), int(100*y+2000)))

out.save("out.png")