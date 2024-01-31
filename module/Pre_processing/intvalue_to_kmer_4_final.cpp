#include <iostream>
#include <sstream>
#include <stdlib.h>
#include <math.h>
#include <libgen.h>
#include <string>
#include <vector>
#include <fstream>
#include <string.h>
using namespace std;

typedef unsigned long long kmer_int_type_t;
char _int_to_base[4] = {'G', 'A', 'T', 'C'};
unsigned char _base_to_int[256] = {
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, //   0-19
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, //  20-39
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, //  40-59
    255, 255, 255, 255, 255, 1, 255, 3, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255,       //  60-79
    255, 255, 255, 255, 2, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 1, 255, 3,       //  80-99
    255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 2, 255, 255, 255,     // 100-119
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, // 120-139
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, // 140-159
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, // 160-179
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, // 180-209
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, // 200-219
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, // 220-239
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255                      // 240-255
};

char int_to_base(int baseval)
{
  if (baseval < 0 || baseval > 3)
  {
    std::cerr << "Error, baseval out of range 0-3" << std::endl;
    exit(1);
  }
  return (_int_to_base[baseval]);
}

int base_to_int(char nucleotide)
{
  switch (nucleotide)
  {
  case 'G':
  case 'g':
    return (0);
  case 'A':
  case 'a':
    return (1);
  case 'T':
  case 't':
    return (2);
  case 'C':
  case 'c':
    return (3);
  default:
    return (-1);
  }
}

kmer_int_type_t kmer_to_intval(const std::string &kmer)
{
  kmer_int_type_t kmer_val = 0;
  for (unsigned int i = 0; i < kmer.length(); ++i)
  {
    char c = kmer[i];
    int val = base_to_int(c);
    kmer_val = kmer_val << 2;
    kmer_val |= val;
  }
  return (kmer_val);
}

kmer_int_type_t kmer_to_intval(const std::string &kmer, unsigned int kmer_length)
{
  kmer_int_type_t kmer_val = 0;
  for (unsigned int i = 0; i < kmer_length; ++i)
  {
    char c = kmer[i];
    int val = base_to_int(c);
    kmer_val = kmer_val << 2;
    kmer_val |= val;
  }
  return (kmer_val);
}

std::string intval_to_kmer(kmer_int_type_t intval, unsigned int kmer_length)
{
  // std::string kmer = "";
  std::string kmer(kmer_length, ' ');
  for (unsigned int i = 1; i <= kmer_length; ++i)
  {
    int base_num = intval & 3ll;
    // char base = int_to_base(base_num);
    kmer[kmer_length - i] = _int_to_base[base_num];
    intval = intval >> 2;
    // kmer = base + kmer;
  }
  return (kmer);
}

<<<<<<< HEAD
=======
// 读入的文件中的数字是字符串形式，将其转换为整数类型
>>>>>>> 2c04df41c9b4d3a24fc3553359e4acfc47e5a1e4
class Solution
{
public:
  long StrToInt(string str)
  {
    if (str.empty())
    {
      return 0;
    }

<<<<<<< HEAD
=======
    // 记录字符串的对应符号
>>>>>>> 2c04df41c9b4d3a24fc3553359e4acfc47e5a1e4
    int symbol = 1;
    if (str[0] == '-')
    {
      symbol = -1;
      str[0] = '0';
    }
    else if (str[0] == '+')
    {
      symbol = 1;
      str[0] = '0';
    }

<<<<<<< HEAD
=======
    // 字符串转整数，sum记录转换后的数据
>>>>>>> 2c04df41c9b4d3a24fc3553359e4acfc47e5a1e4
    long sum = 0;
    for (int i = 0; i < str.size(); i++)
    {
      if (str[i] < '0' || str[i] > '9')
      {
        sum = 0;
        break;
      }

      sum = sum * 10 + str[i] - '0';
    }
    return symbol * sum;
  }
};

void ShowUsage()
{
  cout << "Usage   :" << endl;
  cout << "Options :" << endl;
  cout << " --l=your barcode length             Your barcode length , an integer." << endl;
  cout << " --input_file=your input_flie path   The default is the pre.txt file in current folder. " << endl;
  cout << " --output_file=your onput_flie path  The default is the pre.txt file in current folder. " << endl;
  cout << " --input_data=input_data             0 is string -> int value, 1 is int value -> string. " << endl;
<<<<<<< HEAD
=======
  // cout << " --help                            Print this help." << endl;
>>>>>>> 2c04df41c9b4d3a24fc3553359e4acfc47e5a1e4
  return;
}

