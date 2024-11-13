// weather_broadcast.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define BUFFER_SIZE 256

void broadcaster(int pipe_fd) {
    char weather_info[] = "Sunny, 25°C";
    write(pipe_fd, weather_info, strlen(weather_info) + 1);
    close(pipe_fd);
}

void listener(int pipe_fd) {
    char buffer[BUFFER_SIZE];
    read(pipe_fd, buffer, BUFFER_SIZE);
    printf("Weather Info: %s\n", buffer);
    close(pipe_fd);
}

int main() {
    int pipe_fd[2];
    int pid;

    if (pipe(pipe_fd) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    pid = fork();
    if (pid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    }

    if (pid == 0) {
        close(pipe_fd[1]);
        listener(pipe_fd[0]);
    } else {
        close(pipe_fd[0]);
        broadcaster(pipe_fd[1]);
    }

    return 0;
}