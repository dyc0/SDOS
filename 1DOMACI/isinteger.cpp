// VERSION WITH LOOPS

#include <iostream>
#include <cstdlib>
#include <cmath>

#define MATRIX_DIM 1024

void isinteger (float* matrix[], bool* results[]) {
    // Loop order is important when matrices get big.
    for (int j = 0; j < MATRIX_DIM; j++)
        for (int i = 0; i < MATRIX_DIM; i++)
            results[j][i] = matrix[j][i] == std::round(matrix[i][j]);
            // This check is not numerically stable, there should be 
            // an approximate check instead of an absolute one.
}

int main(int argv, char** argc) {

    // MATRIX GENERATION
    float* matrix[MATRIX_DIM];
    float* column;
    bool* results[MATRIX_DIM];
    for (int i = 0; i < MATRIX_DIM; i++) {
        results[i] = new bool[MATRIX_DIM];
        column = new float[MATRIX_DIM];
        for (int j = 0; j < MATRIX_DIM; j++)
            column[j] = static_cast <float> (std::rand()) / (static_cast <float> (RAND_MAX/10));
        matrix[i] = column; 
    }
        

    // CHECKING FOR INTEGERS
    isinteger(matrix, results);

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