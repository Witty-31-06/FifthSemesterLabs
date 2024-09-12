#include <iostream>
#include <unistd.h>
#include <sys/wait.h>
#include <string>
#include <vector>
#include <sstream>
#include <cstdlib>
#include <cstring>
#include <dirent.h>

using namespace std;

// Function to split a string into tokens (command and arguments)
vector<string> parseInput(string input) {
    vector<string> tokens;
    stringstream ss(input);
    string token;
    while (ss >> token) {
        tokens.push_back(token);
    }
    return tokens;
}

// Function to handle "cd" command
void changeDirectory(const vector<string>& args) {
    if (args.size() < 2) {
        cerr << "cd: missing argument\n";
    } else {
        if (chdir(args[1].c_str()) != 0) {
            perror("cd");
        }
    }
}

// Function to handle "pwd" command
void printWorkingDirectory() {
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        cout << cwd << endl;
    } else {
        perror("pwd");
    }
}

// Function to execute system commands like "ls", "echo", etc.
void executeCommand(const vector<string>& args) {
    pid_t pid = fork();
    if (pid == 0) {
        // Child process
        vector<char*> c_args;
        for (const auto& arg : args) {
            c_args.push_back(const_cast<char*>(arg.c_str()));
        }
        c_args.push_back(NULL);

        if (execvp(c_args[0], c_args.data()) == -1) {
            perror("execvp");
        }
        exit(EXIT_FAILURE);
    } else if (pid < 0) {
        // Error forking
        perror("fork");
    } else {
        // Parent process
        wait(NULL); // Wait for the child process to complete
    }
}

int main() {
    string input;
    while (true) {
        cout << "xxxx-shell> ";
        getline(cin, input);

        // Parse the input
        vector<string> args = parseInput(input);

        if (args.empty()) continue; // Empty input, continue to the next iteration

        // Handle built-in commands
        if (args[0] == "cd") {
            changeDirectory(args);
        } else if (args[0] == "pwd") {
            printWorkingDirectory();
        } else if (args[0] == "exit") {
            break; // Exit the shell
        } else {
            // Execute other commands like ls, echo, etc.
            executeCommand(args);
        }
    }

    return 0;
}
