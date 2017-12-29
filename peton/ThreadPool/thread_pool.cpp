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
	pthread_cond_init(&pool->task_is_done, NULL);
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
	if (!pool->end) {
		pool->tasks.push(task);
	}
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
	while (pool->tasks.size() != 0) {
		pthread_mutex_lock(&pool->mutex); 
		pthread_cond_wait(&pool->task_is_done, &pool->mutex);
		pthread_mutex_unlock(&pool->mutex); 
	}
	pthread_cond_broadcast(&pool->new_task);
	for (int i = 0; i < pool->threads.size(); i++) {
//		std::cout << "3 finit\n";
		pthread_join(pool->threads[i], NULL);
//		std::cout << "4 finit\n";
	}	
	
	pthread_mutex_destroy(&pool->mutex);
	pthread_cond_destroy(&pool->new_task);
	pthread_cond_destroy(&pool->task_is_done);
//	std::cout << "5 finit\n";
}

void* invoke(void* const pool) {
	ThreadPool* p = (ThreadPool*)pool;
	while(true) {
		pthread_mutex_lock(&p->mutex);
		while (p->tasks.empty() || p->end) {
			if (p->end) {
				pthread_cond_signal(&p->task_is_done);
				pthread_mutex_unlock(&p->mutex);
				return NULL;
			}
			pthread_cond_wait(&p->new_task, &p->mutex);
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

struct input {
	int l;
	int m;
	int r;
	int* array;
};

void sort (void* arg) {
	input* data = (input*)arg;
	int tmp;
	for (int i = data->l; i < data->r; i++) {
		for (int j = data->l; j < data->r + data->l - i - 1; j++) {		
			if (data->array[j] > data->array[j+1]) {
				tmp = data->array[j];
				data->array[j] = data->array[j+1];
				data->array[j+1] = tmp;
			}
		}
	}
}

void merge (void* arg) {
	input* data = (input*)arg;
	int i = data->l;
	int j = data->m;
	int* buf = new int[data->r - data->l];
	int k = 0;
	while (i < data->m && j < data->r) {
		if (data->array[i] < data->array[j]) {
			buf[k] = data->array[i];
			i++;
		} else {
			buf[k] = data->array[j];
			j++;
		}
		k++;
	}
	while (i < data->m) {
		buf[k] = data->array[i];
		i++;
		k++;
	}
	while (j < data->r) {
		buf[k] = data->array[j];
		j++;
		k++;
	}
	for (int q = data->l; q < data->r; q++) {
		data->array[q] = buf[q-data->l];
	}

	delete [] buf;
}

int main () {
	ThreadPool pool;
	thpool_init(&pool, 2);
	

	int* a = new int[4];
	a[0] = 4;
	a[1] = 7;
	a[2] = 8;
	a[3] = 1;

	Task *t1 = new Task;
	t1->f = sort;
	t1->iscompleted_bool = false;
	input *arg1 = new input;
	arg1->l = 0;
	arg1->r = 2;
	arg1->array = a;
	t1->arg = arg1;
	
	Task *t2 = new Task;
	t2->f = sort;
	t2->iscompleted_bool = false;
	input *arg2 = new input;
	arg2->l = 2;
	arg2->r = 4;
	arg2->array = a;
	t2->arg = arg2;
	
	Task *t3 = new Task;
	t3->f = merge;
	t3->iscompleted_bool = false;
	input *arg3 = new input;
	arg3->l = 0;
	arg3->m = 2;
	arg3->r = 4;
	arg3->array = a;
	t3->arg = arg3;

	thpool_submit(&pool, t1);
	thpool_wait(t1);

	thpool_submit(&pool, t2);
	thpool_wait(t2);

	thpool_submit(&pool, t3);
	thpool_wait(t3);

	thpool_finit(&pool);
	for (int i = 0; i < 4; i++) {
		std::cout << a[i] << " ";
	}
	std::cout << "\n";
	return 0;
}