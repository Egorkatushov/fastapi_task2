#include <iostream>
#include <string>
#include <windows.h>
#include <iomanip>
using namespace std;

enum Color { RED, BLACK };
HANDLE output = GetStdHandle(STD_OUTPUT_HANDLE);
CONSOLE_SCREEN_BUFFER_INFO csbInfo;

template <typename T>
class RedBlackTree {
private:
    struct Node {
        T data;
        Color color;
        Node* parent;
        Node* left;
        Node* right;
        Node(T value) : data(value), color(RED), parent(nullptr), left(nullptr), right(nullptr) {}
    };

    Node* root;
    Node* NIL;

    void leftRotate(Node* x) {
        Node* y = x->right;
        x->right = y->left;
        if (y->left != NIL) y->left->parent = x;
        y->parent = x->parent;
        if (x->parent == NIL) root = y;
        else if (x == x->parent->left) x->parent->left = y;
        else x->parent->right = y;
        y->left = x;
        x->parent = y;
    }

    void rightRotate(Node* x) {
        Node* y = x->left;
        x->left = y->right;
        if (y->right != NIL) y->right->parent = x;
        y->parent = x->parent;
        if (x->parent == NIL) root = y;
        else if (x == x->parent->right) x->parent->right = y;
        else x->parent->left = y;
        y->right = x;
        x->parent = y;
    }

    void fixInsert(Node* z) {
        while (z->parent->color == RED) {
            if (z->parent == z->parent->parent->left) {
                Node* y = z->parent->parent->right;
                if (y->color == RED) {
                    z->parent->color = BLACK;
                    y->color = BLACK;
                    z->parent->parent->color = RED;
                    z = z->parent->parent;
                }
                else {
                    if (z == z->parent->right) {
                        z = z->parent;
                        leftRotate(z);
                    }
                    z->parent->color = BLACK;
                    z->parent->parent->color = RED;
                    rightRotate(z->parent->parent);
                }
            }
            else {
                Node* y = z->parent->parent->left;
                if (y->color == RED) {
                    z->parent->color = BLACK;
                    y->color = BLACK;
                    z->parent->parent->color = RED;
                    z = z->parent->parent;
                }
                else {
                    if (z == z->parent->left) {
                        z = z->parent;
                        rightRotate(z);
                    }
                    z->parent->color = BLACK;
                    z->parent->parent->color = RED;
                    leftRotate(z->parent->parent);
                }
            }
        }
        root->color = BLACK;
    }

    void transplant(Node* u, Node* v) {
        if (u->parent == NIL) root = v;
        else if (u == u->parent->left) u->parent->left = v;
        else u->parent->right = v;
        v->parent = u->parent;
    }

    // Функция для поиска максимального узла (предшественника)
    Node* maxValueNode(Node* node) {
        while (node->right != NIL) node = node->right;
        return node;
    }

    void fixDelete(Node* x) {
        while (x != root && x->color == BLACK) {
            if (x == x->parent->left) {
                Node* w = x->parent->right;
                if (w->color == RED) {
                    w->color = BLACK;
                    x->parent->color = RED;
                    leftRotate(x->parent);
                    w = x->parent->right;
                }
                if (w->left->color == BLACK && w->right->color == BLACK) {
                    w->color = RED;
                    x = x->parent;
                }
                else {
                    if (w->right->color == BLACK) {
                        w->left->color = BLACK;
                        w->color = RED;
                        rightRotate(w);
                        w = x->parent->right;
                    }
                    w->color = x->parent->color;
                    x->parent->color = BLACK;
                    w->right->color = BLACK;
                    leftRotate(x->parent);
                    x = root;
                }
            }
            else {
                Node* w = x->parent->left;
                if (w->color == RED) {
                    w->color = BLACK;
                    x->parent->color = RED;
                    rightRotate(x->parent);
                    w = x->parent->left;
                }
                if (w->right->color == BLACK && w->left->color == BLACK) {
                    w->color = RED;
                    x = x->parent;
                }
                else {
                    if (w->left->color == BLACK) {
                        w->right->color = BLACK;
                        w->color = RED;
                        leftRotate(w);
                        w = x->parent->left;
                    }
                    w->color = x->parent->color;
                    x->parent->color = BLACK;
                    w->left->color = BLACK;
                    rightRotate(x->parent);
                    x = root;
                }
            }
        }
        x->color = BLACK;
    }

