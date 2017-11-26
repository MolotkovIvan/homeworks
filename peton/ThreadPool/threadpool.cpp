#include <pthread.h>
#include <vector>
#include <queue>

bool end = false;
pthread_mutex_t m_end;

void thpool_init(struct ThreadPool* pool, unsigned threads_nm) {
	pthread_cond_init(&pool->cond);
	pthread_mutex_init(&pool->mutex);
	pthread_mutex_init(&m_end);
	for (unsigned i = 0; i < threads_nm; i++) {
		pthread_t id;
		pool->threads.push_back(id); 
		pthread_create(&pool->threads[i], NULL, invoke, pool); 
	}
}

void thpool_submit(struct ThreadPool* pool, struct Task* task) {
	pthread_mutex_init(&task->m);
	pool->tasks.push(*task);
	pthread_cond_signal(&pool->cond);
}

void thpool_wait(struct Task* task) {
	while (!task->is_completed) {}; //wait until task is taken by some thread
	pthread_mutex_lock(task->m); //after that we wait until task is completed
}

void thpool_finit(struct ThreadPool* pool) {
	pthread_mutex_lock(&m_end);
	end = true; //tell threads to stop working
	pthread_mutex_unlock(&m_end);
}

void* invoke(struct ThreadPool* pool) {
	while(true) { //now thread is able to perform more than one task
		pthread_mutex_lock(&pool->mutex);
		while (pool->tasks.empty()) {
			pthread_mutex_lock(&m_end);
			if (end) {	//while waiting for a new task thread simultaneously checks whether he should stop working or not 
				return NULL;
			}
			pthread_mutex_unlock(&m_end);
			pthread_cond_wait(&pool->cond, &pool->mutex);
		}
		if (!pool->tasks.empty()) {
			Task t = pool->tasks.pop();
			pthread_mutex_lock(&t->m);
			t.is_completed = true;
			void f = t.f;
			f(t.arg);
			pthread_mutex_unlock(&t->m);
		}
		pthread_mutex_unlock(&pool->mutex);
	}
}