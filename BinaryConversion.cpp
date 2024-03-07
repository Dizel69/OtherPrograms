﻿// Переводит число из десятичной степени счислени в двоичную


#include <iostream>

int main() {
	int bin = 0;
	int n;
	scanf_s("%d", &n);
	int rem, i = 1;
	while (n != 0) {
		rem = n % 2;
		n /= 2;
		bin += rem * i;
		i *= 10;
	}

	printf("%d", bin);

}