#ifndef THREAD_POOL
#define THREAD_POOL
#include "pthread.h"
#include <vector>
#include <queue>
struct Task {
    void (*f)(void*);
    void* arg;
    pthread_mutex_t m;
    pthread_cond_t is_completed;
};

struct ThreadPool {
	unsigned active_threads;
	bool end;
	pthread_mutex_t m_end;
    pthread_mutex_t mutex;     
    pthread_cond_t cond;    
    std::vector<pthread_t> threads;
    std::queue<Task> tasks;
};

void thpool_init(ThreadPool* pool, unsigned threads_nm);
void thpool_submit(ThreadPool* pool, struct Task* task);
void thpool_wait(Task* task);
void thpool_finit(ThreadPool* pool);
#endif
