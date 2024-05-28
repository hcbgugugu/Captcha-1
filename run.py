import torch
import torch.nn as nn
from Testmodel import CNN
from datasets import CaptchaData
from torchvision.transforms import Compose, ToTensor
import pandas as pd
import os
from PIL import Image
import matplotlib.pyplot as plt

model_path = './checkpoints/modeltest.pth'
testpath = './data/test/'


source = [str(i) for i in range(0, 10)]
source += [chr(i) for i in range(97, 97+26)]
source += [chr(i) for  i in range(65,65+26)]
alphabet = ''.join(source)

def run():
    img_list = os.listdir(testpath)
    #img_list.sort(key=lambda x:int(x.split('.')[0]))
    img_li = list()
    label_li = list()
    # print(img_list)
    hw=[]
    correct=0
    for item in img_list:
        imgpath = os.path.join(testpath,item)
        img = Image.open(imgpath)
        trans = ToTensor()
        img_tensor = trans(img)
        cnn = CNN()
        if torch.cuda.is_available():
            cnn = cnn.cuda()
            cnn.eval()
            cnn.load_state_dict(torch.load(model_path))
        else:
            cnn.eval()
            model = torch.load(model_path, map_location='cpu')
            cnn.load_state_dict(model)
        img_tensor = img_tensor.view(1, 3, 40, 120).cuda()
        output = cnn(img_tensor)
        output = output.view(-1, 62)
        output = nn.functional.softmax(output, dim=1)
        output = torch.argmax(output, dim=1)
        output = output.view(-1, 4)[0]
        label = ''.join([alphabet[i] for i in output.cpu().numpy()])
        id = "".join(item)
        print("ID:",id , "label:",label)
        hw.append(id.strip().split('.')[0]+'\t'+label.strip())
        img_li.append(img)
        label_li.append(label)
    #####
        if label.strip() == id.split('_')[0].strip():
            correct += 1
    print('Acc:'+str(correct/len(img_list)))
    hw.sort(key=lambda item:eval(item.split('\t')[0]),reverse=False)
    with open('22920212204054.txt','w') as f:
        for item in hw:
            f.write(item+'\n')
    print('Having written into 22920212204054.txt.')
    #####
    for i in range(1,11):
        plt.subplot(5,2,i)
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.15, hspace=1.5)
        plt.imshow(img_li[i-1])
        plt.title("predict result:{}".format(label_li[i-1]))
    plt.show()



if __name__=="__main__":
    run()
