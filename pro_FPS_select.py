# encoding:utf-8
import random
import sys
import os
import shutil
import time
import argparse
from tqdm import tqdm
from multiprocessing import Pool

sys.path.append('module/pro_divergence')

from edit_distance import weight


def update(seq1, seq2, i):
    # print(i)
    d = weight(seq1, seq2, sequencing_accuracy)
    re = (i, d)
    return re


def thresh(num, l):
    thres = (sequencing_accuracy**l)*(((1/3)*(1/4)*(1-sequencing_accuracy))**num)
    return thres**2


def read_file(path):
    line = []
    with open(path, "r") as f:
        data = f.readlines()
    for m in range(len(data)):
        line.append(data[m].strip('\n'))
    return line


def pre_process():
    if input_path != 'None_file':
        if os.path.exists(input_path):
            input_d = read_file(input_path)
            if len(input_d) < quantity:
                print('Error!!! The number of sequences (quantity) after pre-processing should be greater than the number of sequences in the input.')
                sys.exit(0)
        else:
            print('Error!!! Input file does not exist.')
            sys.exit(0)

    os.mkdir(output_path)
    command_input_path = ' -i ' + input_path
    command_length = ' -l ' + str(barcode_length)
    command_output_file = ' -o ' + output_pre_path
    command_away_flankings = ' -f ' + flankings
    command_quantity = ' -q ' + str(quantity)
    command = 'python ./module/Pre_processing/pre_processing.py' + command_length + \
        command_output_file+command_quantity + command_away_flankings+command_input_path
    os.system(command)
    d = read_file(output_pre_path)
    print("len(dataset)", len(d))
    return d


def FPSselection():
    random.seed(se)
    sample_s = random.choice(dataset)
    print("1", sample_s)
    output_file_name = output_path+'/select_barcode.txt'
    file = open(output_file_name, "wb+", buffering=0)
    file.write(str(sample_s).encode('utf-8')+b"\n")

    temp = []
    sample_seqs = []
    l = len(dataset)

    seq_index = dataset.index(sample_s)
    temp = [0] * l
    sample_seqs.append(dataset[seq_index])

    min_temp = 0
    j = 1
    while min_temp <= threshold:
        j = j+1
        p = Pool(threads)
        result = []
        for i in tqdm(range(l), desc='Selecting barcode', ncols=100, mininterval=0.3):
            result.append(p.apply_async(
                update, args=(sample_s, dataset[i], i,)))
        p.close()
        p.join()
        for pair in result:
            c = pair.get()
            c = list(c)
            c_1 = float(c[-1])
            c_0 = int(c[0])
            temp[c_0] = max(temp[c_0], c_1)
        min_temp = min(temp)
        seq_index = temp.index(min_temp)
        sample_s = dataset[seq_index]
        sample_seqs.append(sample_s)
        print(j, sample_s)
        file.write(str(sample_s).encode('utf-8')+b"\n")
    file.close()


def check_and_remove_file(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"warning!!! The folder {folder_path} exists, the original folder has been deleted!")


def initialization_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', action='store', dest='barcode_length', type=int, required=True,
                        help='Specify the length of a barcode sequence')
    parser.add_argument('-th', action='store', dest='threshold_number', type=int, required=True,
                        help='Set threshold:the number of edit errors for which a barcode can be correctly demultiplexed')  # 对不同长度设定不同的默认阈值
    parser.add_argument('-o', action='store', dest='output_path', type=str, required=True, default='None_file',
                        help='Output_path. Default output would the current directory')
    # Optional
    parser.add_argument('-a', action='store', dest='sequencing_accuracy', type=float, required=False, default=0.88,
                        help='sequencing accuracy')
    parser.add_argument('-q', action='store', dest='quantity', type=int, required=False, default=100000,
                        help='Number of barcodes after pre-processing.')
    parser.add_argument('-i', action='store', dest='input_path', type=str, required=False, default='None_file',
                        help='Pick the barcode set from the user-specified sequence. Please enter the txt file containing the specified DNA sequence.')
    parser.add_argument('-t', action='store', dest='threads', type=int, required=False, default=20,
                        help='Specify the number of threads, which affects the speed of barcode generation.')
    parser.add_argument('-s', action='store', dest='seed', type=int, required=False, default=1,
                        help='The random seed determines the first generated sequence in the FPS algorithm.')
    parser.add_argument('-f', action='store', dest='flankings', type=str, required=False, default='None_file',
                        help='If barcodes needs to keep a certain edit distance from the flanking sequence. Please specify a fastq file contains the flanking sequences used in the library preparation.')
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    start = time.perf_counter()

    args = initialization_parameters()

    barcode_length = args.barcode_length
    threshold_number = args.threshold_number
    output_path = args.output_path
    threads = args.threads
    quantity = args.quantity
    se = args.seed
    flankings = args.flankings
    input_path = args.input_path
    sequencing_accuracy = args.sequencing_accuracy
    
    threshold = thresh(threshold_number, barcode_length)

    if output_path=="None_file":
        output_path='pro_FPS_select'
    else:
        output_path = output_path+'/pro_FPS_select'
    check_and_remove_file(output_path)    
        

    output_pre_path = output_path + '/pre_processing_barcodes.txt'

    dataset = pre_process()
    FPSselection()

    end = time.perf_counter()
    print('End Generation! Total run time: %s Seconds' % (end - start))
