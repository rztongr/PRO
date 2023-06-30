# encoding:utf-8
import os
import sys
import edlib
import time
import argparse
from tqdm import tqdm
from multiprocessing import Pool
import math

sys.path.append('module/pro_divergence')

from edit_distance import metric


def cut_sequencing_barcode(file_name, fr, en):
    # print(fr,en)
    z_f = 0
    z_e = 0
    if len(fr) != 8:
        z_f = len(fr)-8
    if len(en) != 8:
        z_e = len(en)-8
    seqs = {}
    tags = []
    with open(file_name, 'r') as f:
        h = 0
        text = f.read()
        lines = text.splitlines()
        for i in range(100):
            tag = lines[4*i].split(' ')[0]
            sequencing_seq_prefix = lines[4*i+1][35:70+z_f]
            a = edlib.align(fr, sequencing_seq_prefix, mode="HW", task="path")
            sequencing_seq_suffix = lines[4*i+1][35+24:121+z_e]
            b = edlib.align(en, sequencing_seq_suffix, mode="HW", task="path")
            f = a['editDistance']
            e = b['editDistance']
            if f <= 1 and e <= 1:
                start = a['locations'][-1][-1] + 35
                end = b['locations'][0][0]+35+24
                sequences = lines[4*i+1][start+1:end]
            elif f <= e:
                start = a['locations'][-1][-1] + 35
                sequences = lines[4*i+1][start+1:start+25]
            else:
                end = b['locations'][0][0]+35+24
                sequences = lines[4*i+1][end-24:end]
            seqs[tag] = sequences
    return seqs


def get_dex_barcode(cut_seqs_tag):
    barcode = "a"
    for key, value in cut_seqs_tag.items():
        max = 0
        for seq_2 in dataset:
            d = metric(seq_2, value)  # dataset,如果序列不是DNA AGCT序列
            if d > max:
                max = d
                barcode = seq_2
        cut_seqs_tag[key] = barcode
    return cut_seqs_tag


def read_file(path):
    datase = []
    with open(path, "r") as f:
        data = f.readlines()
        data.remove(data[0])
    for m in range(len(data)):
        line = data[m].strip('\n')
        datase.append(line.split(",")[-1])
    return datase


def get_flanking(path):
    line = []
    with open(path, "r") as f:
        data = f.readlines()
    for m in range(len(data)):
        line.append(data[m].strip('\n'))
    fr = line[1]
    en = line[3]
    return fr, en


def dex_6(file,i):
    if i==1:
        file_name = fastq_path + '/' + file
    else:
        file_name = fastq_path
    cut_seqs_tag = cut_sequencing_barcode(file_name, fr, en)
    dex_res = get_dex_barcode(cut_seqs_tag)
    output_file_name = output_file + '/dex_result' + '/' + file.split('.')[0]+'.txt'
    file = open(output_file_name, 'w')
    for key, value in dex_res.items():
        file.write(str(key)+': ')
        file.write(str(value)+'\n')
    file.close()


def initialization_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='fastq_path', type=str, required=True,
                        help='Sequencing results: the fastq files after sequencing.')
    parser.add_argument('-b', action='store', dest='barcode_path', type=str, required=True,
                        help='A csv file contains barcode sequences.')
    parser.add_argument('-f', action='store', dest='flankings', type=str, required=True,
                        help='A fastq file contains the flanking sequences used in the library preparation.')
    parser.add_argument('-o', action='store', dest='output_file', type=str, required=True,
                        help='The directory path to save the result files of demultiplexing.')
    # Optional
    parser.add_argument('-t', action='store', dest='threads', type=int, required=False, default=20,
                        help='Specify the number of threads, which affects the speed of demultiplexing.')
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    time_start = time.time()

    args = initialization_parameters()

    fastq_path = args.fastq_path
    barcode_path = args.barcode_path
    flankings = args.flankings
    threads = args.threads
    output_file = args.output_file
    
    dataset = read_file(barcode_path)
    fr, en = get_flanking(flankings)
    os.makedirs(output_file+'/dex_result')
    if os.path.isdir(fastq_path):
        fastq_files = os.listdir(fastq_path)
        p = Pool(20)
        for file in tqdm(fastq_files, ncols=100, mininterval=0.3):
            p.apply_async(dex_6, args=(file,1))
        p.close()
        p.join()
    else:
        dex_6(os.path.split(fastq_path)[-1],0)

    time_end = time.time()
    time_sum = time_end - time_start
    print("End Demultiplexing! Total run time: %fs" % (time_sum))
