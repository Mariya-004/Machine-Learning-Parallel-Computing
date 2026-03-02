#include <iostream>
#include <thread>
#include <chrono>
#include <mutex>
#include <cstdlib>
#include <ctime>
using namespace std;
using namespace chrono;

int sum = 0;
int found = -1;
mutex m;

void partSum(int a[], int start, int end) {
    int localSum = 0;   // each thread uses its own local sum

    for(int i = start; i < end; i++)
        localSum += a[i];

    lock_guard<mutex> lock(m);   // safely update global sum
    sum += localSum;
}

void partSearch(int a[], int start, int end, int key) {
    for(int i = start; i < end; i++) {
        if(a[i] == key) {
            lock_guard<mutex> lock(m);
            if(found == -1)
                found = i;
            return;
        }
    }
}

int main() {
    int n, key;
    cout << "Enter size: ";
    cin >> n;

    if(n <= 0) {
        cout << "Invalid size!\n";
        return 0;
    }

    int* a = new int[n];

    srand(time(0));

    for(int i = 0; i < n; i++)
        a[i] = rand() % 100;

    cout << "Enter key to search: ";
    cin >> key;

    int mid = n / 2;

    // ---- SUM ----
    sum = 0;   // IMPORTANT reset

    auto start = high_resolution_clock::now();

    thread t1(partSum, a, 0, mid);
    thread t2(partSum, a, mid, n);

    t1.join();
    t2.join();

    auto stop = high_resolution_clock::now();

    cout << "\nThread Sum = " << sum << endl;
    cout << "Sum Time = "
         << duration_cast<microseconds>(stop - start).count()
         << " us\n";

    // ---- SEARCH ----
    found = -1;   // reset

    start = high_resolution_clock::now();

    thread t3(partSearch, a, 0, mid, key);
    thread t4(partSearch, a, mid, n, key);

    t3.join();
    t4.join();

    stop = high_resolution_clock::now();

    if(found != -1)
        cout << "\nKey found at index: " << found << endl;
    else
        cout << "\nKey not found\n";

    cout << "Search Time = "
         << duration_cast<microseconds>(stop - start).count()
         << " us\n";

    delete[] a;
    return 0;
}
