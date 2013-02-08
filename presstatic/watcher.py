# -*- coding: utf-8 -*-

import logging

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class BaseWatcher(object):

    def __init__(self, path, recursive=True):
        self.path = path
        self.recursive = recursive
        self.observer = Observer()

    def event_handler(self):
        raise NotImplementedError()

    def start(self):
        handler = self.event_handler()
        self.observer.schedule(handler, self.path, self.recursive)
        self.observer.start()

    def stop(self):
        self.observer.stop()


class EventHandler(PatternMatchingEventHandler):

    def __init__(self, builder):
        self.builder = builder
        ignore = '{0}*'.format(builder.output_path)
        super(EventHandler, self).__init__(ignore_patterns=[ignore])

    # XXX: we should not build everything on every event. Works for now
    def on_any_event(self, event):
        super(EventHandler, self).on_any_event(event)
        self.builder.build()

    def on_moved(self, event):
        super(EventHandler, self).on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Moved %s: from %s to %s", what, event.src_path,
                     event.dest_path)

    def on_created(self, event):
        super(EventHandler, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        super(EventHandler, self).on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event):
        super(EventHandler, self).on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Modified %s: %s", what, event.src_path)


class Watcher(BaseWatcher):

    def __init__(self, builder, **kwargs):
        super(Watcher, self).__init__(builder.path, **kwargs)
        self.builder = builder

    def event_handler(self):
        return EventHandler(self.builder)
