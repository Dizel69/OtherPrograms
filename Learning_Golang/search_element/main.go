package main

import (
	"archive/zip"
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"strings"
)

func main() {
	// Имя архива (измените при необходимости)
	zipFile := "task.zip"

	// Открываем архив
	r, err := zip.OpenReader(zipFile)
	if err != nil {
		fmt.Printf("Ошибка открытия архива: %v\n", err)
		os.Exit(1)
	}
	defer r.Close()

	// Переменная для результата
	var result string

	// Обходим все файлы в архиве
	for _, f := range r.File {
		// Пропускаем директории
		if f.FileInfo().IsDir() {
			continue
		}

		// Открываем файл из архива
		rc, err := f.Open()
		if err != nil {
			fmt.Printf("Ошибка открытия файла %s: %v\n", f.Name, err)
			continue
		}

		// Читаем содержимое файла
		content, err := io.ReadAll(rc)
		rc.Close()
		if err != nil {
			fmt.Printf("Ошибка чтения файла %s: %v\n", f.Name, err)
			continue
		}

		// Пробуем прочитать как CSV
		reader := csv.NewReader(strings.NewReader(string(content)))
		reader.Comma = ',' // задаем разделитель

		// Читаем все записи
		records, err := reader.ReadAll()
		if err != nil {
			// Не CSV файл, пропускаем
			continue
		}

		// Проверяем размер таблицы (10x10)
		if len(records) != 10 {
			continue
		}

		valid := true
		for _, row := range records {
			if len(row) != 10 {
				valid = false
				break
			}
		}

		if !valid {
			continue
		}

		// Нашли подходящий файл
		// Получаем значение из 5 строки (индекс 4) и 3 столбца (индекс 2)
		if len(records) > 4 && len(records[4]) > 2 {
			result = records[4][2]
			fmt.Printf("Найден CSV файл: %s\n", f.Name)
			fmt.Printf("Результат: %s\n", result)
			break
		}
	}

	if result == "" {
		fmt.Println("Не удалось найти CSV файл 10x10 в архиве")
	}
}
