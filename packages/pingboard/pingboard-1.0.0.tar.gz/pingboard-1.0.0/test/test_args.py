import getpass
import pytest

import pingboard


def test_no_args(mocker):
    with pytest.raises(SystemExit) as e:
        pingboard.main([])
    assert 'Must specify at least one server' in str(e.value)


@pytest.fixture
def mock_main(mocker):
    sm = mocker.patch('pingboard.SocketMaster')
    cw = mocker.patch('curses.wrapper')
    pt = mocker.patch('pingboard.PingTarget')
    return (sm, cw, pt)


def test_one_server_arg(mock_main):
    '''If we call pingboard.main() with just one argument, check that the
    SocketMaster has a single PingTarget assigned to it'''

    pingboard.main(['localhost'])

    # Check there was only one pingtarget added
    sockmaster = mock_main[0]
    pingtarget = mock_main[2]
    assert len(sockmaster.call_args[1]['targets']) == 1

    pt_calls = pingtarget.call_args_list
    assert pt_calls[0][1]['hostname'] == 'localhost'


def test_several_server_arg(mock_main):
    '''If we call pingboard.main() with just several arguments, check that
    the SocketMaster has a correct PingTarget assigned to it'''

    pingboard.main(['www.debian.org', '8.8.8.8', 'www.theskepticsguide.org'])

    # Check there were three pingtarget set
    sockmaster = mock_main[0]
    pingtarget = mock_main[2]
    assert len(sockmaster.call_args[1]['targets']) == 3

    pt_calls = pingtarget.call_args_list
    assert pt_calls[0][1]['hostname'] == 'www.debian.org'
    assert pt_calls[1][1]['hostname'] == '8.8.8.8'
    assert pt_calls[2][1]['hostname'] == 'www.theskepticsguide.org'


def test_server_list(mock_main, tmpdir):
    '''If we call pingboard.main() with a file listing servers, check
    the SocketMaster has a correct PingTarget assigned to it'''

    fn = tmpdir.join('server-list.txt')
    fn.write('saltstack.org\npython.org\niwamashinshinaikido.com\n')
    pingboard.main(['--server-list', str(fn)])

    # Check there were three pingservers set
    sockmaster = mock_main[0]
    pingtarget = mock_main[2]
    assert len(sockmaster.call_args[1]['targets']) == 3

    pt_calls = pingtarget.call_args_list
    assert pt_calls[0][1]['hostname'] == 'saltstack.org'
    assert pt_calls[1][1]['hostname'] == 'python.org'
    assert pt_calls[2][1]['hostname'] == 'iwamashinshinaikido.com'


def test_server_list_comments(mock_main, tmpdir):
    '''If we call pingboard.main() with a file listing servers, where there
    are comments, check PingTarget gets those comments.'''

    fn = tmpdir.join('server-list.txt')
    fn.write('gatherer.wizards.com  Check the oracle!\n')
    pingboard.main(['--server-list', str(fn)])

    # Check there was only one pingtarget set
    sockmaster = mock_main[0]
    pingtarget = mock_main[2]
    assert len(sockmaster.call_args[1]['targets']) == 1

    pt_calls = pingtarget.call_args_list
    assert pt_calls[0][1]['hostname'] == 'gatherer.wizards.com'
    assert pt_calls[0][1]['comment'] == 'Check the oracle!'


def test_errors():
    with pytest.raises(SystemExit) as sysexit:
        pingboard.main(argv=['--min-wait', '0.1', 'localhost'])
    assert 'must be greater than 0.5' in str(sysexit.value)

    with pytest.raises(SystemExit) as sysexit:
        pingboard.main(argv=[])
    assert 'Must specify at least one server' in str(sysexit.value)


@pytest.mark.skipif(getpass.getuser() == 'root',
                    reason="requires non-root user")
def test_nonroot():
    with pytest.raises(SystemExit) as sysexit:
        pingboard.main(argv=['localhost'])
    assert 'Operation not permitted' in str(sysexit.value)
