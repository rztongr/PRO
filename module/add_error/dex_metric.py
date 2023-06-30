# -*- coding:utf-8 -*-
import sys
from multiprocessing import  Pool
import argparse
import time
sys.path.append('module/pro_divergence')
from edit_distance import metric

def initialization_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', action='store', dest='barcode_path', type=str, required=True, help='barcode_path')
    parser.add_argument('-e', action='store', dest='barcode_error_path', type=str, required=True, help='barcode_error_path')
    args = parser.parse_args()
    return args

def read_file(path):
    dataset = []
    with open(path,"r") as f:  
        data = f.readlines()                                                
    for m in range(len(data)):
        dataset.append(data[m].strip('\n'))
    return dataset

def get_dex_barcode(i):
    max=0
    bar_err=barcode_error[i]
    for seq_2 in barcodes:
        d=metric(seq_2,bar_err)
        if d>max:
            max=d
            barcode=seq_2
    if barcode==barcodes[int(i/100)]:
        return 1
    else:
        return 0   


if __name__ == '__main__':
    time_start = time.time()

    args = initialization_parameters()
    barcode_path=args.barcode_path
    barcode_error_path=args.barcode_error_path 
    
    barcode_error=read_file(barcode_error_path)
    barcodes = read_file(barcode_path)
    print("len(barcode_error)",len(barcode_error))
    print("len(barcodes)",len(barcodes))
    

    p=Pool(20)
    result=[]
    for i in range(len(barcode_error)):
        result.append(p.apply_async(get_dex_barcode,args=(i,)))
    p.close()
    p.join()
    correct=0
    error=0
    for i in result:
         if int(i.get())==1:
            correct=correct+1
         elif int(i.get())==0:
            error=error+1
    print(correct/len(barcode_error))


    end_time = time.time()
    print('用时：', end_time -  time_start)