    void deleteTree(Node* node) {
        if (node != NIL) {
            deleteTree(node->left);
            deleteTree(node->right);
            delete node;
        }
    }

    void getHeightHelper(Node* node, short& max, short deepness = 1) {
        if (node == NIL) return;
        if (deepness > max) max = deepness;
        if (node->left != NIL) getHeightHelper(node->left, max, deepness + 1);
        if (node->right != NIL) getHeightHelper(node->right, max, deepness + 1);
    }

    void printHelper(Node* x, const COORD pos, const short offset) {
        if (x == NIL) return;
        SetConsoleCursorPosition(output, pos);
        SetConsoleTextAttribute(output, x->color == RED ? 12 : 15);
        cout << right << setw(offset + 1) << x->data;
        SetConsoleTextAttribute(output, 7);
        if (x->left != NIL) printHelper(x->left, { pos.X, short(pos.Y + 1) }, offset >> 1);
        if (x->right != NIL) printHelper(x->right, { short(pos.X + offset), short(pos.Y + 1) }, offset >> 1);
    }

    bool isSizeOfConsoleCorrect(const short& width, const short& height) {
        GetConsoleScreenBufferInfo(output, &csbInfo);
        COORD sz = csbInfo.dwSize;
        if (sz.X < width || sz.Y < height) {
            cout << "Увеличьте терминал до " << width << "x" << height << "\n";
            return false;
        }
        return true;
    }

    void clearScreen() {
        COORD topLeft = { 0, 0 };
        SetConsoleCursorPosition(output, topLeft);
        CONSOLE_SCREEN_BUFFER_INFO csbi;
        GetConsoleScreenBufferInfo(output, &csbi);
        DWORD written;
        DWORD cells = csbi.dwSize.X * csbi.dwSize.Y;
        FillConsoleOutputCharacter(output, ' ', cells, topLeft, &written);
        FillConsoleOutputAttribute(output, csbi.wAttributes, cells, topLeft, &written);
        SetConsoleCursorPosition(output, topLeft);
    }

    void printElementsHelper(Node* node) {
        if (node != NIL) {
            printElementsHelper(node->left);
            cout << node->data << " ";
            printElementsHelper(node->right);
        }
    }

public:
    RedBlackTree() {
        NIL = new Node(T());
        NIL->color = BLACK;
        NIL->left = NIL->right = NIL->parent = NIL;
        root = NIL;
    }

    ~RedBlackTree() { deleteTree(root); delete NIL; }
    bool isEmpty() { return root == NIL; }
    short getHeight() { short max = 1; getHeightHelper(root, max); return max; }

    void printTree(const string& title = "") {
        clearScreen();
        cout << title << "\n" << string(50, '=') << "\n";
        if (isEmpty()) { cout << "Дерево пустое!\n"; return; }
        short max = getHeight();
        short width = 1 << (max + 1);
        if (width > 120) width = 120;
        if (!isSizeOfConsoleCorrect(width, max)) { system("pause"); return; }
        for (short i = 0; i < max; ++i) cout << '\n';
        GetConsoleScreenBufferInfo(output, &csbInfo);
        COORD endPos = csbInfo.dwCursorPosition;
        SetConsoleTextAttribute(output, 12); cout << "Красный";
        SetConsoleTextAttribute(output, 7); cout << "-R ";
        SetConsoleTextAttribute(output, 15); cout << "Белый";
        SetConsoleTextAttribute(output, 7); cout << "-B\n\n";
        printHelper(root, { 0, short(endPos.Y - max) }, width >> 1);
        SetConsoleCursorPosition(output, endPos);
        cout << "\n\n";
    }

    void insert(T key) {
        Node* node = new Node(key);
        node->left = node->right = node->parent = NIL;
        Node* y = NIL;
        Node* x = root;
        while (x != NIL) {
            y = x;
            if (node->data < x->data) x = x->left;
            else x = x->right;
        }
        node->parent = y;
        if (y == NIL) root = node;
        else if (node->data < y->data) y->left = node;
        else y->right = node;
        node->color = RED;
        fixInsert(node);
    }

