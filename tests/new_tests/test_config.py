from unittest.mock import Mock

from pytest_mock import MockerFixture

import peracotta


def test_config(mocker: MockerFixture):
    mocked_open: Mock = mocker.patch(open)
