//Задан массив целых чисел записать максимальное и переместить его в конец
#include <iostream>
#include <limits>
using namespace std;

int main() {
	setlocale(0, "rus");

	const int n = 5;
	const int q = 6;
	int a[n];
	
	//Записываем изначальный массив
	for (int i = 0; i < n; i++) {
		printf("Введите элемент массива =  ", i);
		scanf_s("%d", &a[i]);
	}
	// Ищем максимальный элемент массива
	int p;
	int max = INT_MIN;
	for (int i = 0; i < n; i++) {
		if (a[i] > max) {
			p = i;
			max = a[i];
		}
	}

	//Инициализируем новый массив и в конец записываем максимальное число из первого массива
	int b[q];
	for (int i = 0; i < n; i++)
	{
		b[i] = a[i];
	}
	b[5] = a[p];

	//Выводим итоговый массив
	printf("Новый массив: ");
	for (int i = 0; i < q; i++) {
		printf("%d ", b[i]);
	}

	return 0;
}