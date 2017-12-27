#include "threadpool.h"
#include <iostream>
#include <pthread.h>
#include <vector>
#include <queue>

void* invoke(void*);
void func(void*);

void thpool_init(ThreadPool* pool, unsigned threads_nm) {
	pthread_mutex_init(&pool->mutex, NULL);
	pthread_mutex_init(&pool->m_end, NULL);
	pthread_cond_init(&pool->cond, NULL);
	pool->active_threads = threads_nm;
	for (unsigned i = 0; i < threads_nm; i++) {
		pthread_t id;
		pool->threads.push_back(id); 
		pthread_create(&pool->threads[i], NULL, invoke, (void*)pool); 
	}
	std::cout << "0\n";
}

void thpool_submit(ThreadPool* pool, struct Task* task) {
	pthread_mutex_init(&task->m, NULL);
	pool->tasks.push(*task);
	pthread_cond_signal(&pool->cond);

}

void thpool_wait(struct Task* task) {
	pthread_mutex_lock(&task->m);
	pthread_cond_wait(&task->is_completed, &task->m);
	pthread_mutex_unlock(&task->m);

}

void thpool_finit(ThreadPool* pool) {
	pthread_mutex_lock(&pool->m_end);

	pool->end = true;
	while (pool->active_threads != 0) {
		std::cout << pool->active_threads << "active_threads\n";
	}
	pthread_mutex_unlock(&pool->m_end);
	pthread_mutex_destroy(&pool->m_end);
	pthread_mutex_destroy(&pool->mutex);
	pthread_cond_destroy(&pool->cond);

}

void* invoke(void* pool) {
	while(true) {
		std::cout << "1\n";
		ThreadPool* p = (ThreadPool*)pool;
		pthread_mutex_lock(&p->mutex);
		std::cout << "2\n";
		while (p->tasks.empty()) {
			std::cout << "6\n";
			pthread_mutex_lock(&p->m_end);
			std::cout << "7\n";
			if (p->end) { 
				p->active_threads -= 1;
				return NULL;
			}
			std::cout << "8\n";
			pthread_mutex_unlock(&p->m_end);
			std::cout << "9\n";
			pthread_cond_wait(&p->cond, &p->mutex);
		}
		std::cout << p->tasks.size() <<" 3\n";
		if (!p->tasks.empty()) {
			pthread_mutex_lock(&p->tasks.front().m);
			Task t = p->tasks.front();
			p->tasks.pop();
			void (*f)(void*);
			f = t.f;
			f(t.arg);
			pthread_mutex_unlock(&t.m);
			pthread_cond_broadcast(&t.is_completed);
			pthread_mutex_destroy(&t.m);
			pthread_cond_destroy(&t.is_completed);
		}
		std::cout << "4\n";
		
		pthread_mutex_unlock(&p->mutex);
		std::cout << "5\n";
	}
}

void func(void* arg) {
	int* n = (int*)arg;
	std::cout << *n << "\n";
}

int main () {
	ThreadPool pool;
	thpool_init(&pool, 2);
	Task *t1 = new Task;
	t1->f = func;
	int n1 = 22;
	t1->arg = &n1;
	thpool_submit(&pool, t1);
	Task *t2 = new Task;
	t2->f = func;
	int n2 = 6;
	t2->arg = &n2;
	
	thpool_finit(&pool);
	std::cout << "end\n";
	return 0;
}
