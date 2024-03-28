//Задан текст. Удалить первую букву в каждом слове.

#include <iostream>
#include <string> 
#include <Windows.h>
using namespace std;

int main()
{
    setlocale(LC_ALL, "Russian");
    
    // Для возможности обработки русских букв
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    int i = 0;
    string s;
   
    //Вводим строки с консоли
    cout << "Введите текст:\n";
    getline(cin, s);
    
    //Идём по строке и удаляем букву после каждого пробела.
    //erase() - удаляет элемент в строке. В качестве параметров она принимает начальный индекс удаления и количество удаляемых символов
    s = ' ' + s;
    while (s[i] != '\0')
    {
        if (s[i] == ' ' && s[i + 1] != ' ') s.erase(i + 1, 1);
        i++;
    }
    s.erase(0, 1);
    cout << s << endl;
    return 0;
}