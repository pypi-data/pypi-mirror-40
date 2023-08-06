import json
import logging
import math
import threading
import time
from typing import Optional, Dict, Union, Tuple, Iterable, Type, Hashable, cast

logger = logging.getLogger(__name__)

MetricLabels = Dict[str, str]


def validate_value(value: Union[int, float]) -> float:
    if type(value) == int:
        value = float(value)

    if not math.isfinite(value):
        raise ValueError(f"Non finite {value} in not supported")

    return value


class Sample:

    def __init__(self,
                 name: str,
                 value: float,
                 host: str,
                 storage_type: str,
                 labels: MetricLabels,
                 timestamp: int,
                 ttl: Optional[int] = None,
                 ) -> None:
        self.name: str = name
        self.value = value
        self.host = host
        self.type = storage_type
        self.labels = labels or {}
        self.ttl = ttl
        self.timestamp = timestamp

        # created is used to calculate the age of a sample, not the timestamp,
        # this prevents expiring historical samples before they are published
        self.created = self.get_timestamp()

    def __repr__(self) -> str:
        return json.dumps(self.to_dict())

    def __hash__(self) -> int:
        return hash((self.name, self.type, tuple(sorted(self.labels.items()))))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sample):
            return False

        return self.__hash__() == other.__hash__()

    def to_dict(self) -> Dict:
        return self.__dict__

    @property
    def never_expires(self) -> bool:
        return self.ttl is None

    @property
    def age_seconds(self) -> int:
        return int(self.age_ms / 1000)

    @property
    def age_ms(self) -> int:
        # Age is based on the time we created/collected the sample,
        # this prevents expiring historical samples before they are published
        return self.get_timestamp() - self.created

    @property
    def ttl_ms(self):
        return self.ttl_ms

    @property
    def has_expired(self) -> bool:
        if self.never_expires:
            return False
        else:
            ttl = self.ttl or 0
            return self.age_seconds > ttl

    @staticmethod
    def get_timestamp() -> int:
        return int(round(time.time() * 1000))


class Metric(object):

    def __init__(self,
                 name: str,
                 labels: dict,
                 ttl: Optional[int] = None) -> None:
        self._name: str = name
        self._labels: Dict[str, str] = labels
        self._value: float = 0.0
        self._ttl = ttl

    @staticmethod
    def hash(name: str, labels: dict) -> Tuple[str, Tuple]:
        return name, tuple(sorted(labels.items()))

    def set(self,
            value: float,
            ttl: Optional[int]=None) -> 'Metric':
        """set the value for this metric"""
        self._value = validate_value(value)
        if ttl:
            self._ttl = ttl

        return self

    def get(self) -> float:
        return self._value

    def flush(self, parent_labels: Dict[str, str]) -> Dict:
        labels = {**parent_labels, **self._labels}
        return {
            'name': self._name,
            'value': self._value,
            'storage_type': self.type,
            'labels': labels,
            'ttl': self._ttl,
        }

    @property
    def type(self) -> str:
        raise NotImplementedError()


class Gauge(Metric):

    @property
    def type(self) -> str:
        return 'gauge'

    def inc(self, value: float=1.0) -> None:
        """increment the gauge by value. value will default to 1"""
        self.set(self._value + value)

    def dec(self, value: float=1.0) -> None:
        """decrement the gauge by value. value will default to 1"""
        self.set(self._value - value)


class Counter(Metric):

    @property
    def type(self) -> str:
        return 'counter'

    def inc(self, value: float=1.0) -> None:
        """increment the counter by value. value will default to 1"""
        self.set(self._value + value)


class Aggregator:

    def __init__(self,
                 labels: Optional[MetricLabels]=None
                 ) -> None:
        self.labels = labels or {}
        self.metrics: Dict[Hashable, Metric] = {}
        self._lock = threading.Lock()

    def reset(self):
        with self._lock:
            self.metrics = {}

    def flush(self) -> Iterable[Dict]:
        with self._lock:
            for m in self.metrics.values():
                yield m.flush(self.labels)

    def submit(self,
               type: str,
               name: str,
               value: float,
               labels: Optional[dict]=None,
               ttl: Optional[int]=None) -> None:
        metrics = {
            'gauge': Gauge,
            'counter': Counter
        }
        self._ensure_metric(metrics[type], name, labels).set(value, ttl)

    def gauge(self, name: str, labels: Optional[dict]=None) -> Gauge:
        """Get a Gauge instance for the specified Name/Labels"""
        return cast(Gauge, self._ensure_metric(Gauge, name, labels))

    def counter(self, name: str, labels: Optional[dict]=None) -> Counter:
        """Get a Counter instance for the specified Name/Labels"""
        return cast(Counter, self._ensure_metric(Counter, name, labels))

    def _ensure_metric(self,
                       metric_class: Type[Metric],
                       name: str,
                       labels: Optional[Dict[str, str]]=None) -> Metric:
        """
        ensure a metrics is registered with the plugin
        """
        if labels is None:
            labels = {}

        key = metric_class.hash(name, labels)
        if key not in self.metrics:
            with self._lock:
                self.metrics[key] = metric_class(name=name,
                                                 labels=labels)

        if not isinstance(self.metrics[key], metric_class):
            raise Exception('metric type mismatch')

        return self.metrics[key]
