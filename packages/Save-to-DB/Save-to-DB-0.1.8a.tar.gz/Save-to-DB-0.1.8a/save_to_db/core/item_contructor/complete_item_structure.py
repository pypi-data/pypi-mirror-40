from collections import defaultdict
from .merge_items import merge_items


def complete_item_structure(item):
    """ Takes an item, completes reverse relationships inside it and
    return a dictionary like this:
    
        .. code-block:: Python
            
            {
                item_cls: [item_instance, ...],
                ...
            }
            
    Where keys are a subclasses of :py:class:`~.item.Item` and values are
    instances of that class.
    """
    structure = defaultdict(list)  # item class to a list of instances
    __add_flat_item_to_structure(item, structure)
     
    # merging items
    all_items = []
    for item_cls in structure.keys():
        if not item_cls.allow_merge_items:
            continue
        if not all_items:
            for items in structure.values():
                all_items.extend(items)
        merge_items(structure[item_cls], all_items)
     
    return structure


def __add_flat_item_to_structure(item, structure):
    
    if item.is_single_item():
        if item in structure[type(item)]:
            return
        structure[type(item)].append(item)
        
        for key, relation in item.relations.items():
            if key not in item or item[key] is None:
                continue
            
            __add_flat_item_to_structure(item[key], structure)
            
            # setting reverse relations
            reverse_key = relation['reverse_key']
            if reverse_key is None:
                continue
            
            that_item = item[key]
            is_one_to_x = relation['relation_type'].is_one_to_x()
 
            if that_item.is_single_item():
                if is_one_to_x:
                    that_item[relation['reverse_key']] = item
                else:
                    that_item[relation['reverse_key']].add(item)
            else:
                for inner_item in that_item.bulk:
                    if is_one_to_x:
                        inner_item[reverse_key] = item
                    else:
                        inner_item[reverse_key].add(item)
            
    else:
        # bulk item can be added (using this function) only once at the
        # beginning
        for inner_item in item.bulk:
            __add_flat_item_to_structure(inner_item, structure)