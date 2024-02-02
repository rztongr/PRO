

class Solution:
    def minDistance(self, word1: str, word2: str) -> int:

        m = len(word1)
        n = len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
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
        return dp, dp[m][n]
    
    #word1变word2
    def backpath(self, word1, word2, dp):
        i = len(dp) - 1
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
            elif b == min([a, b, c]):
                i = i - 1
                res.append((i, i + 1, word1[i], "", "del"))
            elif a == min([a, b, c]):
                i -= 1
                j -= 1
                res.append((i, i + 1, word1[i], word2[j], "sub"))  
            else:
                j = j - 1
                res.append((i + 1, i + 1, "", word2[j], "ins"))
        return res

def metric(word1, word2, error_rate):
    operate = []
    obj = Solution()
    dp, min_distance = obj.minDistance(word1, word2)
    res = obj.backpath(word1, word2, dp)
    for i in res:
        operate.append(list(i)[4])
    c = operate.count('non')
    s = operate.count('sub')
    i = operate.count('ins')
    d = operate.count('del')
    metr = error_rate ** c * ((1 / 3) * (1 - error_rate)) ** d * ((1 / 3)**2 * (1 - error_rate)) ** s *((1 / 3)*(1 / 4) * (1 - error_rate)) ** i
    return metr

def weight(word1, word2, error_rate):
    w1=metric(word1, word2, error_rate)
    w2=metric(word2, word1, error_rate)
    w=max(w1,w2)
    return w