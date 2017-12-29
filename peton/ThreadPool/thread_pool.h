#ifndef THREAD_POOL
#define THREAD_POOL
#include "pthread.h"
#include <vector>
#include <queue>
struct Task {
    void (*f)(void*);
    void* arg;
    pthread_mutex_t m;
    
    pthread_cond_t iscompleted_cond;
    bool iscompleted_bool;
};

struct ThreadPool {
	bool end;
    pthread_mutex_t mutex;     
    std::vector<pthread_t> threads;
    std::queue<Task*> tasks;
    pthread_cond_t new_task;
    pthread_cond_t task_is_done;
    unsigned active_threads;
};

void thpool_init(ThreadPool* pool, unsigned threads_nm);
void thpool_submit(ThreadPool* pool, struct Task* task);
void thpool_wait(Task* task);
void thpool_finit(ThreadPool* pool);
#endif
