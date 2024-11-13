// pesticide_broadcast.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/msg.h>

#define MSG_KEY 1234
#define BUFFER_SIZE 256

struct message {
    long msg_type;
    char msg_text[BUFFER_SIZE];
};

void broadcaster() {
    int msg_id;
    struct message msg;
    msg_id = msgget(MSG_KEY, 0666 | IPC_CREAT);
    msg.msg_type = 1;
    strcpy(msg.msg_text, "Pesticide Info: Use XYZ for best results.");
    msgsnd(msg_id, &msg, sizeof(msg), 0);
}

void listener() {
    int msg_id;
    struct message msg;
    msg_id = msgget(MSG_KEY, 0666 | IPC_CREAT);
    msgrcv(msg_id, &msg, sizeof(msg), 1, 0);
    printf("Broadcast: %s\n", msg.msg_text);
}

void query() {
    int msg_id;
    struct message msg;
    msg_id = msgget(MSG_KEY, 0666 | IPC_CREAT);
    msg.msg_type = 2;
    strcpy(msg.msg_text, "Query: What is the price of XYZ?");
    msgsnd(msg_id, &msg, sizeof(msg), 0);
}

int main() {
    pid_t pid;

    pid = fork();
    if (pid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    }

    if (pid == 0) {
        listener();
    } else {
        broadcaster();
        query();
    }

    return 0;
}