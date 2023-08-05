import os
import sys
import sqlite3
import csv
import shutil
import locale
import random
import string
import signal
import logging

from datetime import datetime
from contextlib import contextmanager
from itertools import groupby, chain, repeat
from concurrent.futures import ProcessPoolExecutor

import psutil
import pandas as pd
from sas7bdat import SAS7BDAT
from graphviz import Digraph


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(module)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

if os.name == 'nt':
    locale.setlocale(locale.LC_ALL, 'English_United States.1252')
else:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


WORKSPACE = ''
_EMPTY = ''
_filename, _ = os.path.splitext(os.path.basename(sys.argv[0]))
_DBNAME = _filename + '.db'
_GRAPH_NAME = _filename + '.gv'
_JOBS = {}


@contextmanager
def _connect(dbfile, cache_size=100000, temp_store=2):
    conn = _Connection(dbfile, cache_size, temp_store)
    try:
        yield conn
    finally:
        # Trying to make closing atomic to handle multiple ctrl-cs
        # Imagine the first ctrl-c have the process enter the 'finally block'
        # and the second ctrl-c interrupts the block in the middle 
        # so that the database is corrupted
        with _delayed_keyboard_interrupts():
            # should I close the cursor?
            conn._cursor.close()
            conn._conn.commit()
            conn._conn.close()


@contextmanager
def _delayed_keyboard_interrupts():
    signal_received = False 
    def handler(sig, frame):
        signal_received = (sig, frame) 
        logger.debug('SIGINT received. Delaying KeyboardInterrupt.')
    old_handler = signal.signal(signal.SIGINT, handler)

    try:
        yield
    finally:
        signal.signal(signal.SIGINT, old_handler)
        if signal_received:
            old_handler(*signal_received)


class _Connection:
    def __init__(self, dbfile, cache_size, temp_store):
        global WORKSPACE
        if not WORKSPACE:
            WORKSPACE = os.getcwd()

        dbfile = os.path.join(WORKSPACE, dbfile)

        self._conn = sqlite3.connect(dbfile)
        self._conn.row_factory = _dict_factory

        self._cursor = self._conn.cursor()
        self._cursor.execute(f'PRAGMA cache_size={cache_size}')
        self._cursor.execute(f'PRAGMA temp_store={temp_store}')
        self._cursor.execute('PRAGMA journal_mode=OFF')

    def fetch(self, tname, where=None, by=None):
        query = f'select * from {tname}'
        if by and by.strip() != '*':
            query += " order by " + by

        rows = self._conn.cursor().execute(query)

        if where:
            rows = (r for r in rows if where(r))

        if by:
            gby = groupby(rows, _build_keyfn(by))
            yield from (list(rs) for _, rs in gby)
        else:
            yield from rows

    def insert(self, rs, name):
        try:
            r0, rs = _peek_first(rs)
        except StopIteration:
            raise ValueError("No row to insert")

        cols = list(r0)
        n = len(cols)

        self._cursor.execute(_create_statement(name, cols))
        istmt = _insert_statement(name, n)
        self._cursor.executemany(istmt, (list(r.values()) for r in rs if isinstance(r, dict)))

    def load(self, filename, name=None, encoding='utf-8', fn=None):
        if isinstance(filename, str):
            fname, ext = os.path.splitext(filename)

            if ext == '.csv':
                seq = _read_csv(filename, encoding)
            elif ext == '.xlsx':
                seq = _read_excel(filename)
            elif ext == '.sas7bdat':
                seq = _read_sas(filename)
            else:
                raise ValueError('Unknown file extension', ext)
            name = name or fname
        else:
            seq = filename

        if fn:
            seq = (fn(r) for r in seq)
        self.insert(seq, name)

    def get_tables(self):
        query = self._cursor.execute("select * from sqlite_master where type='table'")
        return [row['name'] for row in query]

    def drop(self, tables):
        tables = _listify(tables)
        for table in tables:
            self._cursor.execute(f'drop table if exists {table}')

    def join(self, tinfos, name):
        tname0, _, mcols0 = tinfos[0]
        join_clauses = []
        for i, (tname1, _, mcols1) in enumerate(tinfos[1:], 1):
            eqs = []
            for c0, c1 in zip(_listify(mcols0), _listify(mcols1)):
                if c1:
                    eqs.append(f't0.{c0} = t{i}.{c1}')
            join_clauses.append(f"left join {tname1} as t{i} on {' and '.join(eqs)}")
        jcs = ' '.join(join_clauses)

        allcols = []
        for i, (_, cols, _) in enumerate(tinfos):
            for c in _listify(cols):
                if c == '*':
                    allcols += [f't{i}.{c1}' for c1 in self._cols(f'select * from {tinfos[i][0]}')]
                else:
                    allcols.append(f't{i}.{c}')

        # create indices
        ind_tnames = []
        for tname, _, mcols in tinfos:
            mcols1 = [c for c in _listify(mcols) if c]
            ind_tname = tname + _random_string(10)
            self._cursor.execute(f"create index {ind_tname} on {tname}({', '.join(mcols1)})")

        query = f"create table {name} as select {', '.join(allcols)} from {tname0} as t0 {jcs}"
        self._cursor.execute(query)
        # drop indices, not so necessary
        for ind_tname in ind_tnames:
            self._cursor.execute(f"drop index {ind_tname}")

    def _cols(self, query):
        return [c[0] for c in self._cursor.execute(query).description]


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def _execute(c, job):
    def flatten(seq):
        for x in seq:
            if isinstance(x, dict):
                yield x
            else:
                yield from x

    def genfn(c, fn, input, where, by, arg=None):
        if arg:
            yield from flatten(fn(rs, arg) for rs in c.fetch(input, where, by))
        else:
            yield from flatten(fn(rs) for rs in c.fetch(input, where, by))

    cmd = job['cmd']
    if cmd == 'load':
        c.load(job['file'], job['output'], job['encoding'], job['fn'])
    elif cmd == 'map':
        if job['parallel']:
            with ProcessPoolExecutor(max_workers=psutil.cpu_count(logical=False)) as exe:
                cnksize = job['parallel'] if isinstance(job['parallel'], int) else 1
                if job['arg']:
                    seq = exe.map(job['fn'],
                                  c.fetch(job['inputs'][0], job['where'], job['by']),
                                  repeat(job['arg']),
                                  chunksize=cnksize)
                else:
                    seq = exe.map(job['fn'],
                                  c.fetch(job['inputs'][0], job['where'], job['by']),
                                  chunksize=cnksize)
                c.insert(flatten(seq), job['output'])
        else:
            seq = genfn(c, job['fn'], job['inputs'][0], job['where'], job['by'], job['arg'])
            c.insert(seq, job['output'])

    elif cmd == 'join':
        c.join(job['args'], job['output'])
    elif cmd == 'union':
        def gen():
            for input in job['inputs']:
                for r in c.fetch(input):
                    yield r
        c.insert(gen(), job['output'])


