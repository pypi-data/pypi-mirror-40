from __future__ import print_function
import json as JSON
import pytz
from copy import copy
import re, sys, time, base64, random
import requests

import numpy as np
import pandas as pd

from pandas.io.json import json_normalize
from datetime import timedelta
from functools import partial
from multiprocessing.pool import ThreadPool
from threading import Lock
from shapely.geometry import Point

from sentenai.exceptions import *
from sentenai.exceptions import handle
from sentenai.utils import *
from sentenai.historiQL import EventPath, Stream, StreamPath, Proj

BaseStream = Stream


if PY3:
    string_types = str
else:
    string_types = basestring

if not PY3:
    import virtualtime

try:
    from urllib.parse import quote
except:
    from urllib import quote



class Event(object):
    def __init__(self, client, stream, id=None, ts=None, data=None, event=None, duration=None, saved=False):
        self.stream = stream
        self.id = id
        self.ts = ts if isinstance(ts, datetime) or ts is None else cts(ts)
        self.data = data or event or {}
        self.duration = duration
        self._saved = saved

    @property
    def exists(self):
        return bool(self._saved)


    def __repr__(self):
        return "Event(stream={}, id={}, ts={}, exists={})".format(self.stream.name, self.id, self.ts, self.exists)

    def _repr_html_(self):
        return '<pre>Event(\n  stream = "{}",\n  id = "{}",\n  ts = {},\n  exists = {},\n  data = {})</pre>'.format(self.stream.name, self.id, repr(self.ts), self.exists, JSON.dumps(self.data, indent=4, default=dts))


    def json(self, include_id=False, df=False):
        if df:
            d = copy(self.data)
            d['ts'] = pd.to_datetime(dts(self.ts))
            return d
        elif include_id:
            return {'ts': self.ts, 'event': self.data, 'id': self.id}
        else:
            return {'ts': self.ts, 'event': self.data}

    def create(self):
        loc = self.stream.put(self.data, self.id, self.ts)
        self.id = loc
        self._saved = True
        return self

    def read(self):
        x = self.stream.read(self.id)
        self.ts = x.ts
        self.data = x.data
        self._saved = True
        return self

    def update(self):
        if not self.id:
            raise Exception("Not found")
        loc = self.stream.put(self.data, self.id, self.ts, self.duration)
        self.id = loc
        self._saved = True
        return self

    def delete(self):
        self.stream.delete(self.id)
        self._saved = False


class Values(object):
    def __init__(self, stream, at, data):
        self.at = at
        self._data = data

    def __getitem__(self, i):
        if isinstance(i, StreamPath):
            nd = []
            for d in self._data:
                if d['path']._attrlist == i._attrlist:
                    return d['value']
            else:
                raise IndexError
        else:
            return self._data[i]


    def _repr_html_(self):
        df = pd.DataFrame(self._data)
        df['path'] = df['path'].apply(lambda x: ".".join(x._attrlist))
        df = df[['path', 'value', 'timestamp']]
        return df.sort_values(by='path').rename(
                index=str,
                columns={
                    'path': 'Event Path',
                    'value': 'Value'.format(self.at),
                    'timestamp': 'Updated At'
                    }
            )._repr_html_()

    def items(self):
        return [(d['path'], d['value']) for d in self._data]



class Fields(object):
    def __init__(self, fields, view="field"):
        self._view = view
        self._fields = [f for f in fields if f['path']]

    def __getitem__(self, path):
        xs = []
        for field in self._fields:
            if field._attrlist[:len(path._attrlist)] == path._attrlist:
                xs.append(field)
        return Fields(xs)

    def __repr__(self):
        return repr(self._fields)

    def __iter__(self):
        return iter(self._fields)

    def _repr_html_(self):
        df = pd.DataFrame(sorted(self._fields, key=lambda x: (x['start'], ".".join(x['path']))))
        df['path'] = df['path'].apply(lambda x: ".".join(x))
        df['start'] = df['start'].apply(cts)
        df = df[['path', 'start']]
        return df.rename(
                index=str,
                columns={
                    'path': self._view.capitalize(),
                    'start': 'Added At'
                    }
            )._repr_html_()


