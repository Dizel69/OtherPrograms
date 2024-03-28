//Удалить строку и столбец, на пересечении которых расположен 
// наименьший по модулю элемент матрицы

#include <iostream>
using namespace std;

//Удаление строки
void DeleteRow(int** A, int k, int N, int M)
{
    for (int i = k; i < N - 1; i++)
    {
        for (int j = 0; j < M; j++)
        {
            A[i][j] = A[i + 1][j];
        }
    }
}

// удаление столбца
void DeleteColumn(int** A, int k, int N, int M)
{
    for (int i = 0; i < N; i++)
    {
        for (int j = k; j < M - 1; j++)
        {
            A[i][j] = A[i][j + 1];
        }
    }
}

//Заполнение матрицы
void MatrixInput(int** A, int N, int M)
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < M; j++)
        {
            cin >> A[i][j];
        }
    }
}

//Вывод матрицы
void MatrixOutput(int** A, int N, int M)
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < M; j++)
        {
            cout << A[i][j] << " ";
        }
        cout << endl;
    }
}

int main()
{
    setlocale(0, "rus");
    int N, M, x, y, min;
    cout << "Введите размерность матрицы:" << endl;
    cout << "N = ";
    cin >> N;
    cout << "M = ";
    cin >> M;
    int** A = new int* [N];
    for (int i = 0; i < N; i++)
    {
        A[i] = new int[M];
    }
    cout << "Введите матрицу:" << endl;
    MatrixInput(A, N, M);
    min = INT_MAX;
   //Ищем минимальный по модулю элемент
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < M; j++)
        {
            if (abs(A[i][j] < min))
            {
                min = abs(A[i][j]);
                x = i;
                y = j;
            }
        }
    }
   
    cout << "Найденный элемент: " << min << "\n";
    

    DeleteRow(A, x, N, M);
    DeleteColumn(A, y, N, M);

    cout << "Итоговая матрица:" << endl;
    MatrixOutput(A, N - 1, M - 1);
    for (int i = 0; i < N; i++)
    {
        delete[] A[i];
    }
    delete[] A;
    return 0;
}