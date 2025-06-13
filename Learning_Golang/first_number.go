// Дано неотрицательное целое число. Найдите и выведите первую цифру числа.
package main

import "fmt"

func main() {
	var n int
	fmt.Scan(&n)

	for n >= 10 {
		n = n / 10
	}

	fmt.Println(n)
}
