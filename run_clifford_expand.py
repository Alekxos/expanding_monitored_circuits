import argparse
import numpy as np
import stim

from values import num_repeats, t_max
from functions import init_superposition_state, EntanglementEntropy

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("r")
parser.add_argument("L")
parser.add_argument("n")
args = parser.parse_args()

def main():
    L = int(args.L)
    n = int(args.n)
    r = float(args.r)
    print(f"L={L}; n={n}; r={r}")
    simulator = stim.TableauSimulator()
    circuit = init_superposition_state(L)
    for t in range(t_max + np.random.choice([0, 1])):
        if t % 2 == 0:
            # Even rows
            # offset by 2 so that circuit doesn't go out of bounds
            for even_idx in range(0 + 2, 2 + (L - 1), 2):
                # if np.random.uniform() < p:
                #   print(f"M {even_idx}, {even_idx + 1}")
                #   circuit.append("M", [even_idx, even_idx + 1])
                if np.random.uniform() < r:
                    directionality = np.random.choice([0, 1])
                    new_idx = even_idx + directionality
                    shifted_circuit = stim.Circuit()
                    if directionality == 1:
                        # Measure rightmost qubit
                        shifted_circuit.append("M", [2 + L])
                        for c in circuit:
                            c_args = str(c).split(' ')
                            gate = c_args[0]

                            # Shift right by 1
                            targets = [int(target) + 1 if int(target) >= new_idx
                                       else int(target) for target in c_args[1:]]
                            instruction = stim.CircuitInstruction(gate, targets)
                            shifted_circuit.append(instruction)
                        # Insert measured result at ancilla position
                        shifted_circuit.append("SWAP", [2 + L, new_idx])
                    else:
                        # Measure leftmost qubit
                        shifted_circuit.append("M", [1])
                        for c in circuit:
                            c_args = str(c).split(' ')
                            gate = c_args[0]

                            # Shift left by 1
                            targets = [int(target) - 1 if int(target) <= new_idx
                                       else int(target) for target in c_args[1:]]
                        # if np.all([target >= 0 for target in targets]) and np.all([target <= L - 1 for target in targets]):
                        instruction = stim.CircuitInstruction(gate, targets)
                        shifted_circuit.append(instruction)
                        # Insert measured result at ancilla position
                        shifted_circuit.append("SWAP", [2 + (-1), new_idx])
                    circuit = shifted_circuit
                    ## Insert new qubit wire to left/right with even probability
                # else:
                tableau = stim.Tableau.random(2)
                C = tableau.to_circuit(method="elimination")
                for c in C:
                    # print(f"c: {str(c)}")
                    c_args = str(c).split(' ')
                    gate = c_args[0]
                    targets = [int(target) + even_idx for target in c_args[1:]]
                    instruction = stim.CircuitInstruction(gate, targets)
                    circuit.append(instruction)
        else:
            # Odd rows
            for odd_idx in range(2 + 1, 2 + (L - 1), 2):
                # if np.random.uniform() < p:
                #   print(f"M {odd_idx}, {odd_idx + 1}")
                #   circuit.append("M", [odd_idx, odd_idx + 1])
                if np.random.uniform() < r:
                    directionality = np.random.choice([0, 1])
                    new_idx = odd_idx + directionality
                    shifted_circuit = stim.Circuit()
                    if directionality == 1:
                        # Measure rightmost qubit
                        shifted_circuit.append("M", [2 + L])
                        for c in circuit:
                            c_args = str(c).split(' ')
                            gate = c_args[0]

                            # Shift right by 1
                            targets = [int(target) + 1 if int(target) >= new_idx
                                       else int(target) for target in c_args[1:]]
                            instruction = stim.CircuitInstruction(gate, targets)
                            shifted_circuit.append(instruction)
                        # Insert measured result at ancilla position
                        shifted_circuit.append("SWAP", [2 + L, new_idx])
                    else:
                        # Measure leftmost qubit
                        shifted_circuit.append("M", [1])
                        for c in circuit:
                            c_args = str(c).split(' ')
                            gate = c_args[0]

                            # Shift left by 1
                            targets = [int(target) - 1 if int(target) <= new_idx
                                       else int(target) for target in c_args[1:]]
                        # if np.all([target >= 0 for target in targets]) and np.all([target <= L - 1 for target in targets]):
                        instruction = stim.CircuitInstruction(gate, targets)
                        shifted_circuit.append(instruction)
                        # Insert measured result at ancilla position
                        shifted_circuit.append("SWAP", [2 + (-1), new_idx])

                    shifted_circuit.append("H", [new_idx])
                    circuit = shifted_circuit
                # else:
                tableau = stim.Tableau.random(2)
                C = tableau.to_circuit(method="elimination")
                for c in C:
                    c_args = str(c).split(' ')
                    gate = c_args[0]
                    targets = [int(target) + odd_idx for target in c_args[1:]]
                    instruction = stim.CircuitInstruction(gate, targets)
                    circuit.append(instruction)
    simulator.do_circuit(circuit)
    S_run = EntanglementEntropy(simulator, 2 + L // 4)
    f = open(f"S_r{str(r).replace('.', '-')}_L{L}_n{n}.txt", "a")
    f.write(f"{S_run}")
    f.close()
    print(f"S: {S_run}")
# print(f"Final circuit: {circuit}")

if __name__ == "__main__":
    main()