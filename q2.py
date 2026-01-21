from scipy.stats import norm
from math import log, sqrt, exp

def black_scholes(S, K, T, r, sigma, option_type):
    """计算Black-Scholes期权价格"""
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type必须是'call'或'put'")
    return price

def implied_volatility(S, K, T, r, market_price, option_type, tol=1e-6, max_iter=1000):
    """二分法计算隐含波动率"""
    vol_low = 0.001    # 波动率下限(0.1%)
    vol_high = 10.0     # 波动率上限(500%)
    
    for _ in range(max_iter):
        vol_mid = (vol_low + vol_high) / 2
        price_mid = black_scholes(S, K, T, r, vol_mid, option_type)
        
        if price_mid > market_price:
            vol_high = vol_mid
        else:
            vol_low = vol_mid
        
        if (vol_high - vol_low) < tol:
            return (vol_low + vol_high) / 2
    
    return (vol_low + vol_high) / 2  # 未收敛时返回最近值

# 输入参数
S = 2.651          # 标的资产价格
K = 2.65           # 行权价
T = 28 / 365       # 到期时间（年）
r = 0.03           # 无风险利率

call_price = 0.1205 # 看涨期权市场价格
put_price = 0.1134  # 看跌期权市场价格

# 计算隐含波动率
iv_call = implied_volatility(S, K, T, r, call_price, 'call')
iv_put = implied_volatility(S, K, T, r, put_price, 'put')

# 输出结果（保留四位小数）
print(f"看涨期权隐含波动率: {iv_call:.4f} ({iv_call*100:.2f}%)")
print(f"看跌期权隐含波动率: {iv_put:.4f} ({iv_put*100:.2f}%)")

print("This is the anwser to question 2.")