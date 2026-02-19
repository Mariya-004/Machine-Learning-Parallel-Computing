// ---------------------------------------------
// Program to create a thread to print
// first n natural numbers
// ---------------------------------------------

#include <iostream>
#include <thread>

using namespace std;

// Function that will be executed by the thread
void printNumbers(int n)
{
    cout << "First " << n << " natural numbers are:\n";
    
    for(int i = 1; i <= n; i++)
    {
        cout << i << " ";
    }
    
    cout << endl;
}

int main()
{
    int n;

    cout << "Enter the value of n: ";
    cin >> n;

    // Create a thread and pass the function with argument
    thread t1(printNumbers, n);

    // Wait for thread to finish execution
    t1.join();

    return 0;
}
