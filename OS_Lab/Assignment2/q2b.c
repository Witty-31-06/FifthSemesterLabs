#include <stdio.h>
#include <stdlib.h>
#include <semaphore.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h>

#define SEM_NAME "/mysem"

void loopY(sem_t *sem) {
    for(int i = 0; i < 10; i++) {
        sem_wait(sem);  // Wait for X to finish iteration i-1
        printf("Process Y: iteration %d\n", i);
        sleep(1);       // Simulate some work
        sem_post(sem);  // Allow X to start iteration i
    }
}

void loopX(sem_t *sem) {
    for(int i = 0; i < 10; i++) {
        sem_wait(sem);  // Wait for Y to finish iteration i-1
        printf("Process X: iteration %d\n", i);
        sleep(1);       // Simulate some work
        sem_post(sem);  // Allow Y to proceed to next iteration
    }
}

int main() {
    sem_t *sem = sem_open(SEM_NAME, O_CREAT | O_EXCL, 0644, 1);
    if (sem == SEM_FAILED) {
        perror("Semaphore creation failed");
        return 1;
    }

    pid_t pidX = fork();
    if (pidX < 0) {
        perror("Fork for X failed");
        sem_unlink(SEM_NAME);
        return 1;
    } else if (pidX == 0) {
        // Child process X
        sem_t *semX = sem_open(SEM_NAME, 0);
        if (semX == SEM_FAILED) {
            perror("sem_open failed in child X");
            exit(1);
        }
        loopX(semX);
        sem_close(semX);
        exit(0);
    }

    pid_t pidY = fork();
    if (pidY < 0) {
        perror("Fork for Y failed");
        sem_unlink(SEM_NAME);
        return 1;
    } else if (pidY == 0) {
        // Child process Y
        sem_t *semY = sem_open(SEM_NAME, 0);
        if (semY == SEM_FAILED) {
            perror("sem_open failed in child Y");
            exit(1);
        }
        loopY(semY);
        sem_close(semY);
        exit(0);
    }

    // Parent process waits for both children to finish
    wait(NULL);
    wait(NULL);

    // Cleanup semaphore in the parent process
    sem_close(sem);
    sem_unlink(SEM_NAME);

    return 0;
}
