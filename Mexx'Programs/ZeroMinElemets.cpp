//Задана матрица целых чисел. Записать нули в строку, в которой находится min элемент


#include <iostream>
#include <time.h>

using namespace std;

void main()
{
    srand(time(NULL));
    setlocale(LC_ALL, "ru");
    const int M = 5, N = 5;
    int A[N][M], min, imin = 0;
    cout << "Исходная матрица:" << endl;
   //Заполняем матрицу и сразу ищем минимальный элемент
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < M; j++)
        {
            A[i][j] = 0 + rand() % 201;
            cout << A[i][j] << " ";
            if (!i && !j) min = A[0][0]; //проверка на минимальный элемент
            else if (min > A[i][j])
            {
                min = A[i][j];
                imin = i;
            }
        }
        cout << endl;
    }

    //Выводим результат
    cout << "Минимальный элемент = " << min << endl;
    cout << "Конечная матрица: " << endl;
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < M; j++)
        {
            if (i == imin)
                A[i][j] = 0;
            cout << A[i][j] << " ";
        }
        cout << endl;
    }
    system("pause");
}