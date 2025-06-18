//По данному трехзначному числу определите, все ли его цифры различны

package main

import "fmt"

func main() {
	var n int
	fmt.Scan(&n)

	a := n / 100     // Первая цифра (сотни)
	b := n / 10 % 10 // Вторая цифра (десятки)
	c := n % 10      // Третья цифра (единицы)

	if a != b && a != c && b != c {
		fmt.Println("YES")
	} else {
		fmt.Println("NO")
	}
}
