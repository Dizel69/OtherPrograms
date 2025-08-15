package main

func main() {
	fibonacci(1, 2, 3, 4)
}

func fibonacci(n int) int {
	if n <= 2 {
		return 1
	}

	a, b := 1, 1
	for i := 3; i <= n; i++ {
		next := a + b
		a = b
		b = next
	}
	return b
}
