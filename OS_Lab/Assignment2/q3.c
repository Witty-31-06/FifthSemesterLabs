#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define BUFFER_SIZE 5   // Size of the buffer
#define P 3             // Number of producers
#define C 2             // Number of consumers

int buffer[BUFFER_SIZE];
int in = 0;             // Index for producers
int out = 0;            // Index for consumers

sem_t empty;            // Counts empty slots in the buffer
sem_t full;             // Counts filled slots in the buffer
pthread_mutex_t mutex;  // Mutual exclusion for buffer access

// Function to add an item to the buffer (for producers)
void put(int item) {
    buffer[in] = item;
    printf("Produced %d at index %d\n", item, in);
    in = (in + 1) % BUFFER_SIZE;  // Circular increment
}

// Function to remove an item from the buffer (for consumers)
int get() {
    int item = buffer[out];
    printf("Consumed %d from index %d\n", item, out);
    out = (out + 1) % BUFFER_SIZE;  // Circular increment
    return item;
}

// Producer thread function
void *producer(void *param) {
    int id = *(int *)param;
    while (1) {
        int item = rand() % 100;  // Produce a random item

        sem_wait(&empty);         // Wait for an empty slot
        pthread_mutex_lock(&mutex);  // Lock the buffer

        put(item);  // Place the item in the buffer

        pthread_mutex_unlock(&mutex); // Unlock the buffer
        sem_post(&full);              // Signal that an item is available

        printf("Producer %d sleeping\n", id);
        sleep(rand() % 3);  // Simulate work
    }
    pthread_exit(0);
}

// Consumer thread function
void *consumer(void *param) {
    int id = *(int *)param;
    while (1) {
        sem_wait(&full);             // Wait for a filled slot
        pthread_mutex_lock(&mutex);   // Lock the buffer

        int item = get();  // Remove an item from the buffer

        pthread_mutex_unlock(&mutex); // Unlock the buffer
        sem_post(&empty);             // Signal that a slot is empty

        printf("Consumer %d sleeping\n", id);
        sleep(rand() % 3);  // Simulate work
    }
    pthread_exit(0);
}

int main() {
    srand(time(NULL));

    pthread_t producers[P], consumers[C];
    int producer_ids[P], consumer_ids[C];

    // Initialize the semaphores and mutex
    sem_init(&empty, 0, BUFFER_SIZE);
    sem_init(&full, 0, 0);
    pthread_mutex_init(&mutex, NULL);

    // Create producer threads
    for (int i = 0; i < P; i++) {
        producer_ids[i] = i + 1;
        pthread_create(&producers[i], NULL, producer, &producer_ids[i]);
    }

    // Create consumer threads
    for (int i = 0; i < C; i++) {
        consumer_ids[i] = i + 1;
        pthread_create(&consumers[i], NULL, consumer, &consumer_ids[i]);
    }

    // Join threads (though with infinite loops, this will not terminate)
    for (int i = 0; i < P; i++) {
        pthread_join(producers[i], NULL);
    }
    for (int i = 0; i < C; i++) {
        pthread_join(consumers[i], NULL);
    }

    // Cleanup semaphores and mutex
    sem_destroy(&empty);
    sem_destroy(&full);
    pthread_mutex_destroy(&mutex);

    return 0;
}
