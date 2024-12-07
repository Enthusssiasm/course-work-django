# main/services.py
import math


def calculate_m(M):
    return round(math.log(M, 2))


def generate_matrix_p(matrix, k):
    P = []
    for i in matrix:
        binary_number = bin(i)
        binary_number_clean = binary_number[2:]
        Pi = []
        for j in binary_number_clean:
            Pi.append(int(j))
        while len(Pi) < k:
            Pi.insert(0, 0)
        P.append(Pi[:])
        Pi.clear()
    return P


def transpose_matrix(P):
    return [[P[j][i] for j in range(len(P))] for i in range(len(P[0]))]


def create_identity_matrix(k):
    return [[1 if i == j else 0 for j in range(k)] for i in range(k)]


def combine_matrices(transposed_P, identity_matrix):
    return [transposed_P[i] + identity_matrix[i] for i in range(len(transposed_P))]


def generate_encoding_indices(transposed_P, P):
    encoding_indices = []

    # Формирование индексов для c1, c2, c3
    for row in transposed_P:
        indices = [f"a{col_idx + 1}" for col_idx, value in enumerate(row) if value == 1]
        encoding_indices.append(indices)

    # Формирование индексов для c4
    c4_indices = [f"a{row_idx + 1}" for row_idx, row in enumerate(P) if sum(row) % 2 == 0]
    encoding_indices.append(c4_indices)

    return encoding_indices


def generate_syndrome_indices(encoding_indices):
    syndrome_indices = []

    # Формирование синдромов для c1, c2, c3
    for a_idx, indices in enumerate(encoding_indices, 1):
        if a_idx < 4:
            syndrome_indices.append(indices + [f"c{a_idx}"])

    # Формирование индексов для S4 (все a и c)
    all_a_indices = sorted(set(idx for indices in encoding_indices for idx in indices if idx.startswith("a")))
    all_c_indices = [f"c{i}" for i in range(1, len(encoding_indices) + 1)]
    syndrome_indices.append(all_a_indices + all_c_indices)

    return syndrome_indices


def generate_syndrome_table(syndrome_indices):
    result_dict = {}
    meaning = ['a1', 'a2', 'a3', 'a4', 'c1', 'c2', 'c3', 'c4']
    for idx, j in enumerate(meaning, 1):
        result = ''.join(['1' if j in syndrome else '0' for syndrome in syndrome_indices])
        result_dict[f"e{idx}({j})"] = result
    result_dict["Ошибок нет"] = "0000"
    return result_dict


def calculate_redundant_bits(encoding_indices, information_bits):
    redundant_bits = []
    for indices in encoding_indices:
        count_ones = sum(information_bits[int(i[1:]) - 1] for i in indices)  # Преобразование a2 -> 2
        redundant_bits.append(0 if count_ones % 2 == 0 else 1)
    group_code_vector = ''.join(map(str, information_bits)) + ''.join(map(str, redundant_bits))
    return redundant_bits, group_code_vector


def generate_error_code(group_code_vector, error_vector):
    # Вектор группового кода с ошибкой
    group_code_with_error = [str(int(group_code_vector[i]) ^ int(error_vector[i])) for i in range(len(group_code_vector))]
    return group_code_with_error

