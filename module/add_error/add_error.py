import random
import argparse



def initialization_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', action='store', dest='barcode_file', type=str, required=True, help='The barcode file_csv')
    parser.add_argument('-o', action='store', dest='output_file', type=str, required=True, help='The output_file')
    parser.add_argument('-e', action='store', dest='error_num', type=int, required=True,help="error_number")
    args = parser.parse_args()
    return args

def add_random_mismatch(seq):
    i = random.randrange(len(seq))
    b = random.choice(bases.replace(seq[i], ''))
    return seq[:i] + b + seq[i+1:]

def add_random_deletion(seq):
    i = random.randrange(len(seq))
    return seq[:i] + seq[i+1:]

def add_random_insertion(seq):
    i = random.randrange(len(seq))
    b = random.choice(bases)
    return seq[:i] + b + seq[i:]        

def add_no_error(seq):
    return seq

def random_pick():
    some_list=["mismatch","deletion","insertion"]
    probabilities=[1/3,1/3,1-2/3]
    x = random.uniform(0,1)
    # print(x)
    cumulative_probability=0.0
    for item,item_probability in zip(some_list,probabilities):
        cumulative_probability+=item_probability
        if x < cumulative_probability:
            break
    return item

def add_error(seq,num):
    i=0
    for i in range(num):
        # print(i)
        i=i+1
        error=random_pick()
        if error=="mismatch":
            seq=add_random_mismatch(seq)
        elif error=="deletion":
            seq=add_random_deletion(seq)
        elif error=="insertion":
            seq=add_random_insertion(seq)
    return seq        

if __name__== "__main__" :
    args = initialization_parameters()

    barcode_file = args.barcode_file
    output_file = args.output_file
    error_num = args.error_num
    # se=args.random_seed
    bases='ACGT'

    dataset = []
    dataset1 = []
    with open(barcode_file,'r') as f:  
        data = f.readlines()
    for m in range(1,len(data)):
        lin=data[m].strip('\n')
        dataset.append(lin.split(",")[-1])
    print(dataset[0])
    print(dataset[-1])

    fw = open(output_file+'/'+str(error_num)+'_error.txt', 'w') 
    for seq in dataset:
        for i in range(100):
            seq1=add_error(seq,error_num)
            fw.write(str(seq1) + '\n')

    fw = open(output_file+'/noerror.txt', 'w') 
    for seq in dataset:
        fw.write(str(seq) + '\n')
