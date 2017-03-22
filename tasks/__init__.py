"""
@file: Test

"""
import abc
import subprocess


def get_task_runner(task_definition):
    plugin_name = task_definition['pluginKey']
    task_runner_subclasses = TaskRunner.__subclasses__()
    for sub_class in task_runner_subclasses:
        if sub_class.plugin_name == plugin_name:
            return sub_class(task_definition)
    raise TypeError("No task runner for pluginKey '{}' found".format(plugin_name))


class TaskRunner(object):
    __metaclass = abc.ABCMeta

    plugin_name = None
    task_name = "Base Task"

    def __init__(self, task_data):
        self.oid = task_data['oid']
        self.configuration = task_data['configuration']
        self.description = task_data['description']
        return


    def __call__(self):
        print "\t\t{} '{}' executing...".format(self.__class__.task_name, self.description)
        return self.run()


    @abc.abstractmethod
    def run(self):
        """
        Abstract run method
        """
        return

class VersionControlCheckoutRunner(TaskRunner):
    """
    Plugin Runner for Version Control Checkout
    """
    plugin_name = "com.atlassian.bamboo.plugins.vcs:task.vcs.checkout"
    task_name = "Version Control Checkout Task"

    def _check_git(self):
        try:
            subprocess.check_call(["git", "status"])
        except subprocess.CalledProcessError:
            return False
        return True


    def run(self):
        print "\t\t\tSkipping Version control"
        return

class ScriptRunner(TaskRunner):
    """
    Plugin Runner for Script execution
    """
    plugin_name = "com.atlassian.bamboo.plugins.scripttask:task.builder.script"
    task_name = "Script Runner Task"

    def run(self):
        print "\t\t\tExecuting script"
        return
