import os
import unittest

from satstac import Items, Item

testpath = os.path.dirname(__file__)


class Test(unittest.TestCase):

    def load_items(self):
        return Items.load(os.path.join(testpath, 'items.json'))

    def test_load(self):
        """ Initialize Scenes with list of Scene objects """
        items = self.load_items()
        assert(len(items._collections) == 1)
        assert(len(items) == 2)
        assert(isinstance(items[0], Item))

    def test_save(self):
        """ Save items list """
        items = self.load_items()
        fname = os.path.join(testpath, 'save-test.json')
        items.save(fname)
        assert(os.path.exists(fname))
        os.remove(fname)
        assert(not os.path.exists(fname))

    def test_collection(self):
        """ Get a collection """
        items = self.load_items()
        col = items.collection('landsat-8-l1')
        assert(col.id == 'landsat-8-l1')

    def test_no_collection(self):
        """ Attempt to get non-existent collection """
        items = self.load_items()
        col = items.collection('nosuchcollection')
        assert(col is None)

    def test_bbox(self):
        items = self.load_items()
        bbox = items.bbox()
        assert(len(bbox) == 4)
        assert(bbox == [11.984710693359375, 44.815941348210835, 12.752380371093748, 45.67740123855739])

    def test_center(self):
        items = self.load_items()
        center = items.center()
        assert(center == [45.24667129338411, 12.368545532226562])

    def test_get_properties(self):
        """ Get set of properties """
        items = self.load_items()
        p = items.properties('eo:platform')
        assert(len(p) == 1)
        assert(p[0] == 'landsat-8')

    def test_print_items(self):
        """ Print summary of items """
        items = self.load_items()
        print(items.summary())

    def test_dates(self):
        """ Get dates of all items """
        items = self.load_items()
        dates = items.dates()
        assert(len(dates) == 1)

    def test_text_calendar(self):
        """ Get calendar """
        items = self.load_items()
        cal = items.calendar()
        assert(len(cal) > 250)

    def test_download_thumbnails(self):
        """ Download all thumbnails """
        items = self.load_items()
        fnames = items.download(key='thumbnail')
        for f in fnames:
            assert(os.path.exists(f))
            os.remove(f)
            assert(not os.path.exists(f))
        #shutil.rmtree(os.path.join(testpath, 'landsat-8-l1'))

    def test_filter(self):
        items = self.load_items()
        items.filter('eo:cloud_cover', [100])
        assert(len(items) == 1)

    def test_download(self):
        """ Download a data file from all items """
        items = self.load_items()
        
        fnames = items.download(key='MTL')
        assert(len(fnames) == 2)
        for f in fnames:
            assert(os.path.exists(f))
            os.remove(f)
            assert(not os.path.exists(f))
        #shutil.rmtree(os.path.join(testpath, 'landsat-8-l1'))
