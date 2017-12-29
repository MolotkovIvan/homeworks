#include "threadpool.h"
#include <iostream>
#include <pthread.h>
#include <vector>
#include <queue>

void* invoke(void*);
void func(void*);

void thpool_init(ThreadPool* const pool, unsigned threads_nm) {
	pthread_mutex_init(&pool->mutex, NULL);
	pthread_cond_init(&pool->new_task, NULL);
	pool->end = false;
	pool->active_threads = threads_nm;
	for (unsigned i = 0; i < threads_nm; i++) {
		pthread_t id;
		pool->threads.push_back(id); 
		pthread_create(&pool->threads[i], NULL, invoke, (void*)pool); 
	}
}

void thpool_submit(ThreadPool* const pool, struct Task* const task) {
	pthread_mutex_init(&task->m, NULL);
	pthread_cond_init(&task->iscompleted_cond, NULL);
	
	pthread_mutex_lock(&pool->mutex);
	pool->tasks.push(task);
	pthread_mutex_unlock(&pool->mutex); 
	
	pthread_cond_signal(&pool->new_task);
}

void thpool_wait(struct Task* const task) {
//	std::cout << "1 wait\n";
	pthread_mutex_lock(&task->m);	
	while (!task->iscompleted_bool) { 
//		std::cout << "2 wait\n";
		pthread_cond_wait(&task->iscompleted_cond, &task->m);
	}
	pthread_mutex_unlock(&task->m);	

	pthread_mutex_destroy(&task->m);
	pthread_cond_destroy(&task->iscompleted_cond);
//	std::cout << "3 wait\n";
}

void thpool_finit(ThreadPool* const pool) {
//	std::cout << "1 finit\n";
	pthread_mutex_lock(&pool->mutex); 
	pool->end = true;
	pthread_mutex_unlock(&pool->mutex);
//	std::cout << "2 finit\n";
	pthread_cond_broadcast(&pool->new_task);
	while (pool->active_threads == 0) {
//		std::cout << "3 finit\n";
		pthread_mutex_lock(&pool->mutex); 
		pthread_cond_wait(&pool->finit, &pool->mutex);
		pthread_mutex_unlock(&pool->mutex); 
//		std::cout << "4 finit\n";
	}
	
	pthread_mutex_destroy(&pool->mutex);
//	std::cout << "5 finit\n";
}

void* invoke(void* const pool) {
	ThreadPool* p = (ThreadPool*)pool;
	while(true) {
		pthread_mutex_lock(&p->mutex);
		while (p->tasks.empty() || p->end) {
			pthread_cond_wait(&p->new_task, &p->mutex);
			if (p->end) {
				--p->active_threads;
				pthread_cond_signal(&p->finit);
				return NULL;
			}

		};

		if (!p->tasks.empty() && !p->end) {
			Task *t = p->tasks.front();
			pthread_mutex_lock(&t->m);
			p->tasks.pop();
			pthread_mutex_unlock(&p->mutex);
			t->f(t->arg);
			t->iscompleted_bool = true;
			pthread_cond_signal(&t->iscompleted_cond);
			pthread_mutex_unlock(&t->m);
		}
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
	t1->iscompleted_bool = false;
	thpool_submit(&pool, t1);
	thpool_wait(t1);
	
	Task *t2 = new Task;
	t2->f = func;
	int n2 = 6;
	t2->arg = &n2;
	t2->iscompleted_bool = false;
	thpool_submit(&pool, t2);
	thpool_wait(t2);
	
	thpool_finit(&pool);
	return 0;
}
