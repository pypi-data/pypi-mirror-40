from collections import OrderedDict
import traceback
import argparse
import asyncio
import json
import re
import sys

from .entries import entry_wrap, Entry
from .extractor import Extractor
from . import executors
from . import utils

arg_help = utils.arg_help

class BaseStreamer():
    def __init__(self, **options):
        self.options = options
        self.initialize()

    def __aiter__(self):
        return self.stream()

    async def handle(self, value):
        raise NotImplemented('Implement either the stream or handle method of a BaseStreamer subclass')

    async def stream(self, source):
        async for entry in source:
            result = await self.handle(entry.value)
            entry.value = result
            yield entry

    def initialize(self):
        pass

@arg_help('Translate each value by assigning it to the result of a python expression', example='"value.upper()"')
class PyExecTransform(BaseStreamer):
    @classmethod
    def args(cls, parser):
        parser.add_argument(
            'code',
            nargs='?',
            help='Python code to evaluate',
        )
        parser.add_argument(
            '--statement',
            action='store_true',
            help='Indicates that the python code is not an expression but a statement',
            default=False,
        )

    def __init__(self, code=None, statement=False, show_exceptions=False):
        self.show_exceptions = show_exceptions
        self.expression = not statement
        self.runner = exec if statement else eval
        try:
            self.code = compile(code, '<string::transform>', self.runner.__name__)
        except Exception as e:
            traceback.print_exc()
            sys.exit(1)

    async def stream(self, source):
        async for entry in source:
            scope = {'value': entry.value, 'input': entry.original_value, 'i': entry.index, 'index': entry.index}
            try:
                if self.expression:
                    entry.value = self.runner(self.code, globals(), scope)
                else:
                    self.runner(self.code, globals(), scope)
                    if 'result' in scope:
                        entry.value = scope.get('result', None) 
                    else:
                        entry.value = scope.get('result')
            except Exception as e:
                print(e)
                if self.show_exceptions:
                    entry.exception(e)
                    traceback.print_exc()
                else:
                    continue
            yield entry

@arg_help('Filter out values that dont have a truthy result to a particular python expression', example='"\'foobar\' in value"')
class PyExecFilter(BaseStreamer):
    @classmethod
    def args(cls, parser):
        parser.add_argument(
            'code',
            nargs='?',
            help='Python code to evaluate',
        )

    def __init__(self, code=None, show_exceptions=False):
        self.show_exceptions = show_exceptions
        try:
            self.code = compile(code, '<string::filter>', 'eval')
        except Exception as e:
            traceback.print_exc()
            sys.exit(1)

    async def stream(self, source):
        async for entry in source:
            scope = {'value': entry.value, 'input': entry.original_value, 'i': entry.index, 'index': entry.index}
            try:
                keep = eval(self.code, globals(), scope)
            except Exception as e:
                keep = False
                if self.show_exceptions:
                    traceback.print_exc()
            if keep:
                yield entry

@arg_help('Filter out values that dont have a truthy result to a particular python expression', example='--selector exit_code')
class ExtractionStreamer(BaseStreamer):
    @classmethod
    def args(cls, parser):
        parser.add_argument(
            '--selector',
            help='dot-separated path to desired attribute',
        )

    def initialize(self):
        self.extractor = Extractor(self.options['selector'])

    async def handle(self, value):
        return self.extractor.extract(value)

class AsyncExecutor():
    """
        :: Worker-oriented event loop processor

        Workers are no longer a necessary concept in an asynchronous world. However, the concept can still be very
        helpful for controlling resource usage on the host machine or remote systems used by the job. For this reason
        I'm re-implementing a worker-style executor pool which could be used with jobs that are threaded or async.
    """
    DEFAULT_WORKERS = 20

    @classmethod
    def args(cls, parser):
        parser.add_argument(
            '-w', '--workers',
            type=int,
            help='Number of concurrent workers for execution modules',
            default=cls.DEFAULT_WORKERS,
        )
        parser.add_argument(
            '-p', '--show-progress',
            action='store_true',
            help='Output progress bar',
            default=False,
        )

    def __init__(self, executor=None, show_progress=False, workers=DEFAULT_WORKERS, loop=None):
        self.executor = executor
        self.output_queue = asyncio.Queue()
        self.show_progress = show_progress
        self.worker_count = workers or self.DEFAULT_WORKERS

        # State data
        self.entry_count = 0
        self.complete_count = 0
        self.active_count = 0
        self.all_enqueued = False
        self.loop = loop or asyncio.get_event_loop()

    def _show_progress(self, newline=False):
         if not self.show_progress:
             return

         sys.stdout.write('\r {done} out of {total} tasks complete - {percent_done}% (running={running}; pending={pending})'.format(
             done=self.complete_count,
             total=self.entry_count,
             percent_done=int(self.complete_count / self.entry_count * 100),
             running=self.active_count,
             pending='??'
         ))
         if newline:
             # Finish with a newline
             print('')

    def _save_result(self, entry):
        self.complete_count += 1
        self.output_queue.put_nowait(entry)

    async def stream(self, source):
        self.source = source
        # Start workers
        workers = []
        for i in range(self.worker_count):
            worker = self.loop.create_task(self._worker())
            workers.append(worker)

        all_workers = asyncio.gather(*workers)
        asyncio.ensure_future(all_workers)
        while True:
            if all_workers.done() and self.output_queue.qsize() == 0:
                break
            try:
                entry = await asyncio.wait_for(self.output_queue.get(), timeout=.1)
            except asyncio.TimeoutError:
                continue
            self.output_queue.task_done()
            yield entry
            self._show_progress()
        self._show_progress(newline=True)

    async def _worker(self):
        while True:
            try:
                entry = await self.source.__anext__()
            except StopAsyncIteration:
                return
            self.entry_count += 1
            self.active_count += 1
            try:
                if asyncio.iscoroutinefunction(self.executor):
                    entry.value = await self.executor(entry.value)
                else:
                    def executor_wrapper():
                        return self.executor(entry.value)
                    entry.value = await self.loop.run_in_executor(None, executor_wrapper)
            except Exception as e:
                entry.error(e)
            self._save_result(entry)
            self.active_count -= 1

