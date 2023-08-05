# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['coub_api', 'coub_api.modules', 'coub_api.schemas']

package_data = \
{'': ['*']}

modules = \
['README', 'LICENSE']
install_requires = \
['pydantic>=0.16.1,<0.17.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.6.0,<0.7.0']}

setup_kwargs = {
    'name': 'coub-api',
    'version': '0.1.1a0',
    'description': 'Api wrapper for coub.com',
    'long_description': '===============================\nApi-wrapper for coub.com\n===============================\n\n.. image:: https://travis-ci.com/Derfirm/coub_api.svg?branch=master\n    :target: https://travis-ci.com/Derfirm/coub_api\n    :alt: Build Status\n\n.. image:: https://codecov.io/gh/Derfirm/coub_api/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/Derfirm/coub_api\n    :alt: Coverage Status\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n    :alt: Codestyle: Black\n\nKey Features\n============\n- response are fully-annotated with pydantic\n- test work on snapshots from real http-answers (can easy inspect responses)\n\nGetting started\n===============\nInitiate Api client\n________\n.. code-block:: python\n\n    from coub_api import CoubApi\n\n    api = CoubApi()\n    access_token = "<your access token>"\n    api.authenticate(access_token)  # required for some authenticated requests\n\n\nGet coub details\n________________\n.. code-block:: python\n\n    coub = api.coubs.get_coub("1jf5v1")\n    print(coub.id, coub.channel_id)\n\nCreate Coub\n___________\n.. code-block:: python\n\n    api.coubs.init_upload()) # {"permalink":"1jik0b","id":93927327}\n    api.coubs.upload_video(93927327, "video.mp4")\n    api.coubs.upload_audio(93927327, "audio.mp3"))\n    api.coubs.finalize_upload(93927327, title="Awesome CAT", tags=["cat", "animal"]))\n    api.coubs.get_upload_status(93927327))  # {"done": False, "percent_done": 0}\n    # wait a minute\n    api.coubs.get_upload_status(93927327))  # {"done": True, "percent_done": 100}\n\n\n\nGet weekly hot coubs\n___________\n.. code-block:: python\n\n    from coub_api.schemas.constants import Period\n    api.timeline.hot(period=Period.WEEKLY, order_by="likes_count")\n\n\nGet 5 page of random section with cars\n___________\n.. code-block:: python\n\n    from coub_api.schemas.constants import Section, Category\n\n    current_page = 1\n    max_page = 5\n    while current_page <= max_page:\n        response = api.timeline.section(section=Section.RANDOM, category=Category.CARS, per_page=30, page=current_page)\n        print(f"processing {current_page} of {max_page}")\n        for coub in response.coubs:\n            print(coub.permalink)\n        current_page += 1\n        max_page = min(max_page, response.total_pages)\n\n',
    'author': 'Andrew Grinevich',
    'author_email': 'andrew.grinevich@gmail.com',
    'url': 'https://github.com/Derfirm/coub_api',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
