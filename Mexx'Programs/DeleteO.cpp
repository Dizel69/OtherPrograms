// Удалить из слов этого текста буквы о, стоящие на нечетных местах

#include <iostream>
#include <fstream>
using namespace std;

int main()
{
    int i = 0;
    char ch;
    string s;

    //Считываем файл
    ifstream in("input.txt");

    if (in.is_open())
    {
        while (in.get(ch))
        {
            if (ch != 'o' || (ch == 'o' && i % 2)) s += ch; // Проводим проверку на "o" и удаляем или пропускаем символ. 
            i++;
        }
        in.close();
    }
    else cout << "Невозможно открыть файл\n";

    cout << s << "\n";

    return 0;
}