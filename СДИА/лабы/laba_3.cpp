#include <iostream>
#include <string>
#include <windows.h>
#include <iomanip>
using namespace std;

// структура для реализации узла дерева
struct tree
{
    int inf;              // значение узла
    tree* left;           // указатель на левого потомка
    tree* right;          // указатель на правого потомка
    tree* parent;         // указатель на родительский узел
};

// Глобальные переменные для работы с консолью
HANDLE output = GetStdHandle(STD_OUTPUT_HANDLE);
CONSOLE_SCREEN_BUFFER_INFO csbInfo;

// функция создания нового узла дерева
tree* node(int x)
{
    tree* node = new tree;
    node->inf = x;
    node->left = node->right = NULL;
    node->parent = NULL;
    return node;
}

// функция вставки узла в дерево
void insert(tree*& tr, int x)
{
    tree* n = node(x);
    if (!tr) tr = n;
    else
    {
        tree* y = tr;
        while (y)
        {
            if (n->inf > y->inf)
                if (y->right)
                    y = y->right;
                else
                {
                    n->parent = y;
                    y->right = n;
                    break;
                }
            else if (n->inf < y->inf)
                if (y->left)
                    y = y->left;
                else
                {
                    n->parent = y;
                    y->left = n;
                    break;
                }
        }
    }
}

// симметричный (in-order) обход дерева
void symmetric(tree* tr)
{
    if (tr)
    {
        symmetric(tr->left);
        cout << tr->inf << " ";
        symmetric(tr->right);
    }
}

// прямой (pre-order) обход
void forward(tree* tr)
{
    if (tr)
    {
        cout << tr->inf << " ";
        forward(tr->left);
        forward(tr->right);
    }
}

// обратный (post-order) обход
void backward(tree* tr)
{
    if (tr)
    {
        backward(tr->left);
        backward(tr->right);
        cout << tr->inf << " ";
    }
}

// рекурсивный поиск узла по значению
tree* find(tree* tr, int x)
{
    if (!tr || x == tr->inf)
        return tr;
    if (x < tr->inf)
        return find(tr->left, x);
    else
        return find(tr->right, x);
}

// поиск узла с минимальным значением
tree* Min(tree* tr)
{
    tree* curr = tr;
    while (curr && curr->left != nullptr)
        curr = curr->left;
    return curr;
}

// поиск узла с максимальным значением
tree* Max(tree* tr)
{
    tree* curr = tr;
    while (curr && curr->right != nullptr)
        curr = curr->right;
    return curr;
}

// поиск следующего узла
tree* Next(tree* tr, int x)
{
    tree* n = find(tr, x);
    if (!n) return nullptr;
    if (n->right)
        return Min(n->right);
    tree* y = n->parent;
    while (y && n == y->right)
    {
        n = y;
        y = y->parent;
    }
    return y;
}

// поиск предыдущего узла
tree* Prev(tree* tr, int x)
{
    tree* n = find(tr, x);
    if (!n) return nullptr;
    if (n->left)
        return Max(n->left);
    tree* y = n->parent;
    while (y && n == y->left)
    {
        n = y;
        y = y->parent;
    }
    return y;
}

// удаление узла по значению
tree* Delete(tree* tr, int x)
{
    if (tr == nullptr) return tr;

    if (x < tr->inf)
        tr->left = Delete(tr->left, x);
    else if (x > tr->inf)
        tr->right = Delete(tr->right, x);
    else
    {
        if (tr->left == nullptr)
        {
            tree* temp = tr->right;
            if (temp) temp->parent = tr->parent;
            delete tr;
            return temp;
        }
        else if (tr->right == nullptr)
        {
            tree* temp = tr->left;
            if (temp) temp->parent = tr->parent;
            delete tr;
            return temp;
        }

        tree* temp = Min(tr->right);
        tr->inf = temp->inf;
        tr->right = Delete(tr->right, temp->inf);
    }
    return tr;
}

