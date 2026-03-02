#include <iostream>
#include <vector>
#include <cstdlib>
#include <chrono>
using namespace std;
using namespace chrono;

long long findSum(vector<int>& a, int n) {
    long long sum = 0;
    for(int i = 0; i < n; i++)
        sum += a[i];
    return sum;
}

int searchKey(vector<int>& a, int n, int key) {
    for(int i = 0; i < n; i++)
        if(a[i] == key)
            return i;
    return -1;
}

int main() {
    int n, key;

    cout << "Enter number of elements: ";
    cin >> n;

    vector<int> a(n);

    cout << "Generating " << n << " random numbers (0–999)...\n";
    for(int i = 0; i < n; i++)
        a[i] = rand() % 1000;

    cout << "Enter key to search: ";
    cin >> key;

    // Measure sum time
    auto t1 = high_resolution_clock::now();
    long long total = findSum(a, n);
    auto t2 = high_resolution_clock::now();

    cout << "\nSum = " << total << endl;
    cout << "Time taken to compute sum = "
         << duration_cast<microseconds>(t2 - t1).count()
         << " microseconds\n";

    // Measure search time
    t1 = high_resolution_clock::now();
    int pos = searchKey(a, n, key);
    t2 = high_resolution_clock::now();

    if(pos != -1)
        cout << "\nKey found at index: " << pos << endl;
    else
        cout << "\nKey not found in the array.\n";

    cout << "Time taken to search = "
         << duration_cast<microseconds>(t2 - t1).count()
         << " microseconds\n";

    return 0;
}
