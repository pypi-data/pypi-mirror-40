import pytest
import time
import getpass
import pingboard


@pytest.mark.skipif(getpass.getuser() != 'root',
                    reason='requires root user')
def test_ping_localhost_name():
    target = pingboard.PingTarget(unique_id=1, hostname='localhost')
    socketmaster = pingboard.SocketMaster(targets={1: target},
                                          min_wait=0.5, max_wait=1)

    socketmaster.setDaemon(True)
    socketmaster.start()

    time.sleep(3)
    details = socketmaster.target_details()
    assert details[0]['state'] == 'alive'