// ========== ФУНКЦИИ ДЛЯ ВЫВОДА ДЕРЕВА ==========

// Функция вычисления высоты дерева
void max_height(tree* x, short& max, short deepness = 1)
{
    if (!x) return;
    if (deepness > max) max = deepness;
    if (x->left) max_height(x->left, max, deepness + 1);
    if (x->right) max_height(x->right, max, deepness + 1);
}

// Проверка достаточности размера консоли
bool isSizeOfConsoleCorrect(const short& width, const short& height)
{
    GetConsoleScreenBufferInfo(output, &csbInfo);
    COORD szOfConsole = csbInfo.dwSize;

    if (szOfConsole.X < width && szOfConsole.Y < height)
        cout << "Пожалуйста, увеличьте высоту и ширину терминала. ";
    else if (szOfConsole.X < width)
        cout << "Пожалуйста, увеличьте ширину терминала. ";
    else if (szOfConsole.Y < height)
        cout << "Пожалуйста, увеличьте высоту терминала. ";

    if (szOfConsole.X < width || szOfConsole.Y < height)
    {
        cout << "Текущий размер терминала: " << szOfConsole.X << " x " << szOfConsole.Y
            << ". Минимально необходимо: " << width << " x " << height << ".\n";
        return false;
    }
    return true;
}

// Вспомогательная рекурсивная функция для вывода дерева
void print_helper(tree* x, const COORD pos, const short offset)
{
    if (!x) return;

    SetConsoleCursorPosition(output, pos);
    cout << right << setw(offset + 1) << x->inf;

    if (x->left)
        print_helper(x->left, { pos.X, short(pos.Y + 1) }, offset >> 1);
    if (x->right)
        print_helper(x->right, { short(pos.X + offset), short(pos.Y + 1) }, offset >> 1);
}

// Очистка экрана и установка курсора в начало
void clearScreen()
{
    COORD topLeft = { 0, 0 };
    SetConsoleCursorPosition(output, topLeft);

    // Очищаем экран пробелами
    CONSOLE_SCREEN_BUFFER_INFO csbi;
    GetConsoleScreenBufferInfo(output, &csbi);
    DWORD written;
    DWORD cells = csbi.dwSize.X * csbi.dwSize.Y;
    FillConsoleOutputCharacter(output, ' ', cells, topLeft, &written);
    FillConsoleOutputAttribute(output, csbi.wAttributes, cells, topLeft, &written);
    SetConsoleCursorPosition(output, topLeft);
}

// Основная функция вывода дерева
void printTree(tree* root, const string& title = "")
{
    clearScreen();

    cout << title << endl;
    cout << string(80, '=') << endl;

    if (!root)
    {
        cout << "Дерево пустое!" << endl;
        return;
    }

    short max = 1;
    max_height(root, max);

    // Вычисляем необходимую ширину (4 символа на элемент на нижнем уровне)
    short width = 1 << (max + 1);  // 2^(max+1)
    short max_w = 120;  // максимальная ширина вывода
    if (width > max_w) width = max_w;

    // Проверяем размер консоли
    if (!isSizeOfConsoleCorrect(width, max))
    {
        cout << "Увеличьте размер консоли и нажмите любую клавишу..." << endl;
        system("pause");
    }

    // Резервируем место для вывода
    for (short i = 0; i < max; ++i)
        cout << '\n';

    // Получаем конечную позицию курсора
    GetConsoleScreenBufferInfo(output, &csbInfo);
    COORD endPos = csbInfo.dwCursorPosition;

    // Выводим дерево
    print_helper(root, { 0, short(endPos.Y - max) }, width >> 1);

    // Возвращаем курсор
    SetConsoleCursorPosition(output, endPos);
    cout << endl << endl;
}

