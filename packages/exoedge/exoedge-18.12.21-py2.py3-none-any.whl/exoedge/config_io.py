# pylint: disable=W0141,W0110,C0103,W1202
"""
    ExoEdge ConfigIO module to handle Channel creation from a config_io object.
"""
import inspect
import time
from exoedge.configs import ExoEdgeConfig
from exoedge import logger
from exoedge.sources import ExoEdgeClassicSource, ExoEdgeSource
from exoedge.namespaces import get_nested_object
from exoedge.channel import Channel, DataOutChannel
from exoedge.constants import DEFAULTS

LOG = logger.getLogger(__name__)


class ConfigIO(ExoEdgeConfig, object):
    """
    This class provides methods to create channels from a
    config_io and to format the data_in object to be sent
    to Murano.

    Required Inputs:
        device: a murano_client.client.Client() object
                for the connection to Murano.

    Optional Inputs:
        config:         a config_io object (dictionary).
        config_io_file: path to a JSON file containing
                        the config_io object.
        wait_timeout:   timeout, in seconds, between
                        printing 'no new config' to
                        the log (default:1.0).

    """
    resource = 'config_io'
    def __init__(self, **kwargs):
        ExoEdgeConfig.__init__(
            self,
            name="ConfigIO",
            device=kwargs.get('device'),
            config_file=kwargs.get(
                'config_io_file',
                DEFAULTS['config_io_file']
            )
        )
        self.wait_timeout = float(kwargs.get('wait_timeout', 1.0))
        self.set_config(kwargs.get('config'))
        # schema: {"$channel_id": <Channel instance>}
        self.channels = {}
        # schema: {"$source_name": {"source": <Source instance>, "channels": [ch1, chN]}}
        self.sources = {}

    def stop(self):
        """ Stop all activity.

        Stops activity of all Channel threads, Channel-
        Watcher threads, and the ConfigIO thread.
        """
        LOG.warning("Stopping ConfigIO...")
        self.stop_all_sources()
        super(ConfigIO, self).stop()

    def add_channel(self, name, ch_cfg):
        """ Create Channel and DataOutChannel objects.

        Create a Channels and DataOutChannels from a channel
        configuration object. Store them in the ConfigIO.channels
        dictionary.

        Parameters:
        name:       the key of the ch_cfg object in config_io
        ch_cfg:     the object representation of the channel
                    taken from config_io.

        """
        LOG.info(
            'Adding channel: {}'
            .format(name)
        )
        ch_cfg['name'] = name
        if get_nested_object(ch_cfg, ['properties', 'data_out']):
            self.channels[name] = DataOutChannel(**ch_cfg)
        else:
            self.channels[name] = Channel(**ch_cfg)
        return self.channels[name]

    @classmethod
    def is_proper_source(cls, source):
        """
            Checks source objects to ensure they're
            a subclass of ExoEdgeSource.
        """
        return isinstance(source, ExoEdgeSource)

    def add_source(self, channel):
        """
            ExoEdgeSource Rules:
             - protocol_config.application
               name/import rules
             - programming rules

            0.  Sources must subclass exoedge.sources.ExoEdgeSource.
            1.  Lowercased, the module name must be
                prefixed by "exoedge_".
            2.  Titlecased, the class name must be
                suffixed by "ExoEdgeSource".
            3.  Modbus_TCP and _RTU are the exception,
                they get stripped to just Modbus.
            4. Source class name must not be "ExoEdgeSource".

            i.e.
                CANOpen -> exoedge_canopen.CanopenExoEdgeSource
                Modbus_TCP -> exoedge_modbus.ModbusExoEdgeSource
                Phidgets -> exoedge_phidgets.PhidgetsExoEdgeSource
        """
        application = channel.protocol_config.application
        if application.startswith(u'Modbus_'):
            application = "Modbus"

        if application == "ExoSimulator":
            module_name = "exoedge.sources.exo_simulator"
            class_name = application
        else:

            # e.g. exoedge_modbus, exoedge_canopen, etc.
            module_name = "exoedge_" + application.lower()
            # e.g. ModbusExoEdgeSource, CanopenExoEdgeSource, etc.
            class_name = application.lower().capitalize() + "ExoEdgeSource"

        # e.g. exoedge_modbus.ModbusExoEdgeSource,
        #      exoedge_canopen.CanopenExoEdgeSource,
        #      exoedge.sources.exo_simulator.ExoSimulator
        #      etc.
        source_name = '.'.join([module_name, class_name])

        # if source already loaded, append channel and return
        loaded_source = self.sources.get(source_name)
        if loaded_source and self.is_proper_source(loaded_source["source"]):
            LOG.warning(
                "Source '{}' already loaded."
                .format(loaded_source)
            )
            self.sources[source_name]["channels"].append(channel)
            # keep reference to source in channel object
            channel.source = self.sources[source_name]["source"]
            return

        LOG.critical(
            "Loading module {}..."
            .format(module_name)
        )
        try:
            module = __import__(module_name)
        except Exception as exc:
            module = None
            LOG.error(
                "Unable to import module {}: {}"
                .format(module_name, exc)
            )
        if module:
            LOG.warning("Imported module: {}".format(module))
            if hasattr(module, class_name):
                Klass = getattr(module, class_name)
                if inspect.isclass(Klass):

                    # check Klass against rules in docstring
                    is_proper_class = issubclass(Klass, ExoEdgeSource) \
                                      and \
                                      class_name != 'ExoEdgeSource'

                    if is_proper_class:
                        # create instance or just add a channel to existing one
                        if not self.sources.get(source_name):
                            LOG.critical(
                                "Creating instance: {}..."
                                .format(source_name + '()')
                            )
                            # create source
                            self.sources[source_name] = {
                                "source": Klass(),
                                "channels": [channel]
                            }
                            # keep reference to source in channel object
                            channel.source = self.sources[source_name]["source"]

            # TODO: EXOEDGE-203
            elif application == "ExoSimulator":
                # create instance or just add a channel to existing one
                if not self.sources.get(source_name):
                    LOG.critical(
                        "Creating instance: {}..."
                        .format(source_name + '()')
                    )
                    # create source
                    self.sources[source_name] = {
                        "source": module.sources.exo_simulator.ExoSimulator(),
                        "channels": [channel]
                    }
                    # keep reference to source in channel object
                    channel.source = self.sources[source_name]["source"]
            else:
                LOG.error(
                    "Unable to find source: {}. Putting channel {} in error."
                    .format(source_name, channel)
                )
                channel.put_channel_error(
                    "Unable to load source: {}"
                    .format(source_name)
                )

        # check to see if we've successfully loaded a source for the given channel
        loaded_source = self.sources.get(source_name)
        if loaded_source and self.is_proper_source(loaded_source["source"]):
            LOG.critical(
                "Created source instance:: {}"
                .format(loaded_source)
            )
        else:
            # if we've made it here we tried to find an installed ExoEdgeSource
            # but didn't find any so now try to see if we can run the channel
            # in classic style
            LOG.critical(
                "no supported source found. trying classic module.function(*args, **kwargs) style.")
            module_name = channel.protocol_config.app_specific_config.get('module')
            function_name = channel.protocol_config.app_specific_config.get('function')
            source_name = "ExoEdgeClassicSource->" + channel.name
            try:
                module = __import__(module_name)
            except Exception as exc:
                module = None
                error_msg = "Unable to import module {}: {}".format(module_name, exc)
                LOG.error(error_msg)
                channel.put_channel_error(error_msg)
                return

            if not hasattr(module, function_name):
                error_msg = "Module {} has no function: {}".format(module_name, function_name)
                LOG.error(error_msg)
                channel.put_channel_error(error_msg)
                return

            if not self.sources.get(source_name):
                self.sources[source_name] = {"source": None, "channels": []}

            self.sources[source_name]["source"] = ExoEdgeClassicSource(
                channel,
                getattr(module, function_name)
            )
            self.sources[source_name]["channels"].append(channel)
            # keep reference to source in channel object
            channel.source = self.sources[source_name]["source"]

    def stop_all_sources(self):
        """ Stop ExoEdge sources.

            Call source.stop_source() for all sources.
            Called by self.run() when a new config is received.
        """
        LOG.warning('Stopping all sources!')
        for source_name in self.sources:
            source = self.sources[source_name].get("source")
            if source:
                LOG.warning(
                    "Stopping source: {}"
                    .format(source)
                )
                source.stop_source()
                if isinstance(source, ExoEdgeSource):
                    source.join(0.5)
                elif isinstance(source, ExoEdgeClassicSource):
                    # wait for one interval for graceful shutdown
                    time.sleep(source.interval)
                else:
                    LOG.critical(
                        "Don't know how to stop source: <({} ){}>"
                        .format(type(source), source)
                    )

        self.sources = {}
        self.channels = {}

    def run(self):
        """
        Update ConfigIO and Channels upon new config(s).

         - Waits for a new config_io event set by ConfigIO.set_config().
         - Stops existing sources, deletes channels before creating new ones
           based on received config object(s).
         - Starts Channels and Sources.
        """
        LOG.debug('starting')
        while not self.is_stopped():
            if self.event_new_config.wait(self.wait_timeout):
                with self._lock:
                    if self.config:
                        LOG.debug('Received config_io')

                        if self.sources:
                            self.stop_all_sources()

                        if 'channels' in self.config.keys():
                            for name, cfg in self.config['channels'].items():
                                self.add_channel(name, cfg)
                            for channel in self.channels.values():
                                self.add_source(channel)

                        # start all sources
                        LOG.info("Loaded sources: {}".format(self.sources))
                        for source in self.sources:
                            LOG.warning("STARTING SOURCE: {}".format(source))
                            self.sources[source]["source"].start_source()

                        LOG.critical("Running sources: {}".format(self.sources))
                    else:
                        LOG.info("No new config_io received.")
                self.event_new_config.clear()

            else:
                LOG.debug('no new config')
        LOG.debug('exiting')