def load(file=None, fn=None, encoding='utf-8'):
    return {'cmd': 'load',
            'file': file,
            'fn': fn,
            'encoding': encoding,
            'inputs': []}


def map(fn=None, data=None, where=None, by=None, arg=None, parallel=False):
    return {
        'cmd': 'map',
        'fn': fn,
        'inputs': [data],
        'where': where,
        'by': by,
        'arg': arg,
        'parallel': parallel
    }


def join(*args):
    inputs = [arg[0] for arg in args]
    return {
        'cmd': 'join',
        'inputs': inputs,
        'args': args
    }


def union(inputs):
    return {
        'cmd': 'union',
        'inputs': _listify(inputs)
    }


def register(**kwargs):
    for k, _ in kwargs.items():
        if _JOBS.get(k, False):
            raise ValueError(f"Table duplication: {k}")
    _JOBS.update(kwargs)


def run():
    def append_output(kwargs):
        for k, v in kwargs.items():
            v['output'] = k
        return [v for _, v in kwargs.items()]

    def find_required_tables(jobs):
        tables = set()
        for job in jobs:
            for table in job['inputs']:
                tables.add(table)
            tables.add(job['output'])
        return tables

    # depth first search
    def dfs(data, path, paths=[]):
        datum = path[-1]
        if datum in data:
            for val in data[datum]:
                new_path = path + [val]
                paths = dfs(data, new_path, paths)
        else:
            paths += [path]
        return paths

    def build_graph(jobs):
        graph = {}
        for job in jobs:
            for ip in job['inputs']:
                if graph.get(ip):
                    graph[ip].add(job['output'])
                else:
                    graph[ip] = {job['output']}
        for x in graph:
            graph[x] = list(graph[x])
        return graph

    def render_graph(graph, jobs):
        dot = Digraph()
        for k, v in graph.items():
            dot.node(k, k)
            if k != v:
                for v1 in v:
                    dot.edge(k, v1)
        for job in jobs:
            if job['cmd'] == 'load':
                dot.node(job['output'], job['output'])
        dot.render(_GRAPH_NAME)

    jobs = append_output(_JOBS)
    required_tables = find_required_tables(jobs)
    with _connect(_DBNAME) as c:
        def delete_after(missing_table, paths):
            for path in paths:
                if missing_table in path:
                    for x in path[path.index(missing_table):]:
                        c.drop(x)

        def get_missing_tables():
            existing_tables = c.get_tables()
            return [table for table in required_tables
                    if table not in existing_tables]

        def find_jobs_to_do(jobs):
            missing_tables = get_missing_tables()
            result = []
            for job in jobs:
                for table in (job['inputs'] + [job['output']]):
                    if table in missing_tables:
                        result.append(job)
                        break
            return result

        def is_doable(job):
            missing_tables = get_missing_tables()
            return all(table not in missing_tables for table in job['inputs']) \
                and job['output'] in missing_tables

        graph = build_graph(jobs)
        try:
            render_graph(graph, jobs)
        except Exception:
            pass

        starting_points = [job['output'] for job in jobs if job['cmd'] == 'load']
        paths = []
        for sp in starting_points:
            paths += dfs(graph, [sp], [])

        for mt in get_missing_tables():
            delete_after(mt, paths)

        jobs_to_do = find_jobs_to_do(jobs)
        logger.info(f'To Create: {[j["output"] for j in jobs_to_do]}')
        while jobs_to_do:
            cnt = 0
            for i, job in enumerate(jobs_to_do):
                if is_doable(job):
                    try:
                        _execute(c, job)
                    except Exception as e:
                        logger.error(f"Failed: {job['output']}")
                        logger.error(f"{type(e).__name__}: {e}")
                        try:
                            # TODO: Sometimes "database locked" error is raised
                            # but drops the table anyway. No idea why.
                            # Not OS specific
                            c.drop(job['output'])
                        except Exception:
                            pass

                        logger.info(f"Unfinished: {[job['output'] for job in jobs_to_do]}")
                        return jobs_to_do
                    logger.info(f"{job['cmd']}: {job['output']}")
                    del jobs_to_do[i]
                    cnt += 1
            if cnt == 0:
                for j in jobs_to_do:
                    logger.warning(f'Unfinished: {j["output"]}')
                    for t in j['inputs']:
                        if t not in c.get_tables():
                            logger.warning(f'Table not found: {t}')
                return jobs_to_do


