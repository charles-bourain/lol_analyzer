from django.conf import settings
from items.models import Item, ItemTag
from request_manager.utils import requester

def request_all_item_info():

    def _get_item_stats_from_json(item, stat_str):
        try:
            return item_data[item]['stats'][stat_str]
        except:
            return None


    # def assign_fields(stat_key):
    #     full_stat = 'item.Item.'+str(stat_key)
    #     print 'Stat Key = ', stat_key

    #     for field in Item.__meta.get_fields():
    #         if field == full_stat:
                




    all_item_request = requester('https://global.api.pvp.net/api/lol/static-data/na/v1.2/item?itemListData=all&api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d','get')
    item_data = all_item_request['data']
    item_data_list = []
   
    for item in item_data:

        item_data_list.append(item_data[item])

        try:
            Item.objects.get(riot_id = item_data[item]['id'])
            continue
        except:
            pass
        try:
            item, created = Item.objects.get_or_create(
            
                riot_id = item_data[item]['id'],
                name = item_data[item]['name'], 
                image = item_data[item]['image'],
                FlatArmorMod = _get_item_stats_from_json(item, 'FlatArmorMod'),
                FlatAttackSpeedMod =  _get_item_stats_from_json(item,'FlatAttackSpeedMod'),  
                FlatBlockMod =  _get_item_stats_from_json(item,'FlatBlockMod'),    
                FlatCritChanceMod = _get_item_stats_from_json(item,'FlatCritChanceMod'),   
                FlatCritDamageMod = _get_item_stats_from_json(item, 'FlatCritDamageMod'),   
                FlatEXPBonus = _get_item_stats_from_json(item, 'FlatEXPBonus'),    
                FlatEnergyPoolMod = _get_item_stats_from_json(item, 'FlatEnergyPoolMod'),   
                FlatEnergyRegenMod = _get_item_stats_from_json(item, 'FlatEnergyRegenMod'),  
                FlatHPPoolMod = _get_item_stats_from_json(item, 'FlatHPPoolMod'),   
                FlatHPRegenMod = _get_item_stats_from_json(item, 'FlatHPRegenMod'),  
                FlatMPPoolMod = _get_item_stats_from_json(item, 'FlatMPPoolMod'),   
                FlatMPRegenMod = _get_item_stats_from_json(item, 'FlatMPRegenMod'),  
                FlatMagicDamageMod = _get_item_stats_from_json(item, 'FlatMagicDamageMod'),  
                FlatMovementSpeedMod = _get_item_stats_from_json(item, 'FlatMovementSpeedMod'),   
                FlatPhysicalDamageMod = _get_item_stats_from_json(item, 'FlatPhysicalDamageMod'),  
                FlatSpellBlockMod = _get_item_stats_from_json(item, 'FlatSpellBlockMod'),   
                PercentArmorMod = _get_item_stats_from_json(item, 'PercentArmorMod'), 
                PercentAttackSpeedMod = _get_item_stats_from_json(item, 'PercentAttackSpeedMod'),   
                PercentBlockMod = _get_item_stats_from_json(item, 'PercentBlockMod'), 
                PercentCritChanceMod = _get_item_stats_from_json(item, 'PercentCritChanceMod'),    
                PercentCritDamageMod = _get_item_stats_from_json(item, 'PercentCritDamageMod'),   
                PercentDodgeMod = _get_item_stats_from_json(item, 'PercentDodgeMod'),
                PercentEXPBonus = _get_item_stats_from_json(item, 'PercentEXPBonus'), 
                PercentHPPoolMod = _get_item_stats_from_json(item, 'PercentHPPoolMod'),    
                PercentHPRegenMod = _get_item_stats_from_json(item, 'PercentHPRegenMod'),   
                PercentLifeStealMod = _get_item_stats_from_json(item, 'PercentLifeStealMod'), 
                PercentMPPoolMod = _get_item_stats_from_json(item, 'PercentMPPoolMod'),    
                PercentMPRegenMod = _get_item_stats_from_json(item, 'PercentMPRegenMod'),   
                PercentMagicDamageMod = _get_item_stats_from_json(item, 'PercentMagicDamageMod'),   
                PercentMovementSpeedMod = _get_item_stats_from_json(item, 'PercentMovementSpeedMod'), 
                PercentPhysicalDamageMod = _get_item_stats_from_json(item, 'PercentPhysicalDamageMod'),    
                PercentSpellBlockMod = _get_item_stats_from_json(item, 'PercentSpellBlockMod'),    
                PercentSpellVampMod = _get_item_stats_from_json(item, 'PercentSpellVampMod'),
                rFlatArmorModPerLevel = _get_item_stats_from_json(item, 'rFlatArmorModPerLevel'),  
                rFlatArmorPenetrationMod = _get_item_stats_from_json(item, 'rFlatArmorPenetrationMod'),    
                rFlatArmorPenetrationModPerLevel = _get_item_stats_from_json(item, 'rFlatArmorPenetrationModPerLevel'),    
                rFlatCritChanceModPerLevel = _get_item_stats_from_json(item, 'rFlatCritChanceModPerLevel'),     
                rFlatCritDamageModPerLevel = _get_item_stats_from_json(item, 'rFlatCritDamageModPerLevel'),     
                rFlatDodgeMod = _get_item_stats_from_json(item, 'rFlatDodgeMod'),      
                rFlatDodgeModPerLevel = _get_item_stats_from_json(item, 'rFlatDodgeModPerLevel'),      
                rFlatEnergyModPerLevel = _get_item_stats_from_json(item, 'rFlatEnergyModPerLevel'),     
                rFlatEnergyRegenModPerLevel = _get_item_stats_from_json(item, 'rFlatEnergyRegenModPerLevel'),    
                rFlatGoldPer10Mod = _get_item_stats_from_json(item, 'rFlatGoldPer10Mod'),      
                rFlatHPModPerLevel = _get_item_stats_from_json(item, 'rFlatHPModPerLevel'),     
                rFlatHPRegenModPerLevel = _get_item_stats_from_json(item, 'rFlatHPRegenModPerLevel'),    
                rFlatMPModPerLevel = _get_item_stats_from_json(item, 'rFlatMPModPerLevel'),     
                rFlatMPRegenModPerLevel = _get_item_stats_from_json(item, 'rFlatMPRegenModPerLevel'),    
                rFlatMagicDamageModPerLevel = _get_item_stats_from_json(item, 'rFlatMagicDamageModPerLevel'),    
                rFlatMagicPenetrationMod = _get_item_stats_from_json(item, 'rFlatMagicPenetrationMod'),      
                rFlatMagicPenetrationModPerLevel = _get_item_stats_from_json(item, 'rFlatMagicPenetrationModPerLevel'),       
                rFlatMovementSpeedModPerLevel = _get_item_stats_from_json(item, 'rFlatMovementSpeedModPerLevel'),      
                rFlatPhysicalDamageModPerLevel = _get_item_stats_from_json(item, 'rFlatPhysicalDamageModPerLevel'),     
                rFlatSpellBlockModPerLevel = _get_item_stats_from_json(item, 'rFlatSpellBlockModPerLevel'),     
                rFlatTimeDeadMod = _get_item_stats_from_json(item, 'rFlatTimeDeadMod'),       
                rFlatTimeDeadModPerLevel = _get_item_stats_from_json(item, 'rFlatTimeDeadModPerLevel'),        
                rPercentArmorPenetrationMod = _get_item_stats_from_json(item, 'rPercentArmorPenetrationMod'),    
                rPercentArmorPenetrationModPerLevel = _get_item_stats_from_json(item, 'rPercentArmorPenetrationModPerLevel'),     
                rPercentAttackSpeedModPerLevel = _get_item_stats_from_json(item, 'rPercentAttackSpeedModPerLevel'),      
                rPercentCooldownMod = _get_item_stats_from_json(item, 'rPercentCooldownMod'),    
                rPercentCooldownModPerLevel = _get_item_stats_from_json(item, 'rPercentCooldownModPerLevel'),    
                rPercentMagicPenetrationMod = _get_item_stats_from_json(item, 'rPercentMagicPenetrationMod'),    
                rPercentMagicPenetrationModPerLevel = _get_item_stats_from_json(item, 'rPercentMagicPenetrationModPerLevel'),    
                rPercentMovementSpeedModPerLevel = _get_item_stats_from_json(item, 'rPercentMovementSpeedModPerLevel'),        
                rPercentTimeDeadMod = _get_item_stats_from_json(item, 'rPercentTimeDeadMod'),    
                rPercentTimeDeadModPerLevel = _get_item_stats_from_json(item, 'rPercentTimeDeadModPerLevel'),    
            )
            if created == True:
                item.save() 
        except:
            print 'ERROR, item ID = ', item_data[item]['id']

            
        
        # for tag in list(raw_tag):
        #     item_tag, tag_created = ItemTag.objects.get_or_create(item = item, tag = tag)
        #     if tag_created == True:
        #         item_tag.save() 





              