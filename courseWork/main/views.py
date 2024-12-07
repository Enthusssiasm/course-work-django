from django.shortcuts import render
from main.services import (calculate_m, generate_matrix_p, transpose_matrix,
                           create_identity_matrix, combine_matrices, generate_encoding_indices,
                           generate_syndrome_indices, generate_syndrome_table, calculate_redundant_bits,
                           generate_error_code, )


def index(request):
    variant = 12
    M = 13
    k = 3
    decimal_matrix_P = [5, 7, 6, 3]
    encoder = 'Последовательный'
    decoder = 'Параллельный'

    U = (variant % 7) + 1
    binary_U = bin(U)[2:].zfill(4)

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

    # Извлечение данных из сессии
    group_code_vector = request.session.get('group_code_vector', '')
    group_code_with_error = request.session.get('group_code_with_error', '')

    context = {
        'variant': variant,
        'U': U,
        'binary_U': binary_U,
        'M': M,
        'm': m,
        'k': k,
        'encoder': encoder,
        'decoder': decoder,
        'decimal_matrix_P': decimal_matrix_P,
        'binary_matrix_P': binary_matrix_P,
        'transposed_P': transposed_P,
        'H_matrix': H_matrix,
        'encoding_operators': encoding_operators,
        'syndrome_operators': syndrome_operators,
        'syndrome_table': syndrome_table,
        'group_code_vector': group_code_vector,
        'group_code_with_error': group_code_with_error,
    }

    if request.method == 'POST':
        group_code_vector = request.POST.get('group_code_vector', '')
        if 'information_vector' in request.POST:
            input_information_vector = request.POST.get('information_vector', '')
            information_bits = [int(bit) for bit in input_information_vector]
            redundant_bits, group_code_vector = calculate_redundant_bits(encoding_indices, information_bits)
            context['redundant_bits'] = redundant_bits
            context['group_code_vector'] = ''.join(map(str, group_code_vector))

        if 'error_vector' in request.POST:
            error_vector = request.POST.get('error_vector', '')
            group_code_with_error = generate_error_code(group_code_vector, error_vector)
            context['group_code_with_error'] = ''.join(group_code_with_error)

        action = request.POST.get('action', '')

        if action == 'clear':
            # Очищаем сессионные данные
            request.session.pop('group_code_vector', None)
            request.session.pop('group_code_with_error', None)

    return render(request, 'main/index.html', context)
