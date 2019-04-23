from threading import Thread


class CommandProcessor(Thread):
    def __init__(self, cmd_coll):
        self._cmd_coll = cmd_coll
        self._is_running = True

    def run(self):
        """
        TODO: need to work out best way to capture command and pass to existing
        TODO: sensor object (events maybe?) not sure yet will work out later
        :return:
        """
        while self._is_running:
            pass

    def stop(self):
        self._is_running = False
