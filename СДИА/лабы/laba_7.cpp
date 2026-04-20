#include <iostream>
#include <vector>
#include <string>

using namespace std;

// Функция для построения префикс-функции
vector<int> buildPrefixFunction(const string& pattern) {
    int m = pattern.length();
    vector<int> pi(m, 0);

    for (int i = 1; i < m; i++) {
        int j = pi[i - 1];

        while (j > 0 && pattern[i] != pattern[j]) {
            j = pi[j - 1];
        }

        if (pattern[i] == pattern[j]) {
            j++;
        }

        pi[i] = j;
    }

    return pi;
}

// Функция поиска подстроки с помощью алгоритма КМП
vector<int> KMPSearch(const string& text, const string& pattern) {
    vector<int> occurrences;

    if (pattern.empty()) {
        return occurrences;
    }

    int n = text.length();
    int m = pattern.length();

    // Строим префикс-функцию для образца
    vector<int> pi = buildPrefixFunction(pattern);

    int j = 0; // количество совпавших символов

    for (int i = 0; i < n; i++) {
        // Пока есть несовпадение, уменьшаем j
        while (j > 0 && text[i] != pattern[j]) {
            j = pi[j - 1];
        }

        // Если символы совпадают
        if (text[i] == pattern[j]) {
            j++;
        }

        // Если нашли полное вхождение
        if (j == m) {
            occurrences.push_back(i - m + 1);
            j = pi[j - 1]; // продолжаем поиск следующих вхождений
        }
    }

    return occurrences;
}

int main() {
    setlocale(LC_ALL, "rus");
    string text, pattern;

    cout << "Введите текст (строку для поиска): ";
    getline(cin, text);

    cout << "Введите образец (подстроку для поиска): ";
    getline(cin, pattern);

    cout << "\nТекст: \"" << text << "\"" << endl;
    cout << "Образец: \"" << pattern << "\"" << endl;

    vector<int> result = KMPSearch(text, pattern);

    if (result.empty()) {
        cout << "\nОбразец не найден в тексте." << endl;
    }
    else {
        cout << "\nОбразец найден на позициях: ";
        for (size_t i = 0; i < result.size(); i++) {
            cout << result[i];
            if (i < result.size() - 1) {
                cout << ", ";
            }
        }
        cout << endl;

        
    }

    return 0;
}