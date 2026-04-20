#include <iostream>
using namespace std;

void counting_sort(int arr[], int n, int k) {
    if (n <= 0) return;

    // Скобки () обнуляют все элементы
    int* count = new int[k + 1]();

    // Подсчитываем количество каждого элемента
    for (int i = 0; i < n; i++) {
        count[arr[i]]++;
    }

    // Преобразуем в массив накопленных частот
    for (int i = 1; i <= k; i++) {
        count[i] += count[i - 1];
    }

    // Создаем выходной массив
    int* ans = new int[n];

    // Заполняем с конца для стабильности
    for (int i = n - 1; i >= 0; i--) {
        ans[count[arr[i]] - 1] = arr[i];
        count[arr[i]]--;
    }

    // Копируем обратно
    for (int i = 0; i < n; i++) {
        arr[i] = ans[i];
    }

    delete[] count;
    delete[] ans;
}

// Вспомогательная функция: найти максимальный элемент
int getMax(int arr[], int n) {
    int mx = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] > mx) mx = arr[i];
    }
    return mx;
}

// Сортировка подсчетом по конкретному разряду 
void countSort_radix(int arr[], int n, int exp) {
    int* output = new int[n];  
    int count[10] = { 0 }; 

    // Подсчет цифр в текущем разряде
    for (int i = 0; i < n; i++) {
        count[(arr[i] / exp) % 10]++;
    }

    // Накопление частот
    for (int i = 1; i < 10; i++) {
        count[i] += count[i - 1];
    }

    // Заполнение выходного массива с конца
    for (int i = n - 1; i >= 0; i--) {
        int digit = (arr[i] / exp) % 10;
        output[count[digit] - 1] = arr[i];
        count[digit]--;
    }

    // Копируем результат обратно
    for (int i = 0; i < n; i++) {
        arr[i] = output[i];
    }

    delete[] output;
}

void radix_sort(int arr[], int n) {
    int m = getMax(arr, n); // Находим максимум для определения числа разрядов

    // Сортируем по каждому разряду, начиная с младшего 
    for (int exp = 1; m / exp > 0; exp *= 10) {
        countSort_radix(arr, n, exp);
    }
}

void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;
}

int main() {
    setlocale(LC_ALL, "rus");

    //  Сортировка подсчетом
    int t1[] = { 4, 2, 2, 8, 3, 3, 1 };
    int n1 = sizeof(t1) / sizeof(t1[0]);

    int k1 = 8;

    cout << "Counting Sort:" << endl;
    cout << "До: "; printArray(t1, n1);
    counting_sort(t1, n1, k1);
    cout << "После: "; printArray(t1, n1);
    cout << endl;

    //  Поразрядная сортировка
    int t2[] = { 170, 45, 75, 90, 802, 24, 2, 66 };
    int n2 = sizeof(t2) / sizeof(t2[0]);

    cout << "Radix Sort LSD:" << endl;
    cout << "До: "; printArray(t2, n2);
    radix_sort(t2, n2);
    cout << "После: "; printArray(t2, n2);

    return 0;
}