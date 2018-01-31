#
# The MIT License (MIT)
#
# Copyright (c) 2018 Rafid Khalid Al-Humaimidi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from django.http import HttpResponse
from django.template import loader
from django.contrib.staticfiles import finders
import hashlib

from HadithHouseWebsite import settings
from HadithHouseWebsite.server_settings import get_fb_appid

all_js_hash = None
all_css_hash = None


def md5(file_name):
    """
    Find the MD5 hash of the given file.
    Taken from: http://stackoverflow.com/q/3431825

    :param file_name: The name of the file
    :return: The MD5 hash
    """
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def set_all_js_hash():
    # Find the hash of all.js, which is used in index.html for cache busting.
    # TODO: Perhaps consider saving it to file to avoid re-calculating it every
    # time the application is restarted?
    # https://github.com/hadithhouse/hadithhouse/issues/307
    global all_js_hash
    if all_js_hash is None and settings.get_environment() == 'production':
        all_js_hash = md5(finders.find('hadiths/js/all.js'))


def set_all_css_hash():
    # Find the hash of all.css, which is used in index.html for cache busting.
    # TODO: Perhaps consider saving it to file to avoid re-calculating it every
    # time the application is restarted?
    # https://github.com/hadithhouse/hadithhouse/issues/307
    global all_css_hash
    if all_css_hash is None and settings.get_environment() == 'production':
        all_css_hash = md5(finders.find('hadiths/css/all.css'))


def index(request, path):
    set_all_js_hash()
    set_all_css_hash()

    context = {
        'appId': get_fb_appid(),
        'offline_mode': settings.OFFLINE_MODE,
        'environment': settings.get_environment(),
        'all_js_hash': all_js_hash,
        'all_css_hash': all_css_hash,
    }

    template_names = [
        'hadiths/index.html',
        'hadiths/index_react.html',
        'hadiths/index_angular.html'
    ]
    template_name = template_names[int(settings.JS_FRAMEWORK_MODE)]
    template = loader.get_template(template_name)

    return HttpResponse(template.render(context))