class StreamMetadata(object):
    def __init__(self, stream):
        self._stream = stream
        self._meta = self.read()


    def read(self):
        resp = self._stream._client.session.get("/".join([self._stream._client.host, "streams", self._stream._name, "meta"]), params={})
        if resp.status_code == 404:
            return None
        elif resp.status_code == 200:
            data = resp.json()
            parsed = {}
            for k,v in data.items():
                if type(v) in [float, int, bool]:
                    parsed[k] = v
                elif type(v) == dict and 'lat' in v and 'lon' in v:
                    parsed[k] = Point(v['lon'], v['lat'])
                else:
                    for fmt in ["%Y-%m-%dT%H:%M:%S.%fZ","%Y-%m-%dT%H:%M:%SZ","%Y-%m-%dT%H:%M:%S","%Y-%m-%dT%H:%M:%S.%f"]:
                        try:
                            val = datetime.strptime(v, fmt)
                        except ValueError:
                            pass
                        else:
                            parsed[k] = val
                            break
                    else:
                        parsed[k] = v

            return parsed
        else:
            return SentenaiException()


    def update(self, kvs):
        kvs2 = {}
        for k, v in kvs.items():
            if v is None:
                kvs2[k] = None
            else:
                kvs2[k] = dts(v)
        if self._stream:
            self._stream._client.session.patch("/".join([self._stream._client.host, "streams", self._stream._name, "meta"]), json=kvs2)
        else:
            self._stream._client.session.post("/".join([self._stream._client.host, "streams", self._stream._name, "meta"]), json=kvs2)


    def replace(self, kvs):
        kvs2 = {}
        for k, v in kvs.items():
            kvs2[k] = dts(v)
        if self._stream:
            self._stream._client.session.put("/".join([self._stream._client.host, "streams", self._stream._name, "meta"]), json=kvs2)
        else:
            self._stream._client.session.post("/".join([self._stream._client.host, "streams", self._stream._name, "meta"]), json=kvs2)


    def clear(self):
        if self._stream:
            self._stream._client.session.put("/".join([self._stream._client.host, "streams", self._stream._name, "meta"]), json={})



    def __repr__(self):
        self._meta = self.read()
        return repr(self._meta)

    def _type(self, v):
        if type(v) in [int, float]:
            return "Numeric"
        elif type(v) == datetime:
            return "Datetime"
        elif type(v) == bool:
            return "Boolean"
        else:
            return "String"

    def _repr_html_(self):
        xs = []
        self._meta = self.read()
        if self._meta:
            for f,v in self._meta.items():
                xs.append({'field': f, 'value': str(v), 'type': self._type(v)})

        return pd.DataFrame(xs, columns=["field", "value", "type"])._repr_html_()

    def __getitem__(self, key):
        self._meta = self.read()
        return self._meta()[key]

    def __setitem__(self, key, val):
        self.update({key: val})

    def __delitem__(self, key):
        x = self.read()
        try:
            del x[key]
        except:
            print("not there")
        else:
            self.replace(x)


