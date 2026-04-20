#include <iostream>
#include <vector>
#include <string>

using namespace std;

// Функция вычисляет префикс-функцию для строки
// pi[i] = длина наибольшего префикса, который также является суффиксом для s[0..i]
vector<int> prefixFunction(string s) {
    int n = s.size();
    vector<int> pi(n, 0);  // создаём массив нулей

    for (int i = 1; i < n; i++) {
        int j = pi[i - 1];  // берём предыдущее значение

        // "откатываемся" назад, пока символы не совпадут
        while (j > 0 && s[i] != s[j]) {
            j = pi[j - 1];
        }

        // если символы совпали — увеличиваем длину
        if (s[i] == s[j]) {
            j++;
        }

        pi[i] = j;  // сохраняем результат
    }
    return pi;
}

// Функция вычисляет Z-функцию для строки
// z[i] = длина наибольшего префикса строки, совпадающего с подстрокой, начинающейся в i
vector<int> zFunction(string s) {
    int n = s.size();
    vector<int> z(n, 0);  // создаём массив нулей

    int l = 0, r = 0;  // границы отрезка, совпадающего с префиксом

    for (int i = 1; i < n; i++) {
        // если мы внутри "хорошего" отрезка — используем ранее посчитанное
        if (i <= r) {
            if (r - i + 1 < z[i - l]) {
                z[i] = r - i + 1;
            }
            else {
                z[i] = z[i - l];
            }
        }

        // пытаемся "доподсчитать" символы вперёд
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) {
            z[i]++;
        }

        // если расширили отрезок — обновляем границы
        if (i + z[i] - 1 > r) {
            l = i;
            r = i + z[i] - 1;
        }
    }
    return z;
}

int main() {
    setlocale(LC_ALL, "rus");
    string s;

    // Ввод строки от пользователя
    cout << "Введите строку: ";
    getline(cin, s);


    // Вычисляем функции
    vector<int> prefix = prefixFunction(s);
    vector<int> z = zFunction(s);

    // Вывод префикс-функции
    cout << "\nPrefix function: ";
    for (int i = 0; i < prefix.size(); i++) {
        cout << prefix[i] << " ";
    }
    cout << endl;

    // Вывод Z-функции
    cout << "Z-function: ";
    for (int i = 0; i < z.size(); i++) {
        cout << z[i] << " ";
    }
    cout << endl;

    return 0;
}