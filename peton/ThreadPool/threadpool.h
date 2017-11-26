#ifndef THREAD_POOL
#define THREAD_POOL

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
    vector<pthread_t>;
    queue<Task> tasks;
};

void thpool_init(struct ThreadPool* pool, unsigned threads_nm);
void thpool_submit(struct ThreadPool* pool, struct Task* task);
void thpool_wait(struct Task* task);
void thpool_finit(struct ThreadPool* pool);
#endif
