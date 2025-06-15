// Определите является ли билет счастливым. Счастливым считается билет, в
// шестизначном номере которого сумма первых трёх цифр совпадает с суммой трёх последних.
package main

import "fmt"

func main() {
	var n int
	fmt.Scan(&n)

	// Разбиваем число на отдельные цифры
	digit1 := n / 100000
	digit2 := n / 10000 % 10
	digit3 := n / 1000 % 10
	digit4 := n / 100 % 10
	digit5 := n / 10 % 10
	digit6 := n % 10

	// Считаем суммы первой и второй половины
	sumFirst := digit1 + digit2 + digit3
	sumSecond := digit4 + digit5 + digit6

	// Сравниваем суммы
	if sumFirst == sumSecond {
		fmt.Println("YES")
	} else {
		fmt.Println("NO")
	}
}
