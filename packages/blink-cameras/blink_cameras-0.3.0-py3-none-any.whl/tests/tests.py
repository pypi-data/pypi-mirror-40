import json, unittest
from blink import Blink

class TestBlink(unittest.TestCase):

  def test_connect(self):
    b = Blink()
    self.assertFalse(b.connected)
    b.connect()
    self.assertTrue(b.connected)

  def test_homescreen(self):
    b = Blink()
    data = b.homescreen()
    self.assertTrue(data['account'] is not None)

  def test_events(self):
    b = Blink()
    b.connect()
    events = b.events(b.networks[0])
    self.assertEqual(type(events), list)

  def test_cameras(self):
    b = Blink()
    b.connect()
    cameras = b.cameras(b.networks[0])
    self.assertEqual(type(cameras), list)

  def test_download_video(self):
    b = Blink()
    b.connect()
    events = b.events(b.networks[0])
    if events:
        event = events[0]
        b.download_video(event)

  def test_videos_list(self):
    b = Blink()
    b.connect()
    videos = b.videos()
    assert len(videos) > 0
    print(videos[:10])

  def test_download_by_address(self):
    b = Blink()
    b.connect()
    videos = b.videos()
    b.download_video_by_address(videos[0]['address'])

  def _test_download_thumbnail(self):
    '''doesn't work'''
    b = Blink()
    b.connect()
    network_id = b.networks[0]['id']
    events = b.events(network_id)
    event = events[0]
    b.download_thumbnail(event)

  def test_sync_modules(self):
    b = Blink()
    b.connect()
    sync_modules = b.sync_modules(b.networks[0])
    print(sync_modules)

  def _test_arm(self):
    b = Blink()
    b.connect()
    print(b.arm(b.networks[0]))

  def test_clients(self):
    b = Blink()
    print(b.clients())

  def test_regions(self):
    b = Blink()
    print(b.regions())

  def test_health(self):
    b = Blink()
    print(b.health())



if __name__ == '__main__':
    unittest.main()