    void remove(T key) {
        Node* z = root;
        Node* x;
        Node* y;

        // Поиск узла для удаления
        while (z != NIL) {
            if (z->data == key) break;
            else if (key < z->data) z = z->left;
            else z = z->right;
        }

        if (z == NIL) {
            cout << "Узел " << key << " не найден!\n";
            return;
        }

        y = z;
        Color yOriginalColor = y->color;

        if (z->left == NIL) {
            // Случай 1: нет левого потомка
            x = z->right;
            transplant(z, z->right);
        }
        else if (z->right == NIL) {
            // Случай 2: нет правого потомка
            x = z->left;
            transplant(z, z->left);
        }
        else {
            // Случай 3: есть оба потомка - используем ПРЕДШЕСТВЕННИКА (максимальный в левом поддереве)
            y = maxValueNode(z->left); // Ищем максимальный узел в ЛЕВОМ поддереве
            yOriginalColor = y->color;
            x = y->left; // У предшественника нет правого потомка, только левый возможен

            if (y->parent == z) {
                // Если предшественник - прямой потомок
                if (x != NIL) x->parent = y;
            }
            else {
                // Предшественник не прямой потомок
                transplant(y, y->left);
                y->left = z->left;
                y->left->parent = y;
            }

            transplant(z, y);
            y->right = z->right;
            if (y->right != NIL) y->right->parent = y;
            y->color = z->color;
        }

        delete z;

        if (yOriginalColor == BLACK) {
            if (x != NIL) fixDelete(x);
            else if (root != NIL) fixDelete(NIL); // Специальный случай
        }

        if (root != NIL) root->color = BLACK;
        cout << "Узел " << key << " удален!\n";
    }

    bool find(T key) {
        Node* node = root;
        while (node != NIL) {
            if (key == node->data) return true;
            else if (key < node->data) node = node->left;
            else node = node->right;
        }
        return false;
    }

    T getMin() { if (isEmpty()) return T(); Node* node = root; while (node->left != NIL) node = node->left; return node->data; }
    T getMax() { if (isEmpty()) return T(); Node* node = root; while (node->right != NIL) node = node->right; return node->data; }
    T getRoot() { if (isEmpty()) return T(); return root->data; }

    void buildFromArray(const int arr[], int size) {
        cout << "Массив: ";
        for (int i = 0; i < size; i++) cout << arr[i] << " ";
        cout << "\nПостроение дерева...\n";
        for (int i = 0; i < size; i++) insert(arr[i]);
    }

    void printElements() { cout << "Элементы: "; printElementsHelper(root); cout << endl; }
};

int main() {
    setlocale(LC_ALL, "rus");
    system("mode con cols=120 lines=40");
    RedBlackTree<int> rbt;
    const int size = 12;
    int arr[size] = { 41, 48, 45, 43, 30, 35, 38, 37, 36, 16, 20, 25 };

    rbt.buildFromArray(arr, size);
    rbt.printTree("НАЧАЛЬНОЕ ДЕРЕВО");
    cout << "Корень: " << rbt.getRoot() << " Min: " << rbt.getMin() << " Max: " << rbt.getMax() << "\n";
    cout << "\nНажмите Enter..."; cin.ignore(); cin.get();

    int del;
    cout << "Узел 1 для удаления: "; cin >> del; cin.ignore();
    rbt.remove(del);
    rbt.printTree("ПОСЛЕ УДАЛЕНИЯ " + to_string(del));
    if (!rbt.isEmpty()) cout << "Корень: " << rbt.getRoot() << "\n";
    cout << "\nНажмите Enter..."; cin.get();

    cout << "Узел 2 для удаления: "; cin >> del; cin.ignore();
    rbt.remove(del);
    rbt.printTree("ПОСЛЕ УДАЛЕНИЯ " + to_string(del));
    if (!rbt.isEmpty()) {
        cout << "Корень: " << rbt.getRoot() << " Min: " << rbt.getMin() << " Max: " << rbt.getMax() << "\n";
        rbt.printElements();
    }

    rbt.printTree("ИТОГОВОЕ ДЕРЕВО");
    system("pause");
    return 0;
}