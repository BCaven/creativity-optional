"""
Config file for celery task manager

Image generation tasks should have high priority
Recieving sound input should have high priority
changing sound settings should have low priority

TODO: fill out this config file
"""
# broker url
# TODO: make this work in docker deployment
broker_url = 'redis://localhost'
# priority routes go here
task_routes = {
    'server_tasks.test_task': 'low-priority'
}