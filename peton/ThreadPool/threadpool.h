#ifndef THREAD_POOL
#define THREAD_POOL

struct Task {
    bool is_completed;    
    void (*f)(void*);
    void* arg;
    pthread_mutex_t m;
};

struct ThreadPool {
    pthread_mutex_t mutex;     
    pthread_cond_t cond;    
    vector<pthread_t>;
    queue<Task> tasks;
};

void thpool_init(struct ThreadPool* pool, unsigned threads_nm);
void thpool_submit(struct ThreadPool* pool, struct Task* task);
void thpool_wait(struct Task* task);
void thpool_finit(struct ThreadPool* pool);
void* invoke(struct ThreadPool* pool);
#endif