def _random_string(nchars):
    "Generates a random string of lengh 'n' with alphabets and digits. "
    chars = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(chars)
                   for _ in range(nchars))


def _peek_first(seq):
    """
    Note:
        peeked first item is pushed back to the sequence
    Args:
        seq (Iter[type])
    Returns:
        Tuple(type, Iter[type])
    """
    # never use tee, it'll eat up all of your memory
    seq1 = iter(seq)
    first_item = next(seq1)
    return first_item, chain([first_item], seq1)


# performance doesn't matter for this, most of the time
def _listify(x):
    """
    Example:
        >>> listify('a, b, c')
        ['a', 'b', 'c']

        >>> listify(3)
        [3]

        >>> listify([1, 2])
        [1, 2]
    """
    try:
        return [x1.strip() for x1 in x.split(',')]
    except AttributeError:
        try:
            return list(iter(x))
        except TypeError:
            return [x]


def _build_keyfn(key):
    " if key is a string return a key function "
    # if the key is already a function, just return it
    if hasattr(key, '__call__'):
        return key
    colnames = _listify(key)
    # special case
    if colnames == ['*']:
        return lambda r: 1

    if len(colnames) == 1:
        col = colnames[0]
        return lambda r: r[col]
    else:
        return lambda r: [r[colname] for colname in colnames]


# primary keys are too much for non-experts
def _create_statement(name, colnames):
    """create table if not exists foo (...)

    Note:
        Every type is numeric.
        Table name and column names are all lowercased
    """
    # every col is numeric, this may not be so elegant but simple to handle.
    # If you want to change this, Think again
    schema = ', '.join([col + ' ' + 'numeric' for col in colnames])
    return "create table if not exists %s (%s)" % (name, schema)


def _insert_statement(name, ncol):
    "insert into foo values (?, ?, ?, ...)"
    qmarks = ', '.join(['?'] * ncol)
    return "insert into %s values (%s)" % (name, qmarks)


def _read_csv(filename, encoding='utf-8'):
    def is_empty_line(line):
        return [x for x in line if x.strip() != ""] == []

    with open(os.path.join(WORKSPACE, filename), encoding=encoding) as f:
        first_line = f.readline()[:-1]
        columns = _listify(first_line)
        ncol = len(columns)

        # NULL byte error handling
        reader = csv.reader(x.replace('\0', _EMPTY) for x in f)
        for line_no, line in enumerate(reader, 2):
            if len(line) != ncol:
                if is_empty_line(line):
                    continue
                raise ValueError(f"Invalid Line at {line_no}: {line}")
            yield {k: v for k, v in zip(columns, line)}


def _read_sas(filename):
    filename = os.path.join(WORKSPACE, filename)
    with SAS7BDAT(filename) as f:
        reader = f.readlines()
        # lower case
        header = next(reader)
        for line in reader:
            yield {k: v for k, v in zip(header, line)}


# this could be more complex but should it be?
def _read_excel(filename):
    def read_df(df):
        cols = df.columns
        for _, r in df.iterrows():
            yield {k: v for k, v in zip(cols, ((str(r[c]) for c in cols)))}

    filename = os.path.join(WORKSPACE, filename)
    # it's OK. Excel files are small
    df = pd.read_excel(filename)
    yield from read_df(df)

