from django.conf import settings
from items.models import Item, ItemTag
from request_manager.utils import requester

def request_all_item_info():
    all_item_request = requester('https://global.api.pvp.net/api/lol/static-data/na/v1.2/item?locale=en_US&itemListData=all&api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d','get')
    item_data = all_item_request['data']
    item_data_list = []
   
    for item in item_data:
        item_data_list.append(item_data[item])
        raw_tag = False

        try:
            raw_tag = item_data[item]['tags']
        except:
            try:
                raw_tag = item_data[item]['tag']
            except:
                pass

        if raw_tag:
            item, created = Item.objects.get_or_create(
            name = item_data[item]['name'], 
            riot_id = item_data[item]['id'])
            for tag in list(raw_tag):
                item_tag, tag_created = ItemTag.objects.get_or_create(item = item, tag = tag)
                print item_tag.item, item_tag.tag
                if tag_created == True:
                    item_tag.save()
            if created == True:
                item.save()  


              