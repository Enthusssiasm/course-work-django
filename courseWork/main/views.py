from django.shortcuts import render
from main.services import (calculate_m, generate_matrix_p, transpose_matrix,
                           create_identity_matrix, combine_matrices, generate_encoding_indices,
                           generate_syndrome_indices, generate_syndrome_table, calculate_redundant_bits)


def index(request):
    M = 13
    k = 3
    decimal_matrix_P = [5, 7, 6, 3]

    m = calculate_m(M)

    binary_matrix_P = generate_matrix_p(decimal_matrix_P, k)
    transposed_P = transpose_matrix(binary_matrix_P)

    identity_matrix = create_identity_matrix(k)
    H_matrix = combine_matrices(transposed_P, identity_matrix)

    encoding_indices = generate_encoding_indices(transposed_P, binary_matrix_P)
    encoding_operators = [(idx + 1, " ⊕ ".join(indices)) for idx, indices in enumerate(encoding_indices)]

    syndrome_indices = generate_syndrome_indices(encoding_indices)
    syndrome_operators = [(idx + 1, " ⊕ ".join(indices)) for idx, indices in enumerate(syndrome_indices)]

    syndrome_table = generate_syndrome_table(syndrome_indices)

    if request.method == 'POST':
        input_information_vector = request.POST.get('information_vector', '')
        information_bits = [int(bit) for bit in input_information_vector]
        redundant_bits, group_code_vector = calculate_redundant_bits(encoding_indices, information_bits)
        return render(request, 'main/index.html', context={
            'm': m,
            'k': k,
            'decimal_matrix_P': decimal_matrix_P,
            'binary_matrix_P': binary_matrix_P,
            'transposed_P': transposed_P,
            'H_matrix': H_matrix,
            'encoding_operators': encoding_operators,
            'syndrome_operators': syndrome_operators,
            'syndrome_table': syndrome_table,
            'redundant_bits': redundant_bits,
            'group_code_vector': group_code_vector
        })


    return render(request, 'main/index.html', context={
        'm': m,
        'k': k,
        'decimal_matrix_P': decimal_matrix_P,
        'binary_matrix_P': binary_matrix_P,
        'transposed_P': transposed_P,
        'H_matrix': H_matrix,
        'encoding_operators': encoding_operators,
        'syndrome_operators': syndrome_operators,
        'syndrome_table': syndrome_table,
    })