int main(int argc, char *argv[])
{
<<<<<<< HEAD
=======
  // 如果用户没有输入参数，则提示错误信息并退出
>>>>>>> 2c04df41c9b4d3a24fc3553359e4acfc47e5a1e4
  if (argc < 2)
  {
    cout << "No arguments, you MUST give an argument at least!" << endl;
    ShowUsage();

    return -1;
  }

  int nOptionIndex = 1;
  int kmer_length;
  string strkmer_length;
  string strinput;
  string stroutput;
  string strinputdata;
  Solution str;

  while (nOptionIndex < argc)
  {
    // 获取barcode长度
    if (strncmp(argv[nOptionIndex], "--l=", 4) == 0)
    {
      strkmer_length = &argv[nOptionIndex][4];
      kmer_length = str.StrToInt(strkmer_length);
    }
    // 获取输入文件路径
    else if (strncmp(argv[nOptionIndex], "--input_file=", 13) == 0)
    {
      strinput = &argv[nOptionIndex][13];
    }
    // 获取输出文件路径
    else if (strncmp(argv[nOptionIndex], "--output_file=", 14) == 0)
    {
      stroutput = &argv[nOptionIndex][14];
    }
    // 获取输出数据类型
    else if (strncmp(argv[nOptionIndex], "--input_data=", 13) == 0)
    {
      strinputdata = &argv[nOptionIndex][13];
    }
    // 显示帮助信息
    else if (strncmp(argv[nOptionIndex], "--help=", 7) == 0)
    {
      ShowUsage();
      return 0;
    }
    else
    {
      cout << "Options '" << argv[nOptionIndex] << "' not valid. Run '" << argv[0] << "' for details." << endl;
      return -1;
    }
    nOptionIndex++;
  }

  cout << "barcode_length is: " << strkmer_length << endl;
  cout << "input_file is: " << strinput << endl;
  cout << "onput_file is: " << stroutput << endl;

  // int value -> string
<<<<<<< HEAD
  vector<string> dataset;
  string type_1 = "num";
  string type_2 = "string";

=======
  //  读取文件
  vector<string> dataset;
  string type_1 = "num";
  string type_2 = "string";
  // 读取1.in.txt文件数据
>>>>>>> 2c04df41c9b4d3a24fc3553359e4acfc47e5a1e4
  ifstream fin(strinput);
  if (!fin.is_open())
  {
    cout << "open error!" << endl;
  }
<<<<<<< HEAD

=======
  // 将数据存入vv数组(以字符串形式)
>>>>>>> 2c04df41c9b4d3a24fc3553359e4acfc47e5a1e4

  string temp;
  while (getline(fin, temp))
  {
    dataset.push_back(temp);
  }
<<<<<<< HEAD

=======
  // cout << dataset.size() << endl;
  // cout << "signed long long is " << sizeof(long long) << " bytes." << endl << endl;

  // int value -> string (num 转 string)
>>>>>>> 2c04df41c9b4d3a24fc3553359e4acfc47e5a1e4
  if (strinputdata == type_1)
  {
    vector<unsigned long long> select;
    vector<string> kmer_seq;
    for (int i = 0; i < dataset.size(); i++)
    {
      unsigned long long u = str.StrToInt(dataset[i]);
      select.push_back(u);
      // if (i <= 3)
        // cout << u << " " << i << endl;
    }
    for (unsigned long long i = 0; i < select.size(); i++)
    {
      unsigned long long g = select[i];
<<<<<<< HEAD
      string kmer_ = intval_to_kmer(g, kmer_length);
      kmer_seq.push_back(kmer_);
    }
    // cout << kmer_seq.size() << endl;

    ofstream fout;
    fout.open(stroutput); 
    for (unsigned long long h = 0; h < kmer_seq.size(); h++)
    {
      fout << kmer_seq[h] << endl;
    }
    fout.close();
=======
      // cout<<i<<" "<<g<<endl;
      string kmer_ = intval_to_kmer(g, kmer_length);
      kmer_seq.push_back(kmer_);
      // cout<<"the "<<kmer_length<<"mer string for int "<<k<<" is: "<<kmer_<<endl;
    }
    // cout << kmer_seq.size() << endl;

    ofstream fout;        // 创建ofstream
    fout.open(stroutput); // 关联一个文件
    for (unsigned long long h = 0; h < kmer_seq.size(); h++)
    {
      fout << kmer_seq[h] << endl; // 写入
      // cout << kmer_seq[h] << endl;
    }
    fout.close(); // 关闭
>>>>>>> 2c04df41c9b4d3a24fc3553359e4acfc47e5a1e4
  }

  // string -> int value (string 转 num)
  if (strinputdata == type_2)
  {
    vector<unsigned long long> num;
    unsigned long long g;
    for (int i = 0; i < dataset.size(); i++)
    {
      g = kmer_to_intval(dataset[i]);
      num.push_back(g);
    }
<<<<<<< HEAD

    ofstream fout;
    fout.open(stroutput);
    for (unsigned long long h = 0; h < num.size(); h++)
    {
      fout << num[h] << endl;
    }
    fout.close();
=======
    // cout << "num.size()" << num.size() << endl;

    ofstream fout;        // 创建ofstream
    fout.open(stroutput); // 关联一个文件
    for (unsigned long long h = 0; h < num.size(); h++)
    {
      fout << num[h] << endl; // 写入
    }
    fout.close(); // 关闭
>>>>>>> 2c04df41c9b4d3a24fc3553359e4acfc47e5a1e4
  }
  return 0;
}
