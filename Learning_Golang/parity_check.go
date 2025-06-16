// Проверка числа на чётность
package main

import "fmt"

func main() {
	var a int
	fmt.Scan(&a)
	if a%2 == 0 {
		fmt.Println("Число чётно")
	} else {
		fmt.Println("Нет")
	}
}
