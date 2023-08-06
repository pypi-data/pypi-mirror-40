from PIL import Image
import numpy as np
import urllib2
import json
from google.protobuf import json_format

class api_utils(object):

    @staticmethod
    def hash_config(request_config):
        return frozenset(request_config.to_dict().items())

    @staticmethod
    def rest_api_call(url, uri_dict):
        url += "&".join(["{}={}".format(k,v) for k,v in uri_dict.iteritems()]).replace(" ", "")
        print("Making REST API call to: {}".format(url))
        response = urllib2.urlopen(url).read()
        return json.loads(response)

    @staticmethod
    def url_exists(url):
        try:
            urllib2.urlopen(url)
            return True
        except urllib2.HTTPError, e:
            # print("{}: {}".format(e.code, url))
            return False
        except urllib2.URLError, e:
            # print("{}: {}".format(e.args, url))
            return False

    @staticmethod
    def resource_location_endpoint(resource_name, blob_form, request_config):
        resource_filename = resource_name + "/" + blob_form.format(**request_config)
        return resource_filename

    @staticmethod
    def display_numpy(data, filename=None, show_image=False, data_is_normalized_to_one=True):
        if data_is_normalized_to_one:
            data = data * 255.

        image = Image.fromarray(np.array(data, dtype=np.uint8))
        if filename is not None:
            image.save(filename)
        if show_image:
            image.show()

    @staticmethod
    def _rectangular_polygon(c, r):
        p = []
        p.append([c[0] - r, c[1] - r])
        p.append([c[0] + r, c[1] - r])
        p.append([c[0] + r, c[1] + r])
        p.append([c[0] - r, c[1] + r])
        p.append([c[0] - r, c[1] - r])
        return p

    @staticmethod
    def _chicago_test_aoi():
        center = [41.2, -87.5]
        radius = 1.5
        aoi = api_utils._rectangular_polygon(center, radius)
        return aoi

    @staticmethod
    def _imperial_test_aoi():
        center = [32.843454, -115.6003187]
        radius = 0.1
        aoi = api_utils._rectangular_polygon(center, radius)
        return aoi

    @staticmethod
    def log_and_return_status(msg, code, request, logger, exc_info=False):
        logger.info("{}: {:.10000} \n Request: {:.10000}".format(code, str(msg), str(request)), exc_info=exc_info)
        return msg, code

    @staticmethod
    def log_and_return_pb(pb, code, request, logger, exc_info=False):
        logger.info("{}: {:.10000} \n Request: {:.10000}".format(code, str(pb), str(request)), exc_info=exc_info)
        return json_format.MessageToJson(pb), code

    @staticmethod
    def simple_cache_get(app, name, default):
        c = app.cache.get(name)
        if c is None:
            return default
        else:
            return c

    @staticmethod
    def simple_cache_set(app, name, value):
        app.cache.set(name, value)
