package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
)

func main() {
	// Имена файлов
	dataFile := "data-20190514T0100.json"

	// Читаем файл с данными
	data, err := ioutil.ReadFile(dataFile)
	if err != nil {
		fmt.Printf("Ошибка чтения файла %s: %v\n", dataFile, err)
		os.Exit(1)
	}

	// Декодируем JSON в общую структуру
	var jsonData interface{}
	err = json.Unmarshal(data, &jsonData)
	if err != nil {
		fmt.Printf("Ошибка декодирования JSON: %v\n", err)
		os.Exit(1)
	}

	// Рекурсивно ищем и суммируем все global_id
	sum := findAndSumGlobalIDs(jsonData)

	fmt.Printf("Сумма всех global_id: %d\n", sum)
}

func findAndSumGlobalIDs(data interface{}) int64 {
	var sum int64 = 0

	// В зависимости от типа данных
	switch v := data.(type) {
	case map[string]interface{}:
		// Если это объект, проверяем наличие global_id
		if gid, ok := v["global_id"]; ok {
			if num, ok := gid.(float64); ok {
				sum += int64(num)
			}
		}

		// Рекурсивно проверяем все значения в объекте
		for _, value := range v {
			sum += findAndSumGlobalIDs(value)
		}

	case []interface{}:
		// Если это массив, рекурсивно проверяем все элементы
		for _, item := range v {
			sum += findAndSumGlobalIDs(item)
		}
	}

	return sum
}
