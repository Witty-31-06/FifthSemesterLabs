#include <eigen3/Eigen/Dense>
#include <iostream>
#include <vector>
#include <string>
using namespace std;

typedef Eigen::MatrixXi walshMatrix;
walshMatrix generateWalshMatrix(int n) {
    if (n == 1) {
        return walshMatrix::Ones(1, 1);
    } else {
        int half = n / 2;
        walshMatrix H = generateWalshMatrix(half);

        walshMatrix walsh(n, n);
        walsh.topLeftCorner(half, half) = H;
        walsh.topRightCorner(half, half) = H;
        walsh.bottomLeftCorner(half, half) = H;
        walsh.bottomRightCorner(half, half) = -H;

        return walsh;
    }
}

walshMatrix WalshMatrix(int numStations)
{
    int order = 1;
    while(order < numStations)
    {
        order = order*2;

    }
    return generateWalshMatrix(order);
}


void simulate(int n, walshMatrix code)
{
    vector<int> stationData(n);
    cout<<"Enter the data to be sent by stations separated by space: ";
    char input;
    for(int i = 0; i<n; i++)
    {
        cin>>input;
        // cout<<input;
        if(input == '1') stationData[i] = 1;
        else if(input == '0') stationData[i] = -1;
        else stationData[i] = 0;
    }

    Eigen::RowVectorXi channel = Eigen::VectorXi::Zero(code.cols());

    // Compute the channel signal
    for(int i = 0; i < n; ++i)
    {
        channel += stationData[i] * code.row(i);
    }

    cout<<"Data in Channel: "<<channel<<endl;

    for(int i = 0; i<n; i++)
    {
        int value = channel.dot(code.row(i))/code.rows();
        string data;
        if(value > 0) data = "1";
        else if(value<0) data = "0";
        else data = "No data";
        cout<<"Station "<< i+1 << " sent data "<< data <<endl;
    }
    



}
int main()
{
    int n;
    cout<<"Enter the number of stations in network: ";
    cin>>n;
    walshMatrix codes = WalshMatrix(n);

    cout<<"Walsh Matrix for "<<n<<" stations: "<<endl;
    cout<<codes<<endl;
    while (true) simulate(n, codes);
}