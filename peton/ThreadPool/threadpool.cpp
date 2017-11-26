#include <pthread.h>
#include <vector>
#include <queue>

void thpool_init(struct ThreadPool* pool, unsigned threads_nm) {
	pthread_cond_init(&pool->cond);
	pthread_mutex_init(&pool->mutex);
	pthread_mutex_init(&m_end);
	pool->active_threads = threads_nm;
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
	pthread_mutex_lock(&task->m);
	while (!task->is_completed) {
		pthread_cond_wait(&task->is_completed, &task->m);
	}
	pthread_mutex_unlock(&task->m);
}

void thpool_finit(struct ThreadPool* pool) {
	pthread_mutex_lock(&m_end);

	pool->end = true;
	while (pool->active_threads != 0) {};
	pthread_mutex_unlock(&m_end);
	pthread_mutex_destroy(&pool->m_end);
	pthread_mutex_destroy(&pool->mutex);
	pthread_cond_destroy(&pool->cond);
}

void* invoke(struct ThreadPool* pool) {
	while(true) {
		pthread_mutex_lock(&pool->mutex);
		while (pool->tasks.empty()) {
			pthread_mutex_lock(&m_end);
			if (end) { 
				pool->active_threads -= 1;
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
			pthread_cond_broadcast(&t->iscompleted);
			pthread_mutex_destroy(&t->m);
			pthread_cond_destroy(&t->iscompleted);
		}
		
		pthread_mutex_unlock(&pool->mutex);
	}
}