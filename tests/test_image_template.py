# Standard library
import unittest

# Local
from canonicalwebteam import image_template
from urllib.parse import quote


asset_url = (
    "https://assets.ubuntu.com/" "v1/479958ed-vivid-hero-takeover-kylin.jpg"
)
encoded_asset_url = quote(asset_url)
non_asset_url = (
    "https://dashboard.snapcraft.io/site_media/appmedia/"
    "2018/10/Screenshot_from_2018-10-26_14-20-14.png"
)
non_hostname_url = "/static/images/Screenshot_from_2018-10-26_14-20-14.png"


class TestImageTemplate(unittest.TestCase):
    def test_returns_string(self):
        markup = image_template(
            url=asset_url,
            alt="test",
            width="1920",
            height="1080",
            hi_def=False,
        )
        self.assertTrue(isinstance(markup, str))

    def test_attributes(self):
        markup = image_template(
            url=asset_url,
            alt="test",
            width="1920",
            height="1080",
            id="test",
            title="test title",
            hi_def=False,
        )
        self.assertTrue(markup.find('id="test"') > -1)
        self.assertTrue(markup.find('title="test title"') > -1)

    def test_classes(self):
        markup = image_template(
            url=asset_url,
            alt="test",
            width="1920",
            height="1080",
            extra_classes="test-title",
            hi_def=False,
        )
        # Check custom class exists
        self.assertTrue(markup.find('class="test-title"') > -1)
        # Check lazyload class still exists
        self.assertTrue(markup.find('class="lazyload test-title"') > -1)

    def test_hi_def(self):
        markup = image_template(
            url=non_asset_url,
            alt="test",
            width="1920",
            height="1080",
            hi_def=True,
        )
        markup_asset = image_template(
            url=asset_url, alt="test", width="1920", height="1080", hi_def=True
        )

        # Check the markup includes srcset
        self.assertTrue(markup.find("srcset="))
        self.assertTrue(markup.find("data-srcset"))
        # Check x2 is present
        self.assertTrue(markup.find("x2"))
        # Check width and height are double
        self.assertTrue(markup.find("3840"))
        self.assertTrue(markup.find("2160"))

        self.assertTrue(markup_asset.find("srcset="))
        self.assertTrue(markup_asset.find("data-srcset"))
        self.assertTrue(markup_asset.find("x2"))
        self.assertTrue(markup_asset.find("w%3D3840%26h%3D2160"))

    def test_assets_url_has_width_and_height(self):
        markup_asset = image_template(
            url=asset_url,
            alt="test",
            width="1920",
            height="1080",
            hi_def=False,
        )
        markup_non_asset = image_template(
            url=non_asset_url,
            alt="test",
            width="1920",
            height="1080",
            hi_def=False,
        )

        self.assertTrue(
            encoded_asset_url + "%3Fw%3D1920%26h%3D1080" in markup_asset
        )
        self.assertTrue("w_1920" not in markup_asset)
        self.assertTrue("w_1920" in markup_non_asset)


if __name__ == "__main__":
    unittest.main()
