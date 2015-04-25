"""Plugin registration."""
import inspect

plugin_blocks = {}


def plugin_block(key):
    """Register a plugin block for the given key."""
    def inner_plugin_block(callback):
        # This is an ugly hack to check if the plugin is enabled..
        parent_file_path = inspect.getouterframes(
            inspect.currentframe())[1][1]
        # Remove the last part(the file)
        parent_file_path = ".".join(parent_file_path.rsplit("/")[:-1])
        plugin_id = 'plugins.%s' % parent_file_path.split(".plugins.")[1]

        if key not in plugin_blocks:
            plugin_blocks[key] = []
        plugin_blocks[key].append((plugin_id, callback))
        return callback
    return inner_plugin_block


def plugin_enabled(plugin_id):
    """True if the plugin is enabled."""
    from admin.models import PluginSetting
    setting = PluginSetting.objects.filter(plugin_name=plugin_id).first()
    if not setting:
        return False
    return setting.enabled