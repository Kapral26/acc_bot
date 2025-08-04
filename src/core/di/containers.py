from dishka import make_async_container

from src.app.analytics.bad_phrase.dependencies import BadPhraseRepositoryProvider
from src.app.dependencies import LoggerProvider


def create_container():
    containers = [LoggerProvider(), BadPhraseRepositoryProvider()]

    return make_async_container(*containers)
