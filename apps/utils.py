def filter_sensitive_data(data, keys_to_remove):
    if isinstance(data, dict):
        return {
            k: filter_sensitive_data(v, keys_to_remove)
            for k, v in data.items()
            if k not in keys_to_remove
        }
    elif isinstance(data, list):
        return [filter_sensitive_data(item, keys_to_remove) for item in data]
    else:
        return data
