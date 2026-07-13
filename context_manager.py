class ContextManager:

    def __init__(self):
        self.active_topic = None
        self.active_task = None

    def set_topic(self, topic):
        self.active_topic = topic

    def get_topic(self):
        return self.active_topic

    def clear_topic(self):
        self.active_topic = None

    def set_task(self, task):
        self.active_task = task

    def get_task(self):
        return self.active_task

    def clear_task(self):
        self.active_task = None

