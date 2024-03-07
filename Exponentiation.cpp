// Задано натуральное число n. 
// Вычислить сумму n^2+(n+1)^2+...+(2n)^2

#include <iostream>
#include <cmath>
using namespace std;

int main()
{
	setlocale(0, "rus");
	//Записываем натуральное число
	int n;
	cout << "Введите натуральное число: ";
	cin >> n;

	//Возводим число в степень
	int sum = 0;
	for (int i = n; i <= n * 2; i++) {
		sum += pow(n, 2); //Функция pow из библиотеки <cmath> позволяет возводить число n в степень 2
	}
	cout << "Sum = " << sum;
}