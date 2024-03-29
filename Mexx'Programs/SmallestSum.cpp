﻿//Задана матрица целых чисел вычислить суммы элементов во всех столбах матрицы и 
// вывести минимальную сумму

#include <iostream>
using namespace std;

int** create_matrix(int n, int m) {
	int** a = new int* [n];
	for (int i = 0; i < n; i++) {
		a[i] = new int[m];
	}
	return a;
}
void fill_matrix(int** mat, int n, int m) {
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			scanf_s("%d", &mat[i][j]);
		}
	}
}
void delete_matrix(int** mat, int n, int m) {
	for (int i = 0; i < n; i++) {
		delete[] mat[i];
	}
	delete[] mat;
}

int sum_row(int* row, int n) {
	int sum = 0;
	for (int i = 0; i < n; i++) {
		sum += row[i];
	}
	return sum;
}
void Find_smallestSumRow(int** mat, int n, int m, int& index, int& sum_value) {
	int minSum = INT_MAX, row_sum;
	for (int i = 0; i < n; i++) {
		row_sum = sum_row(mat[i], m);
		if (row_sum < minSum) {
			minSum = row_sum;
			index = i;
			sum_value = row_sum;
		}
	}
}
int main() {
	setlocale(0, "rus");
	
	int n, m;
	scanf_s("%d", &n); scanf_s("%d", &m);
	int** a = create_matrix(n, m);
	fill_matrix(a, n, m);

	int ind, sum;
	Find_smallestSumRow(a, n, m, ind, sum);

	printf("Наименьшая сумма %d в столбе %d\n", sum, ind);

	delete_matrix(a, n, m);

	return 0;
}