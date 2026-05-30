package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

func main() {
	filename := "task.data"

	file, err := os.Open(filename)
	if err != nil {
		fmt.Printf("Ошибка открытия файла: %v\n", err)
		os.Exit(1)
	}
	defer file.Close()

	reader := bufio.NewReader(file)
	position := 0

	for {
		// Читаем до следующего разделителя ';'
		data, err := reader.ReadBytes(';')

		position++

		// Убираем разделитель из данных (если он есть)
		var numStr string
		if len(data) > 0 {
			// Если последний символ - ';', убираем его
			if data[len(data)-1] == ';' {
				numStr = string(data[:len(data)-1])
			} else {
				numStr = string(data)
			}
		}

		// Проверяем, является ли число нулем
		if strings.TrimSpace(numStr) == "0" {
			fmt.Printf("Число 0 найдено на позиции: %d\n", position)
			return
		}

		// Проверяем ошибки
		if err != nil {
			if err == io.EOF {
				break
			}
			fmt.Printf("Ошибка чтения файла: %v\n", err)
			os.Exit(1)
		}
	}

	fmt.Println("Число 0 не найдено в файле")
}
