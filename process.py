import numpy as np
from matplotlib import pyplot as plt

from values import r_vals, L_vals, num_repeats, t_max

def read_single_S(filename):
    f = open(filename, "r")
    x = float(f.read())
    print(f"x: {x}")
    return x

def read_S_vals():
    S_vals = np.zeros((len(L_vals), len(r_vals)))
    for r_idx, r in enumerate(r_vals):
        for L_idx, L in enumerate(L_vals):
            S_total = 0
            for repeat_idx in range(num_repeats):
                filename = f"S_r{str(r).replace('.', '-')}_L{L}_n{repeat_idx}.txt"
                S_val = read_single_S(filename)
                S_total += S_val
            S_total /= num_repeats
            S_vals[L_idx, r_idx] = S_total
    return S_vals

def main():
    S_vals = read_S_vals()
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']
    plt.xscale('log')
    for L_idx, L_val in enumerate(L_vals):
        S_r = S_vals[L_idx, :]
        plt.plot(r_vals, S_r, color=colors[L_idx], label=f"L={L_val}", marker='o')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()