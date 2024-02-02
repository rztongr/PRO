import random
import os
import argparse
import edlib
import sys


def initialization_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_path', type=str, required=False, default="None_file",
                        help='input_path')
    parser.add_argument('-l', action='store', dest='barcode_length',
                        type=int, required=True, help='barcode_length')
    parser.add_argument('-o', action='store', dest='output_file', type=str, required=True,
                        help='output_file_path')
    parser.add_argument('-q', action='store', dest='quantity', type=int, required=False, default=10000,
                        help='Quantity of barcode after pre-processing.')
    parser.add_argument('-f', action='store', dest='flankings', type=str, required=False, default='None_file',
                        help='A fastq file contains the flanking sequences used in the library preparation.')
    args = parser.parse_args()
    return args


def split_list(N, n):
    random.seed(1)
    samp = []
    size, rest = divmod(N, n)
    if rest == 0 and size > n:
        return split(size, n)
    else:
        start = 0
        for i in range(n):
            step = size + 1 if i < rest else size
            stop = start + step
            a = random.randint(start, stop-1)
            samp.append(a)
            start = stop
        return samp


def split(size, n):
    samp = []
    random.seed(1)
    list = [i for i in range(size)]
    samp_ = random.sample(list, n)
    for i in range(len(samp_)):
        num = i*size+samp_[i]
        samp.append(num)
    return samp


def away(d):
    fw = open(output_file, 'w')
    for seq in d:
        a = edlib.align(fr, seq, mode="HW", task="path")
        b = edlib.align(en, seq, mode="HW", task="path")
        if a['editDistance'] > 1 and b['editDistance'] > 1:
            fw.write(str(seq)+"\n")
    fw.close()


def run():
    output_file_num = os.path.split(output_file)[0] + '/pre_processing_barcodes_number.txt'
    os.system('g++ ' + 'module/Pre_processing/intvalue_to_kmer_4_final.cpp -o module/Pre_processing/intvalue_to_kmer_4_final')
    length_command = ' --l=' + str(barcode_length)
    input_file_command = ' --input_file=' + output_file_num
    output_file_command = ' --output_file=' + output_file
    command = 'module/Pre_processing/intvalue_to_kmer_4_final' + \
        length_command + input_file_command + output_file_command
    return output_file_num, command


def Prescreening():
    random.seed(1)
    output_file_num, command = run()
    if input_path == 'None_file':
        fw = open(output_file_num, 'w')
        s = split_list(4**barcode_length, quantity)
        for e in s:
            fw.write(str(e)+"\n")
        fw.close()
        command_input_data = ' --input_data=num'
        command = command+command_input_data
        os.system(command)
    else:
        command_input_data = ' --input_data=string'
        length_command = ' --l=' + str(barcode_length)
        input_file_command = ' --input_file=' + input_path
        output_file_command = ' --output_file=' + output_file_num
        command = command+command_input_data+length_command + input_file_command + output_file_command
        os.system(command)
        str_nums = read_file(output_file_num)
        int_nums = [int(x) for x in str_nums]
        int_nums.sort()
        s = split_list(len(int_nums), quantity)
        user_seqs_prescreening = []
        fw = open(output_file_num, 'w')
        for i in s:
            fw.write(str(int_nums[i-1])+"\n")
            user_seqs_prescreening.append(int_nums[i-1])
        fw.close()
        output_file_num, command = run()
        command_input_data = ' --input_data=num'
        command = command+command_input_data
        os.system(command)
    d = read_file(output_file)
    return d


def read_file(path):
    line = []
    with open(path, "r") as f:
        data = f.readlines()
    for m in range(len(data)):
        line.append(data[m].strip('\n'))
    return line


def get_flanking(path):
    line = read_file(path)
    fr = line[1]
    en = line[3]
    return fr, en


if __name__ == '__main__':

    args = initialization_parameters()

    barcode_length = args.barcode_length
    output_file = args.output_file
    quantity = args.quantity
    flankings = args.flankings
    input_path = args.input_path

    print("---------------------------Start pre-processing!-------------------------")
    dataset = Prescreening()
    if flankings != 'None_file':
        fr, en = get_flanking(flankings)
        away(dataset)
    print("---------------------------End pre-processing!-------------------------")
