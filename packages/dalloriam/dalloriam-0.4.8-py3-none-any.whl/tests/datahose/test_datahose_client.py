from dalloriam.datahose import DatahoseClient

from tests.mocks.response import MockResponse

from typing import Any, Dict, Optional

from unittest import mock

import pytest


def test_datahose_client_defines_correct_headers():
    password = 'some_password'
    c = DatahoseClient('some_host', password)

    assert c._headers == {
        'Authorization': password
    }


def test_datahose_push_sends_correct_payload():
    with mock.patch('requests.post', return_value=MockResponse(status_code=200)) as mock_post:
        c = DatahoseClient('some_host', 'some_password')
        c.push('some.key', {'some': 'data'})

        mock_post.assert_called_once_with('some_host', json={'key': 'some.key', 'body': {'some': 'data'}}, headers={
            'Authorization': 'some_password'
        })


def test_datahose_push_adds_time_to_payload_when_required():
    with mock.patch('requests.post', return_value=MockResponse(status_code=200)) as mock_post:
        c = DatahoseClient('some_host', 'some_password')
        c.push('some.key', {'some': 'data'}, time=42)

        mock_post.assert_called_once_with(
            'some_host',
            json={
                'key': 'some.key',
                'body': {'some': 'data'},
                'time': 42
            },
            headers={
                'Authorization': 'some_password'
            }
        )


def test_datahose_push_raises_valueerror_when_status_code_isnt_200():
    with mock.patch('requests.post', return_value=MockResponse(status_code=400, text='Something terrible happened')):
        c = DatahoseClient('some_host', 'some_password')

        with pytest.raises(ValueError):
            c.push('some.key', {'some': 'data'})


def test_datahose_notify_preformats_body_for_push():
    c = DatahoseClient('some_host', 'some_password')

    with mock.patch.object(c, 'push') as mock_push:
        c.notify('some_sender', 'some_message')

        mock_push.assert_called_once_with('notification', data={
            'sender': 'some_sender',
            'message': 'some_message'
        })


@mock.patch('dalloriam.datahose.client.DatahoseClient._try_get_disk_config', {'service_host': 'hello', 'password': 'word'})
@pytest.mark.parametrize(
    'disk_data, provided_args,want_err',
    [
        ({'service_host': 'my_host', 'password': 'pwd'}, {}, None),
        ({'service_host': 'my_host'}, {'password': 'pwd'}, None),
        ({}, {'service_host': 'my_host', 'password': 'pwd'}, None),
        ({}, {'password': 'pwd'}, ValueError),
        ({'service_host': 'my_host'}, {}, ValueError),
    ]
)
def test_datahose_initialize_config_autodetect(disk_data: Dict[str, Any], provided_args: Dict[str, Any],
                                               want_err: Optional[Exception]):
    with mock.patch('dalloriam.datahose.client.DatahoseClient._try_get_disk_config', return_value=disk_data):
        if want_err is None:
            try:
                c = DatahoseClient(**provided_args)
                assert c._push_url is not None
                assert c._push_url == disk_data.get('service_host') or provided_args.get('service_host')

                assert c._headers.get('Authorization') is not None
                assert c._headers.get('Authorization') == disk_data.get('password') or provided_args.get('password')
            except Exception as e:  # pragma: nocover
                pytest.fail(f'datahose client should not have raised [{type(e)}]')  # pragma: nocover
        else:
            with pytest.raises(want_err):
                DatahoseClient(**provided_args)
