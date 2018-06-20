# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'item':item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):

        # image_folder_name = response.css('h2 a::text').contract_first().strip()  
        image_folder_name = request.meta['item']['image_folder_name']
        image_guid = request.url.split('/')[-1]  
        return 'full/{0}/{1}'.format(image_folder_name, image_guid)
        ## end of deprecation warning block

        # image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        # image_folder_name = response.css('h2 a::text').contract_first().strip()
        # image_guid = request.url.split('/')[-1]
        # return 'full/%s' % (image_guid)

# import scrapy
# from scrapy.pipelines.images import ImagesPipeline
# from scrapy.exceptions import DropItem

# class MyImagesPipeline(ImagesPipeline):

#     # def get_media_requests(self, item, info):
#     #     for image_url in item['image_urls']:
#     #         yield scrapy.Request(image_url)

#     # def item_completed(self, results, item, info):
#     #     image_paths = [x['path'] for ok, x in results if ok]
#     #     if not image_paths:
#     #         raise DropItem("Item contains no images")
#     #     item['image_paths'] = image_paths
#     #     return item

#     # def file_path(self, request, response=None, info=None):
#     # 	image_guid = response.css('h2 a::text').contract_first().strip()
#     # 	return 'full/%s' % (image_guid)

#     # def get_media_requests(self, item, info):
#     #     return [Request(x) for x in item.get(self.images_urls_field, [])]

#     # def item_completed(self, results, item, info):
#     #     if isinstance(item, dict) or self.images_result_field in item.fields:
#     #         item[self.images_result_field] = [x for ok, x in results if ok]
#     #     return item    
#     def get_media_requests(self, item, info):
#         for image_url in item['image_urls']:
#             yield scrapy.Request(image_url)

#     def item_completed(self, results, item, info):
#         image_paths = [x['path'] for ok, x in results if ok]
#         if not image_paths:
#             raise DropItem("Item contains no images")
#         item['image_paths'] = image_paths
#         return item

#     def file_path(self, request, response=None, info=None):
#         ## start of deprecation warning block (can be removed in the future)
#         def _warn():
#             from scrapy.exceptions import ScrapyDeprecationWarning
#             import warnings
#             warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
#                           'please use file_path(request, response=None, info=None) instead',
#                           category=ScrapyDeprecationWarning, stacklevel=1)

#         # check if called from image_key or file_key with url as first argument
#         if not isinstance(request, Request):
#             _warn()
#             url = request
#         else:
#             url = request.url

#         # detect if file_key() or image_key() methods have been overridden
#         if not hasattr(self.file_key, '_base'):
#             _warn()
#             return self.file_key(url)
#         elif not hasattr(self.image_key, '_base'):
#             _warn()
#             return self.image_key(url)
#         ## end of deprecation warning block

#         # image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
#         # image_folder_name = response.css('h2 a::text').contract_first().strip()
#         image_guid = request.url.split('/')[-1]
#         return 'full/%s' % (image_guid)