class Stream(object):
    def __init__(self, client, name, tz, exists, *filters):
        self._client = client
        self._exists = exists
        self.name = self._name = quote(name.encode('utf-8'))
        self._filters = filters
        self.tz = tz
        self._meta = StreamMetadata(self)


    def __len__(self):
        return self.stats().get('events')


    def __bool__(self):
        resp = self._client.session.get("/".join([self._client.host, "streams", self._name]), params={})
        if resp.status_code == 404:
            self._exists = False
        elif resp.status_code == 200:
            self._exists = True
        else:
            handle(resp)
        return self._exists

    __nonzero__ = __bool__


    def __enter__(self):
        return BaseStream(self._name, self.tz, *self._filters)

    def __exit__(self, *args, **kwargs):
        pass

    def log(self, event=None, ts=None, id=None, duration=None):
        if event is None:
            data = {}
        else:
            data = event
        e = self.Event(data=data, ts=ts, id=id, duration=duration).create()
        print(f"Event successfully logged at time {ts} in Stream('{self.name}')")

    _log = log

    def upload(self, file_path, ts="timestamp", threads=4, apply=dict):
        def f(row):
            timestamp = row[ts]
            d = apply(row)
            if apply is dict:
                del d[ts]
            self.Event(ts = timestamp, data = d).create()
            time.sleep(.01)

        with open(file_path) as fobj:
            fobj.seek(0)
            num_lines = sum(1 for line in fobj) - 1
            errors = 0
        with ThreadPool(threads) as pool:
            for x in log_progress(pd.read_csv(file_path, chunksize=threads), size=num_lines):
                pool.map(f, [r for i, r in x.iterrows()])



    _upload = upload

    def where(self, *filters, **kwargs):
        """Return copy of stream with filters."""
        kwargs['replace'] = True
        return self.filtered(*filters, **kwargs)


    def filtered(self, *filters, **kwargs):
        """Return copy of stream with additional filters.

        Keyword Argument:
            replace -- when True, copy stream while replacing filters instead of adding them.
        """
        if kwargs.get("replace", False):
            return Stream(self._client, self.name, self.tz, self._exists, *filters)
        else:
            return Stream(self._client, self.name, self.tz, self._exists, *(tuple(self._filters) + filters))



    @property
    def earliest(self):
        """Get the oldest event by timestamp in this stream.
        """
        return self._client.oldest(self)


    @property
    def latest(self):
        """Get the newest event by timestamp in this stream.
        """
        return self._client.newest(self)


    def _serialized_filters(self):
        if self._filters:
            return {'filters': base64.urlsafe_b64encode(bytes(json.dumps(self().get('filter')), 'UTF-8'))}
        else:
            return {}


    def __call__(self):
        """Generate AST for the stream object including any filters.

        Arguments:
            sw -- TODO: define this.
        """
        b = {'name': self._name}
        if self.tz:
            b['timezone'] = self.tz
        if self._filters:
            s = self._filters
            expr = s[-1]()
            if 'type' in expr:
                del expr['type']
            for x in s[-2::-1]:
                y = x()
                if 'type' in y:
                    del y['type']
                expr = {
                    'expr': '&&',
                    'args': [y, expr]
                }
            b['filter'] = expr
        return b

    def _oldest(self):
        """Get the oldest event by timestamp in this stream.
        """
        return self._client.oldest(self)


    oldest = property(_oldest)

    @property
    def newest(self):
        """Get the newest event by timestamp in this stream.
        """
        return self._client.newest(self)

    def fields(self):
        """Get a view of all fields in this stream."""
        return Fields(self._client.fields(self))
    _fields = fields

    def tags(self):
        """Get a view of all tags in this stream."""
        return Fields(self._client.fields(self), view="tag")

    def stats(self, field):
        """Get a dictionary of stream statistics."""
        return self._client.stream_stats(self, field)
    _stats = stats

    def values(self, at=None):
        """Get current values for every field in a stream.

        Keyword Arguments:
            at -- If given a datetime for `at`, return the values at that point in
                  time instead
        """

        at = at or datetime.utcnow()
        values = self._client.values(self, at)
        values_rendered = []
        for value in values:
            # create path
            pth = self
            for segment in value['path']:
                pth = pth[segment]
            ts = cts(value['ts'])
            values_rendered.append({
                'timestamp': ts,
                'event': value['id'],
                'value': value['value'],
                'path': pth,
            })
        return Values(self, at, values_rendered)
    _values = values

    def Event(self, *args, **kwargs):
        return Event(self.client, self, *args, **kwargs)
    _Event = Event

    def healthy(self):
        """Did the last `create` or `update` of an event on
        this stream succeed. For debugging purposes."""
        try:
            stats = self._client.stream_stats(self)
            return stats['healthy']
        except NotFound:
            return None

    _healthy = healthy

    def destroy(self, **kwargs):
        """Delete stream.

        Keyword Argument:
            confirm -- Must be `True` to confirm destroy stream
        """
        return self._client.destroy(self, **kwargs)
    _destroy = destroy

    def delete(self, id):
        """Delete event from the stream by its unique id.

        Arguments:
           eid    -- A unique ID corresponding to an event stored within
                     the stream.
        """
        return self._client.delete(self, id)
    _delete = delete

    def get(self, id):
        """Get event as JSON.

        Arguments:
           eid    -- A unique ID corresponding to an event stored within
                     the stream.
        """
        return self._client.get(self, id)
    _get = get

    def read(self, id):
        """Get event as JSON.

        Arguments:
           eid    -- A unique ID corresponding to an event stored within
                     the stream.
        """
        k = self._client.get(self, id)
        return Event(self._client, self, data=k['event'], id=k['id'], ts=cts(k['ts']), saved=True)
    _read = read

    def fstats(self, field, start=None, end=None):
        """Get stats for a given numeric field.

           Arguments:
           field  -- A dotted field name for a numeric field in the stream.
           start  -- Optional argument indicating start time in stream for calculations.
           end    -- Optional argument indicating end time in stream for calculations.
        """
        return self._client.field_stats(self, field, start, end)
    _fstats = fstats

    def describe(self, field, start=None, end=None):
        """Describe a given numeric field.

           Arguments:
           field  -- A dotted field name for a numeric field in the stream.
           start  -- Optional argument indicating start time in stream for calculations.
           end    -- Optional argument indicating end time in stream for calculations.
        """
        x = self._client.field_stats(self, field, start, end)
        if x.get('categorical'):
            print("count\t{count}\nunique\t{unique}\ntop\t{top}\nfreq\t{freq}".format(**x['categorical']))
        else:
            p = x['numerical']
            print("count\t{}\nmean\t{:.2f}\nstd\t{:.2f}\nmin\t{}\nmax\t{}".format(
                p['count'], p['mean'], p['std'], p['min'], p['max']))
    _describe = describe

    def unique(self, field):
        """Get unique values for a given field.

           Arguments:
           field  -- A dotted field name for a numeric field in the stream.
           start  -- Optional argument indicating start time in stream for calculations.
           end    -- Optional argument indicating end time in stream for calculations.
        """
        return UniqueView(self._client.unique(self, field))
    _unique = unique

    def put(self, event, id=None, timestamp=None, duration=None):
        """Put a new event into this stream.

        Arguments:
           event     -- A JSON-serializable dictionary containing an
                        event's data
           id        -- A user-specified id for the event that is unique to
                        this stream (optional)
           timestamp -- A user-specified datetime object representing the
                        time of the event. (optional)
        """
        return self._client.put(self, event, id, timestamp)
    _put = put

    def range(self, start, end, limit=None):
        """Get all of a stream's events between start (inclusive) and end (exclusive).

        Arguments:
           start  -- A datetime object representing the start of the requested
                     time range.
           end    -- A datetime object representing the end of the requested
                     time range.

           Result:
           A time ordered list of all events in a stream from `start` to `end`
        """
        return StreamRange(self, start, end, limit=limit)
    _range = range

    def tail(self, n=5):
        """Get all of a stream's events between start (inclusive) and end (exclusive).

        Arguments:
           n      -- A max number of events to return

           Result:
           A time ordered list of all events in a stream from `start` to `end`
        """
        return StreamRange(self, self.oldest.ts, self.newest.ts, limit=n, sorting='desc')

    def head(self, n=5):
        """Get all of a stream's events between start (inclusive) and end (exclusive).

        Arguments:
           n      -- A max number of events to return

           Result:
           A time ordered list of all events in a stream from `start` to `end`
        """
        return StreamRange(self, self.oldest.ts, self.newest.ts, limit=n, sorting='asc')



