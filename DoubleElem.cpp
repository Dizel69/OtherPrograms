//Задан массив целых чисел. Вывести все числа, которые встречаются в этом массиве
//несколько раз

#include <iostream>
using namespace std;


int main()
{
	setlocale(LC_ALL, "Russian");

	const int n = 5;

	int A[n];
	// Заполняем массив
	printf("Введите элементы массива:\n");
	for (int i = 0; i < n; i++) {
		scanf_s("%d", &A[i]);
	}

	//Проверяем и выводим все встречающиеся элементы
	for (int i = 0; i < n; i++)
	{
		for (int y = 1; y < n; y++)
		{
			if (A[i] == A[y] && i != y) {
				cout << A[i] << " ";
				break;
			}
		}
	}
	cout << "\n";
}