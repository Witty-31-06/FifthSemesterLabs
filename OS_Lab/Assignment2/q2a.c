// Create child processes: X and Y.
// a. Each child process performs 10 iterations. The child process displays its name/id and the current
// iteration number, and sleeps for some random amount of time. Adjust the sleeping duration of the
// processes to have different outputs (i.e. another interleaving of processes’ traces).
// b. Modify the program so that X is not allowed to start iteration i before process Y has terminated
// its own iteration i-1. Use semaphore to implement this synchronization.

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <sys/wait.h>
void loop(int pid, int wait) {

    for(int i = 0; i<10; i++) {
        printf("%Process %d: iteration %d\n", pid, i);
        sleep(wait);
    }
}
int main() {
    int wait_time = 1;
    srand(time(NULL));
    int pid = fork();
    if(pid < 0) {
        perror("Fork failed\n");
    } else if(pid == 0) {
        loop(pid, wait_time);
    } else {
        loop(pid, wait_time);
    }
    wait(NULL);
    return 0;

}
