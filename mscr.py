import numpy as np
import cv2
import csv

##
marker_dpi = 144
scan_dpi = 288

marker=cv2.imread('m_mk.jpg',0)

w,h = marker.shape[::-1]
#print(w,h)

#marker = cv2.resize(marker,(int(h*scan_dpi/marker_dpi),int(w*scan_dpi/marker_dpi)))

img = cv2.imread("mm.jpg",0)

res = cv2.matchTemplate(img,marker,cv2.TM_CCOEFF_NORMED)

threshold = 0.7
loc = np.where(res >= threshold)
print(loc)

mark_area={}
mark_area['top_x']= min(loc[1])
mark_area['top_y']= min(loc[0])
mark_area['bottom_x']= max(loc[1])
mark_area['bottom_y']= max(loc[0])


img0 = img[mark_area['top_y']:mark_area['bottom_y'],mark_area['top_x']:mark_area['bottom_x']]

cv2.imwrite('res0.png',img)

#print(mark_area)

mark_area['top_x']= 358
mark_area['top_y']= 860
mark_area['bottom_x']= 532
mark_area['bottom_y']= 1400

#270
x_ofst = 273
result = []

for i in range(2):
    mark_area['top_y'] += i*820
    mark_area['bottom_y'] += i*820

    for j in range(10):
        img = img0[mark_area['top_y']:mark_area['bottom_y'],mark_area['top_x']+j*x_ofst:mark_area['bottom_x']+j*x_ofst]
        #print(j)
        cv2.imwrite('res.png',img)


        ### ブラーをかける
        img = cv2.GaussianBlur(img,(5,5),0)

        ### 50を閾値として2値化
        res, img = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        ### 白黒反転
        img = 255 - img
        name = 'res1'+ str(i) + '_'+ str(j) + '.png'
        cv2.imwrite(name,img)

        ### 結果を入れる配列を用意


        ### 行ごとの処理(余白行を除いて処理を行う)
        for row in range(10):

            ### 処理する行だけ切り出す
            tmp_img = img [row*54:(row+1)*54,]
            cv2.imwrite('res2.png',tmp_img)
            area_sum = [] # 合計値を入れる配列

            ### 各マークの処理
            for col in range(4):

            ### NumPyで各マーク領域の画像の合計値を求める
                #print(np.sum(tmp_img[:,col*44:(col+1)*44]))
                area_sum.append(np.sum(tmp_img[:,col*44:(col+1)*44]))
            #print(area_sum)
            #print(np.median(area_sum) * 3)
            ### 画像領域の合計値が，中央値の3倍以上かどうかで判断
            #result.append(area_sum > np.median(area_sum) * 3)
            result.append(area_sum == np.max(area_sum))

#print(result)
ans=["A","B","C","D"]
ast=[]
for x in range(len(result)):
    res = np.where(result[x]==True)[0]
    #print(res[0])
    ast.append(ans[res[0]])
    #print(res)
    if len(res)>1:
        print('Q%d: ' % (x+1) + ans[res[0]] + ' ## 複数回答 ##')
    elif len(res)==1:
        print('Q%d: ' % (x+1) + ans[res[0]])
    else:
        print('Q%d: ** 未回答 **' % (x+1))
#print(ast)


f = open("/Users/yotsuyataihei/myp/MKST/ANS.csv","r",encoding="utf-8")
answers = list(csv.reader(f))
f.close()
answers = np.array(answers)
answers = answers[2:3,1:]
answers = np.ravel(answers)
#print(m_past)

mres = ast == answers
#print(ast == answers)

P1=mres[:6]
P2=mres[6:31]
P3=mres[31:70]
P4=mres[70:100]
P5=mres[100:130]
P6=mres[130:146]
P7=mres[146:200]
if np.sum(P1) == 6:
    print("Part1 perfect!")
else:
    print("Part1 " + str(np.sum(P1)) + "answers correct")
    print(np.ravel(np.where(P1==False))+1,"incorrect")

if np.sum(P2) == 25:
    print("Part2 perfect!")
else:
    print("Part2 " + str(np.sum(P2)) + "answers correct")
    print(np.ravel(np.where(P2==False))+7,"incorrect")

if np.sum(P3) == 39:
    print("Part3 perfect!")
else:
    print("Part3 " + str(np.sum(P3)) + "answers correct")
    print(np.ravel(np.where(P3==False))+32,"incorrect")

if np.sum(P4) == 30:
    print("Part4 perfect!")
else:
    print("Part4 " + str(np.sum(P4)) + "answers correct")
    print(np.ravel(np.where(P4==False))+71,"incorrect")

if np.sum(P5) == 30:
    print("Part5 perfect!")
else:
    print("Part5 " + str(np.sum(P5)) + "answers correct")
    print(np.ravel(np.where(P5==False))+101,"incorrect")

if np.sum(P6) == 16:
    print("Part6 perfect!")
else:
    print("Part6 " + str(np.sum(P6)) + "answers correct")
    print(np.ravel(np.where(P6==False))+131,"incorrect")

if np.sum(P7) == 54:
    print("Part7 perfect!")
else:
    print("Part7 " + str(np.sum(P7)) + "answers correct")
    print(np.ravel(np.where(P7==False))+147,"incorrect")

#a=np.ravel(np.where(P7==False))
#print(P7)
#print(a+101)
#print(P1)
#print(P2)
#print(P3)
#print(P4)
#print(P5)
#print(P6)
#print(P7)
