import json
import logging
import os
from enum import Enum
from typing import Optional, MutableMapping, List
from .metrics import Aggregator, Gauge, Counter


class Status(Enum):
    """
    Status enum encapsulates all valid status values
    """
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3


class Target:

    def __init__(self, check, instance):
        self.instance = instance
        self.check = check

    @property
    def env(self):
        return {**self.check.env, **self.instance.env}


class Plugin(object):

    def __init__(self,
                 aggregator: Aggregator = Aggregator(),
                 env: MutableMapping[str, str] = os.environ,
                 logger: Optional[logging.Logger] = None) -> None:
        self.aggregator = aggregator
        self.env = env
        self.logger = logger or self.create_logger()
        self.samples: List = []

    def run(self):
        try:
            status = self.collect({})
            if status is None:
                status = Status.OK

            self.samples.extend(self.aggregator.flush())
            # print metrics to standard out
            print(json.dumps({
                "registry": list(self.samples),
                "version": "0.2.0"
            }))
            return status.value
        except Exception as ex:
            self.logger.exception(ex)
            return Status.CRITICAL.value

    """
    The Plugin API.
    Users must derive from this class when implementing a custom Plugin
    """
    def collect(self, target: Target) -> Status:
        """
        Perform collections operations for the provided Target
        """
        raise NotImplementedError()

    def sample(self,
               name: str,
               value: float,
               timestamp: int,
               labels: Optional[dict] = None,
               host: Optional[str] = None,
               type: Optional[str] = 'gauge'):
        labels = labels or {}

        self.samples.append({
            'name': name,
            'value': value,
            'timestamp': timestamp,
            'labels': labels,
            'host': host,
            'storage_type': type,
        })


    def gauge(self, name: str, labels: Optional[dict] = None) -> Gauge:
        """Get a Gauge instance for the specified Name/Labels"""
        labels = labels or {}
        return self.aggregator.gauge(name, labels)

    def counter(self, name: str, labels: Optional[dict] = None) -> Counter:
        """Get a Counter instance for the specified Name/Labels"""
        labels = labels or {}
        return self.aggregator.counter(name, labels)

    def status(self, status: Status, labels: Optional[dict] = None):
        labels = labels or {}
        self.aggregator.gauge("service.status", labels).set(float(status.value))
        return status

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a Deployment config property"""
        return self.env.get(key, default)


    @classmethod
    def create_logger(cls, level='INFO') -> logging.Logger:
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.getLevelName(level))

        return logging.getLogger(cls.__name__)