@arg_help('No operation. Just for testing.')
async def noop(source):
    for entry in source:
        yield entry

@arg_help('Filter out values that are not truthy')
async def truthy(source):
    async for entry in source:
        if entry.value:
            yield entry

@arg_help('Take json strings and parse them into objects so other streamers can inspect attributes')
async def json_parser(source):
    async for entry in source:
        try:
            entry.value = json.loads(entry.value)
        except Exception as e:
            entry.error(e)
        yield entry

@arg_help('Take any values that are an array and treat each value of an array as a separate input ')
async def split_lists(source):
    """ Splits arrays into multiple entries """
    async for entry in source:
        # No-op on non-list values
        if not isinstance(entry.value, list):
            yield entry


        for wrapped_value in entry_wrap(entry.value):
            yield wrapped_value

@arg_help('Show a report of how many input values ended up with a particular result value')
class ValueBreakdown(BaseStreamer):
    """ Gives summary stats either instead of the values or as an extra event at the end"""

    @classmethod
    def args(cls, parser):
        parser.add_argument(
            '--inputs',
            action='store_true',
            default=False,
            help='Report the array of input values that had a particular result value',
        )
        parser.add_argument(
            '--append-summary',
            action='store_true',
            default=False,
            help='Instead of replacing values with the result breakdown, append a single entry at the end with the data',
        )

    def __init__(self, inputs=False, append_summary=False):
        self.inputs = inputs
        self.append = append_summary

    async def stream(self, source):
        stats = OrderedDict()
        async for entry in source:
            if entry.value in stats:
                value_stats = stats[entry.value]
                value_stats['count'] += 1
                if self.inputs:
                    value_stats['inputs'].append(entry.original_value)
            else:
                metadata = {
                    'value': entry.value,
                    'count': 1,
                }
                if self.inputs:
                    metadata['inputs'] = [entry.original_value]
                stats[entry.value] = metadata

            if self.append:
                yield entry

        if self.append:
            yield Entry(list(stats.values()))
        else:
            for wrapped_value in entry_wrap(stats.values()):
                yield wrapped_value

@arg_help('Force each value to a string and prefix each with the original input value')
async def input_headers(source):
    async for entry in source:
        value = utils.force_string(entry.value)
        header = utils.force_string(entry.original_value)
        entry.value = '{}: {}'.format(header, value)
        yield entry

@arg_help('Filter out any entries that have produced an error')
async def filter_out_errors(source):
    async for entry in source:
        if not entry.errors:
            yield entry

@arg_help('Use the latest error on the entry as the value')
async def error_values(source):
    async for entry in source:
        if not entry.errors:
            yield entry
            continue

        error = entry.errors[-1]
        if isinstance(error, Exception) and getattr(error, '__traceback__', None):
            error = '\n'.join(traceback.format_tb(error.__traceback__))
        entry.value = error
        yield entry

@arg_help('Hold entries in memory until a certain number is reached (give no args to buffer all)', example='--buffer 20')
class StreamingBuffer(BaseStreamer):
    @classmethod
    def args(cls, parser):
        parser.add_argument(
            '--buffer',
            default='all',
            help='Number of entries to buffer (blank for all)',
        )

    def initialize(self):
        try:
            self.buffer_size = int(self.options['buffer'])
        except Exception as e:
            self.buffer_size = None

    async def stream(self, source):
        buffer_list = []
        async for entry in source:
            buffer_list.append(entry)
            if self.buffer_size is None:
                # We want to accrue all
                continue
            elif buffer_list >= self.buffer_size:
                # Empty the buffer
                for entry in buffer_list:
                    yield entry
                buffer_list = []

        # Drain any remaining
        for entry in buffer_list:
            yield entry


STREAMERS = {
    'extract': ExtractionStreamer,
    'py': PyExecTransform,
    'pyfilter': PyExecFilter,
    'truthy': truthy,
    'noop': noop,
    'split': split_lists,
    'breakdown': ValueBreakdown,
    'headers': input_headers,
    'filter_out_errors': filter_out_errors,
    'errors': error_values,
    'buffer': StreamingBuffer,
}
# Add executors that need to be wrapped with AsyncExecutor
STREAMERS.update(executors.EXECUTORS)
