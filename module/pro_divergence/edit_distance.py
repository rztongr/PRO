# from pprint import pprint
import time
time_start = time.time()  # 记录开始时间


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:

        m = len(word1)
        n = len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        #print(dp)
        # dp[i][j]表示word1[:i]与word2[:j]之间的编辑距离

        # 若一个字符串为空，编辑距离等于另一个字符串的长度
        for i in range(1, m + 1):
            dp[i][0] = i

        for j in range(1, n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]) + 1
        # print(dp)
        return dp, dp[m][n]
    
    #word1变word2
    def backpath(self, word1, word2, dp):
        i = len(dp) - 1
        #print(len(dp)-1)
        j = len(dp[0]) - 1
        res = []
        while i > 0 or j > 0:
            a = dp[i - 1][j - 1] if i > 0 and j > 0 else float("inf")
            b = dp[i - 1][j] if i > 0 else float("inf")
            c = dp[i][j - 1] if j > 0 else float("inf")
            min_val = min([a, b, c])

            if dp[i][j] == a and a == min_val:
                i -= 1
                j -= 1
                res.append(("" , "" , "" , "" , "non"))
                # 没有操作
            elif b == min([a, b, c]):
                # 通过删除来的
                i = i - 1
                res.append((i, i + 1, word1[i], "", "del"))
            elif a == min([a, b, c]):
                #  通过替换来的
                i -= 1
                j -= 1
                res.append((i, i + 1, word1[i], word2[j], "sub"))  
            else:
                # 通过插入来的
                j = j - 1
                res.append((i + 1, i + 1, "", word2[j], "ins"))
        # print(res)
        return res

# def metric(word1, word2):
#     q = 0.88
#     operate = []
#     obj = Solution()
#     dp, min_distance = obj.minDistance(word1, word2)
#     #print(min_distance)
#     res = obj.backpath(word1, word2, dp)
#     #print(res)
#     for i in res:
#         operate.append(list(i)[4])
#     c = operate.count('non')
#     s = operate.count('sub')
#     i = operate.count('ins')
#     d = operate.count('del')
#     #print(c,s,i,d)
#     # metr = q ** c * ((1 / 3) * (1 - q)) ** d * ((1 / 3)**2 * (1 - q)) ** s *((1 / 3)*(1 / 4) * (1 - q)) ** i
#     metr = q ** c * ((1 / 3) * (1 - q)) ** d * ((1 / 3)**2 * (1 - q)) ** s *((1 / 3)*(1 / 4) * (1 - q)) ** i
#     #print(metr)
#     return metr

def metric(word1, word2):
    q = 0.88
    operate = []
    obj = Solution()
    dp, min_distance = obj.minDistance(word1, word2)
    #print(min_distance)
    res = obj.backpath(word1, word2, dp)
    #print(res)
    for i in res:
        operate.append(list(i)[4])
    c = operate.count('non')
    s = operate.count('sub')
    i = operate.count('ins')
    d = operate.count('del')
    #print(c,s,i,d)
    metr = q ** c * ((1 / 3) * (1 - q)) ** d * ((1 / 3)**2 * (1 - q)) ** s *((1 / 3)*(1 / 4) * (1 - q)) ** i
    #print(metr)
    return metr

def weight(word1,word2):
    w1=metric(word1, word2)
    w2=metric(word2, word1)
    #print(w1,w2)
    w=max(w1,w2)
    return w

# def p():
#     print("hello world!")




# word1 = "horse"
# word2 = "trse"
# word1 = "AAAAAAAAAA"
# word2 = "AAAAAAAAAAA"
# word1='AAAA'
# word2='AAAAA'

# print(metric(word1,word2))
# print(1/3)

time_end = time.time()  # 记录结束时间
time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
# print(time_sum)   


 

