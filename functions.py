import numpy as np
import stim


def gf2_rank(rows):
    """
    Find rank of a matrix over GF2.

    The rows of the matrix are given as nonnegative integers, thought
    of as bit-strings.

    This function modifies the input list. Use gf2_rank(rows.copy())
    instead of gf2_rank(rows) to avoid modifying rows.
    """
    rank = 0
    while rows:
        pivot_row = rows.pop()
        if pivot_row:
            rank += 1
            lsb = pivot_row & -pivot_row
            for index, row in enumerate(rows):
                if row & lsb:
                    rows[index] = row ^ pivot_row
    return rank

def getCutStabilizers(binaryMatrix, cut):
    """
        - Purpose: Return only the part of the binary matrix that corresponds to the qubits we want to consider for a bipartition.
        - Inputs:
            - binaryMatrix (array of size (N, 2N)): The binary matrix for the stabilizer generators.
            - cut (integer): Location for the cut.
        - Outputs:
            - cutMatrix (array of size (N, 2cut)): The binary matrix for the cut on the left.
    """
    N = len(binaryMatrix)
    cutMatrix = np.zeros((N,2*cut))

    cutMatrix[:, :cut] = binaryMatrix[:,:cut]
    cutMatrix[:, cut:] = binaryMatrix[:,N:N+cut]

    return cutMatrix

def binaryMatrix(zStabilizers):
    """
      - Purpose: Construct the binary matrix representing the stabilizer states.
      - Inputs:
          - zStabilizers (array): The result of conjugating the Z generators on the initial state.
      Outputs:
          - binaryMatrix (array of size (N, 2N)): An array that describes the location of the stabilizers in the tableau representation.
    """
    N = len(zStabilizers)
    binaryMatrix = np.zeros((N, 2*N))
    r = 0 # Row number
    for row in zStabilizers:
      c = 0 # Column number
      for i in row:
          if i == 3: # Pauli Z
              binaryMatrix[r,N + c] = 1
          if i == 2: # Pauli Y
              binaryMatrix[r,N + c] = 1
              binaryMatrix[r,c] = 1
          if i == 1: # Pauli X
              binaryMatrix[r,c] = 1
          c += 1
      r += 1

    return binaryMatrix

# Inspired by https://quantumcomputing.stackexchange.com/questions/16718/measuring-entanglement-entropy-using-a-stabilizer-circuit-simulator
def EntanglementEntropy(s, x):
    tableau = s.current_inverse_tableau() ** -1
    zs = [tableau.z_output(k) for k in range(len(tableau))]
    zs = np.array(zs)
    binary_matrix = binaryMatrix(zs)
    cut_matrix = getCutStabilizers(binary_matrix, x)
    row_size = cut_matrix[0].size
    reverse_list = list(range(row_size))[::-1]
    power_list = [int(2**exponent) for exponent in reverse_list]
    bitstring_matrix = [sum([int(row[i]) * power_list[i] for i in range(len(row))]) for row in cut_matrix]
    # bitstring_matrix = [int(row.dot(power_list)) for row in cut_matrix]
    rank_ge = gf2_rank(bitstring_matrix) - x
    return rank_ge

def init_superposition_state(L):
    # Prepare initial state (x-product state)
    circuit = stim.Circuit()
    for l in range(0, L - 1, 2):
        circuit.append("H", [l])
        circuit.append("CNOT", [l, l + 1])
    #print(f"Initial state circuit: {circuit}")
    return circuit