// Функция для удаления узла с подтверждением и визуализацией
void deleteNodeWithVisualization(tree*& tr, int x, int stepNumber)
{
    cout << "\n=== ШАГ " << stepNumber << ": УДАЛЕНИЕ УЗЛА " << x << " ===\n";

    tree* node_to_delete = find(tr, x);

    if (!node_to_delete)
    {
        cout << "Узел " << x << " не найден в дереве!" << endl;
    }
    else
    {
        cout << "Узел " << x << " найден. Выполняется удаление...\n";
        tr = Delete(tr, x);
        printTree(tr, "ДЕРЕВО ПОСЛЕ УДАЛЕНИЯ УЗЛА " + to_string(x));

        cout << "Симметричный обход: "; symmetric(tr); cout << endl;
        cout << "Прямой обход: "; forward(tr); cout << endl;
        cout << "Обратный обход: "; backward(tr); cout << endl;
    }

    cout << "\nНажмите Enter для продолжения...";
    cin.ignore();
    cin.get();
}

// ========== ОСНОВНАЯ ФУНКЦИЯ ==========

int main()
{
    setlocale(LC_ALL, "rus");

    // Устанавливаем размер консоли (рекомендуется 120x40)
    system("mode con cols=120 lines=40");

    int n, x;
    cout << "Количество узлов: n = "; cin >> n;
    tree* tr = NULL;

    // Ввод значений и построение дерева
    for (int i = 0; i < n; ++i)
    {
        cout << i << ": ";
        cin >> x;
        if (find(tr, x))
        {
            cout << "Недопустимое значение (узел уже существует)" << endl;
            --i;
        }
        else
            insert(tr, x);
    }

    // Вывод начального дерева
    printTree(tr, "НАЧАЛЬНОЕ ДЕРЕВО");

    // Вывод обходов
    cout << "Симметричный обход (in-order): "; symmetric(tr); cout << endl;
    cout << "Прямой обход (pre-order): "; forward(tr); cout << endl;
    cout << "Обратный обход (post-order): "; backward(tr); cout << endl;

    cout << "\nmin = " << Min(tr)->inf << endl;
    cout << "max = " << Max(tr)->inf << endl;

    cout << "\nНажмите Enter для продолжения...";
    cin.ignore();
    cin.get();

    // ПЕРВОЕ УДАЛЕНИЕ
    cout << "\nВведите первый узел для удаления: "; cin >> x;
    deleteNodeWithVisualization(tr, x, 1);

    // ВТОРОЕ УДАЛЕНИЕ
    cout << "\nВведите второй узел для удаления: "; cin >> x;
    deleteNodeWithVisualization(tr, x, 2);

    // Финальное дерево после двух удалений 
    cout << "\n=== ФИНАЛЬНОЕ ДЕРЕВО ПОСЛЕ ДВУХ УДАЛЕНИЙ ===\n";
    printTree(tr, "ИТОГОВОЕ ДЕРЕВО");

    cout << "Симметричный обход: "; symmetric(tr); cout << endl;
    cout << "Прямой обход: "; forward(tr); cout << endl;
    cout << "Обратный обход: "; backward(tr); cout << endl;

    // Вставка нового узла (опционально)
    cout << "\nХотите вставить новый узел? (1 - да, 0 - нет): ";
    int choice;
    cin >> choice;

    if (choice == 1)
    {
        cout << "\nВведите узел, который желаете вставить: "; cin >> x;
        if (!find(tr, x))
        {
            insert(tr, x);
            printTree(tr, "ДЕРЕВО ПОСЛЕ ВСТАВКИ УЗЛА " + to_string(x));

            cout << "Симметричный обход: "; symmetric(tr); cout << endl;
            cout << "Прямой обход: "; forward(tr); cout << endl;
            cout << "Обратный обход: "; backward(tr); cout << endl;
        }
        else
        {
            cout << "Узел " << x << " уже существует в дереве!" << endl;
        }
    }

    cout << "\n";
    system("pause");
    return 0;
}