"""
File: main.py
Author: Chuncheng Zhang
Date: 2025-05-09
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Interpolate examples.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-05-09 ------------------------
# Requirements and constants
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt


# %% ---- 2025-05-09 ------------------------
# Function and class
# 原始时间序列
original_t = np.array([0, 0.01, 0.05, 0.3])  # 时间点
original_values = np.array([1, 2, 3, 4])     # 对应的值

# 目标时间点
# target_t = np.array([0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06])  # 示例目标时间点
target_t = np.linspace(-0.1, 0.4, 20)

# 线性插值
resampled_values_1 = np.interp(target_t, original_t, original_values)

# 创建插值函数
f = interpolate.interp1d(original_t, original_values,
                         kind='linear', fill_value='extrapolate')
# 应用插值
resampled_values_2 = f(target_t)


# %% ---- 2025-05-09 ------------------------
# Play ground
plt.style.available

# %% ---- 2025-05-09 ------------------------
# Pending
with plt.style.context('seaborn-v0_8-whitegrid'):
    plt.plot(original_t, original_values, 'k', label='raw')
    plt.plot(target_t, resampled_values_1, 'go', label='numpy-interp')
    plt.plot(target_t, resampled_values_2, 'rx',
             label='scipy-interp-extrapolate')
    plt.legend()
    plt.tight_layout()
    plt.show()


# %% ---- 2025-05-09 ------------------------
# Pending
