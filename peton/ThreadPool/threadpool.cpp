#include "threadpool.h"
#include <iostream>
#include <pthread.h>
#include <vector>
#include <queue>

void* invoke(void*);
void func(void*);

void thpool_init(ThreadPool* pool, unsigned threads_nm) { //this part seems pretty obvious
	pthread_mutex_init(&pool->mutex, NULL);
	for (unsigned i = 0; i < threads_nm; i++) {
		pthread_t id;
		pool->threads.push_back(id); 
		pthread_create(&pool->threads[i], NULL, invoke, (void*)pool); 
	}
}

void thpool_submit(ThreadPool* pool, struct Task* task) { //send the signal to one of threads, wake it up
	pthread_mutex_init(&task->m, NULL);
	pthread_cond_init(&task->iscompleted_cond, NULL);
	pool->tasks.push(*task);
	pthread_cond_signal(&pool->new_task);
}

void thpool_wait(struct Task* task) {
	pthread_mutex_lock(&task->m);	
	while (!task->iscompleted_bool) { 
		pthread_cond_wait(&task->iscompleted_cond, &task->m); //wake up when task's function is run
	}
	pthread_mutex_unlock(&task->m);	

	pthread_mutex_destroy(&task->m); //clear memory
	pthread_cond_destroy(&task->iscompleted_cond);
}

void thpool_finit(ThreadPool* pool) { //probably the most questionable part. i'm not sure we need to wait for every thread to stop working, but i didn't come up with something better
	pthread_mutex_lock(&pool->mutex); 
	pool->end = true; //set the condition for threads so they don't take anymore tasks
	pthread_mutex_unlock(&pool->mutex);
	for (int i = 0; i < pool->threads.size(); i++) {
		pthread_join(pool->threads[i], NULL);
	}
	pthread_mutex_destroy(&pool->mutex);
}

void* invoke(void* pool) {
	ThreadPool* p = (ThreadPool*)pool;
	while(true) {
		pthread_mutex_lock(&p->mutex);
		while (p->tasks.empty()) {
			pthread_cond_wait(&p->new_task, &p->mutex); //wake up when new task appears
		};

		if (!p->tasks.empty() && !p->end) {
			Task t = p->tasks.front();
			pthread_mutex_lock(&t.m);
			p->tasks.pop();
			t.f(t.arg);
			t.iscompleted_bool = true;
			pthread_cond_signal(&t.iscompleted_cond);
			pthread_mutex_unlock(&t.m);
			pthread_mutex_unlock(&p->mutex);
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
