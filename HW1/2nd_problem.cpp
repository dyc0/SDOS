#include <iostream>
#include <cstdlib>
#include <cmath>

#define MATRIX_DIM 1024
#define PRINTRESULTS

void iseven (int* matrix[], bool* results[]) {
    // Redosled for petlji je vazan za brzinu
    for (int j = 0; j < MATRIX_DIM; j++)
        for (int i = 0; i < MATRIX_DIM; i++)
            results[j][i] = !(matrix[j][i] & 1);
}

// isodd se dobija kao !iseven

int main(int argv, char** argc) {
    int* matrix[MATRIX_DIM];
    int* column;
    bool* results[MATRIX_DIM];
    for (int i = 0; i < MATRIX_DIM; i++) {
        results[i] = new bool[MATRIX_DIM];
        column = new int[MATRIX_DIM];
        for (int j = 0; j < MATRIX_DIM; j++)
            column[j] = std::rand() / (static_cast <float> (RAND_MAX/10));
        matrix[i] = column; 
    }

    iseven(matrix, results);

#ifdef PRINTRESULTS

    for (int i = 0; i < MATRIX_DIM; i++) {
        for (int j = 0; j < MATRIX_DIM; j++)
            std::cout << matrix[i][j] << " ";
        std::cout << std::endl;
    }
    for (int i = 0; i < MATRIX_DIM; i++) {
        for (int j = 0; j < MATRIX_DIM; j++)
            std::cout << results[i][j] << " ";
        std::cout << std::endl;
    }

#endif

    return 0;
}