class UniqueView(object):
    def __init__(self, u):
        if u['categorical']:
            self.unique = u['categorical']
        elif u['numerical']:
            self.unique = u['numerical']
        else:
            self.unique = []

    def _repr_html_(self):
        if self.unique:
            return pd.DataFrame([{"value": k, "frequency": v} for k, v in self.unique])[["value","frequency"]]._repr_html_()
        else:
            return pd.DataFrame()._repr_html_()

    def __getitem__(self, x):
        return self.unique.get(str(x), 0)



class StreamRange(object):
    def __init__(self, stream, start, end, limit=None, sorting="asc"):
        self.stream = stream
        self._events = []
        self.sort = sorting
        self.limit = limit
        self.start = start
        self.end = end
        self.frequency = None

    def __getitem__(self, i):
        if not self._events:
            self._events = self.stream._client.range(self.stream, self.start, self.end, limit=self.limit, sorting=self.sort)
        return self._events[i]

    def __iter__(self):
        if not self._events:
            self._events = self.stream._client.range(self.stream, self.start, self.end, limit=self.limit, sorting=self.sort)
            if self.sort == "desc":
                self._events = reversed(self._events)
            return iter(self._events)

    def resample(self, freq):
        self.frequency = freq
        return self

    def agg(self, *args, **kwargs):
        if self.frequency is None:
            raise Exception("Cannot call `.agg()` on raw data.")
        for arg in args:
            # field renames
            if isinstance(arg, dict):
                for k, v in arg.items():
                    kwargs[k] = v
                continue

            base = kwargs
            segments = list(arg)
            for a in segments[:-1]:
                x = kwargs.get(a)
                if isinstance(x, dict):
                    base = x
                else:
                    base = base[a] = {}
            else:
                base[segments[-1]] = arg

        with self.stream as s:
            p = Proj(s, kwargs, resample=self.frequency)()['projection']

        self._events = self.stream._client.range(self.stream, self.start, self.end, limit=self.limit, proj=p, sorting=self.sort, frequency=self.frequency)

        if len(self._events):
            if self.sort == "desc":
                self._events = reversed(self._events)
            f = json_normalize([x.json(df=True) for x in self._events])
            return f.set_index('ts')
        else:
            return pd.DataFrame()

    def df(self, *args, **kwargs):
        if self.frequency is not None:
            raise Exception("Cannot call `.df()` on resampled data.")
        for arg in args:
            # field renames
            if isinstance(arg, dict):
                for k, v in arg.items():
                    kwargs[k] = v
                continue

            base = kwargs
            segments = list(arg)
            for a in segments[:-1]:
                x = kwargs.get(a)
                if isinstance(x, dict):
                    base = x
                else:
                    base = base[a] = {}
            else:
                base[segments[-1]] = arg

        with self.stream as s:
            p = Proj(s, kwargs)()['projection']

        self._events = self.stream._client.range(self.stream, self.start, self.end, limit=self.limit, proj=p, sorting=self.sort)

        if len(self._events):
            if self.sort == "desc":
                self._events = reversed(self._events)
            f = json_normalize([x.json(df=True) for x in self._events])
            return f.set_index('ts')
        else:
            return pd.DataFrame()


    def reshape(self, *args, lag, horizon, features):
        if args and not features:
            features = args
        if self.frequency is None:
            raise Exception("Cannot call `.reshape()` on raw data.")
        kwargs = dict(("feature-{:04d}".format(i), arg) for i, arg in enumerate(features))
        keys = list(sorted(kwargs.keys()))
        with self.stream as s:
            p = Proj(s, kwargs, resample=self.frequency)()['projection']
        r = self.stream._client.range(self.stream, self.start, self.end, limit=self.limit, proj=p, sorting=self.sort, frequency=self.frequency)

        def tensors():
            for i in range(len(r) - lag - horizon):
                yield ( np.array([[[e.data.get(k) for k in keys] for e in r[i:i+lag]]], np.float32)
                      , np.array([[e.data.get(k) for k in keys] for e in r[i+lag:i+lag+horizon]], np.float32)
                      )

        return TD(tensors())



    def json(self, *args):
        with self as s:
            if len(args) == 1 and isinstance(args[0], dict):
                p = Proj(s, args[0])()['projection']
            else:
                p = None
            return JSON.dumps([x.json(include_id=True) for x in self._events], default=dts, indent=4)


    def _repr_html_(self):
        return self.df()._repr_html_()

class TD(object):
    def __init__(self, xy):
        self.xy = xy
        self.validation_split = None
        self.vbuffer = []
        self.tbuffer = []

    def _get_next(self, test=True):
        if test and self.tbuffer:
            return self.tbuffer.pop(0)
        elif test:
            while True:
                if self.validation_split is None or random.random() >= self.validation_split:
                    return next(self.xy)
                else:
                    self.vbuffer.append(next(self.xy))
        elif self.vbuffer:
            return self.vbuffer.pop(0)
        else:
            while True:
                if self.validation_split and random.random() < self.validation_split:
                    return next(self.xy)
                else:
                    self.tbuffer.append(next(self.xy))


    def validation(self, split=0.2):
        self.validation_split = split
        while True:
            yield self._get_next(test=False)

    def test(self):
        while True:
            p = self._get_next()
            yield p


class StreamsView(object):
    def __init__(self, client, streams):
        self._client = client
        self._streams = streams

    def _repr_html_(self):
        if self._streams:
            return pd.DataFrame(self._streams)[['name', 'events', 'healthy']].rename(columns={'events': 'length'})._repr_html_()
        else:
            return pd.DataFrame(columns=["name", "length", "healthy"])._repr_html_()

    def __iter__(self):
        return iter([Stream(
            self._client,
            name=v['name'],
            tz=v.get('tz', None),
            exists=True
         ) for v in self._streams])

    def __getitem__(self, i):
        v = self._streams[i]
        return Stream(self._client, name=v['name'], tz=v.get('tz', None), exists=True)













def log_progress(sequence, size=0, name='Uploaded'):
    from ipywidgets import IntProgress, HTML, VBox
    from IPython.display import display

    if size <= 200:
        every = 1
    else:
        every = int(size / 200)


    progress = IntProgress(min=0, max=size, value=0)
    label = HTML()
    box = VBox(children=[label, progress])
    display(box)
    index = 0
    ts0 = datetime.utcnow()
    label.value = u'{name}: {index} / {size} Events'.format(
        name=name,
        index=index,
        size=size
    )
    try:
        for record in sequence:
            index += len(record)
            if index == 1 or index % every == 0:
                progress.value = index
                label.value = u'{name}: {index} / {size} Events'.format(
                    name=name,
                    index=index,
                    size=size
                )
            yield record
    except:
        progress.bar_style = 'danger'
        raise
    else:
        ts1 = datetime.utcnow()
        progress.bar_style = 'success'
        progress.value = index
        td = ts1 - ts0
        label.value = "{name} {index} Events in {time}".format(
            name=name,
            index=str(index or '?'),
            time="{:.1f} seconds".format(td.total_seconds()) if td.total_seconds() < 60 else ts
        )








