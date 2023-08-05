"""
    An ExoEdge source that provided convenient access to system information and resources.

    An example of enabling all of the functions in this module:

    config_io:
    {
      "channels": {
        "architecture": {
          "display_name": "Processor Architecture",
          "description": "The Processor Architecture of the gateway.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": true,
            "app_specific_config": {
              "function": "architecture",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        },
        "machine_type": {
          "display_name": "Machine Type",
          "description": "The Machine Type of the gateway.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": true,
            "app_specific_config": {
              "function": "machine_type",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        },
        "system_platform": {
          "display_name": "System Platform",
          "description": "The System Platform of the gateway.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": true,
            "app_specific_config": {
              "function": "system_platform",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        },
        "python_version": {
          "display_name": "Python Version",
          "description": "The Python Version of the gateway.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": true,
            "app_specific_config": {
              "function": "python_version",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        },
        "whoami": {
          "display_name": "Current User",
          "description": "The Current User of the edged process.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": true,
            "app_specific_config": {
              "function": "whoami",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        },
        "net_io": {
          "display_name": "NetIO",
          "description": "Network statistics of the gateway.",
          "properties": {
            "data_type": "JSON"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": false,
            "sample_rate": 30000,
            "report_rate": 30000,
            "app_specific_config": {
              "function": "net_io",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        },
        "disk_stats": {
          "display_name": "Disk Stats",
          "description": "Disk usage statistics of the gateway.",
          "properties": {
            "data_type": "JSON"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": false,
            "sample_rate": 30000,
            "report_rate": 30000,
            "app_specific_config": {
              "function": "disk_stats",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        },
        "cpu_times_percent": {
          "display_name": "CPU Stats",
          "description": "CPU usage statistics of the gateway.",
          "properties": {
            "data_type": "JSON"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": false,
            "sample_rate": 30000,
            "report_rate": 30000,
            "app_specific_config": {
              "function": "cpu_times_percent",
              "module": "exo_simulator",
              "parameters": {
                "interval": 1
              },
              "positionals": []
            }
          }
        },
        "exoedge_version": {
          "display_name": "ExoEdge Version",
          "description": "The ExoEdge Version running on the gateway.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": true,
            "app_specific_config": {
              "function": "exoedge_version",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        }
      }
    }

"""
# pylint: disable=W1202,C0111
import time
import threading
import platform as _platform
import sys as _sys
import getpass as _getpass
import json
import threading
import psutil as _psutil
from exoedge.sources import ExoEdgeSource
from exoedge import __version__


def architecture():
    """
        Get the system architecture.

    config_io:
    {
      "channels": {
        "architecture": {
          "display_name": "Processor Architecture",
          "description": "The Processor Architecture of the gateway.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": true,
            "app_specific_config": {
              "function": "architecture",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        }
      }
    }
    """
    tmp = _platform.architecture()
    if isinstance(tmp, tuple):
        depth = tmp[0]
    else:
        depth = tmp
    return depth

def machine_type():
    """
        Get the machine type.

    config_io:
    {
      "channels": {
        "machine_type": {
          "display_name": "Machine Type",
          "description": "The Machine Type of the gateway.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": true,
            "app_specific_config": {
              "function": "machine_type",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        }
      }
    }
    """
    return _platform.machine()

def system_platform():
    """
        Get the machine platform info.

    config_io:
    {
      "channels": {
        "system_platform": {
          "display_name": "Platform",
          "description": "The Platform of the gateway.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": true,
            "app_specific_config": {
              "function": "system_platform",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        }
      }
    }
    """
    return _platform.platform()

def python_version():
    """
        Get the version of Python currently in use.

    config_io:
    {
      "channels": {
        "python_version": {
          "display_name": "Python Version",
          "description": "The Python Version of the gateway.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": true,
            "app_specific_config": {
              "function": "python_version",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        }
      }
    }
    """
    return _platform.python_version()

def whoami():
    """
        Get the current user.

    config_io:
    {
      "channels": {
        "whoami": {
          "display_name": "Current User",
          "description": "The Current User of the edged process.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": true,
            "app_specific_config": {
              "function": "whoami",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        }
      }
    }
    """
    return _getpass.getuser()

def net_io():
    """
        Get usage statistics on all system net interfaces.

    config_io:
    {
      "channels": {
        "net_io": {
          "display_name": "NetIO",
          "description": "Network statistics of the gateway.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": false,
            "sample_rate": 30000,
            "report_rate": 30000,
            "app_specific_config": {
              "function": "net_io",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        }
      }
    }
    """
    payload = {}
    ioc = _psutil.net_io_counters(pernic=True)
    for iface in ioc:
        if not payload.get(iface):
            payload[iface] = {}
        for elem in dir(ioc[iface]):
            if not elem.startswith('_'):
                if hasattr(ioc[iface], elem):
                    attr = getattr(ioc[iface], elem)
                    if callable(attr):
                        pass
                    else:
                        payload[iface][elem] = attr
                elif hasattr(ioc[iface], '__dict__') and ioc[iface].__dict__.get(elem):
                    payload[iface][elem] = ioc[iface].__dict__[elem]
    return payload

def disk_stats():
    """
        Get current usage on all mountpoints.

    config_io:
    {
      "channels": {
        "disk_stats": {
          "display_name": "Disk Stats",
          "description": "Disk usage statistics of the gateway.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": false,
            "sample_rate": 30000,
            "report_rate": 30000,
            "app_specific_config": {
              "function": "disk_stats",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        }
      }
    }
    """
    payload = {}
    mountpoints = [p.mountpoint for p in _psutil.disk_partitions()]
    for _mp in mountpoints:
        usage = _psutil.disk_usage(_mp)
        if not payload.get(_mp):
            payload[_mp] = {}
        for elem in dir(usage):
            if not elem.startswith('_'):
                if hasattr(_mp, elem):
                    attr = getattr(_mp, elem)
                    if callable(attr):
                        pass
                    else:
                        payload[_mp][elem] = attr
                elif hasattr(usage, '__dict__') and usage.__dict__.get(elem):
                    payload[_mp][elem] = usage.__dict__[elem]
    return payload

def cpu_times_percent(interval=1):
    """
        Get info about the cpu usage per interval (in seconds).

    config_io:
    {
      "channels": {
        "cpu_times_percent": {
          "display_name": "CPU Stats",
          "description": "CPU usage statistics of the gateway.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": false,
            "sample_rate": 30000,
            "report_rate": 30000,
            "app_specific_config": {
              "function": "cpu_times_percent",
              "module": "exo_simulator",
              "parameters": {
                "interval": 1
              },
              "positionals": []
            }
          }
        }
      }
    }
    """
    cpus = _psutil.cpu_times_percent(interval=interval, percpu=True)
    payload = {}
    cpunum = 0
    for cpu in cpus:
        cpunum += 1
        if not payload.get(cpu):
            payload[cpunum] = {}
        for elem in dir(cpu):
            if not elem.startswith('_'):
                if hasattr(cpu, elem):
                    attr = getattr(cpu, elem)
                    if callable(attr):
                        pass
                    else:
                        payload[cpunum][elem] = attr
                elif hasattr(cpu, '__dict__') and cpu.__dict__.get(elem):
                    payload[cpunum][elem] = cpu.__dict__[elem]

    return payload

def exoedge_version():
    """
        Get the current version of ExoEdge.

    config_io:
    {
      "channels": {
        "exoedge_version": {
          "display_name": "ExoEdge Version",
          "description": "The ExoEdge Version running on the gateway.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": true,
            "app_specific_config": {
              "function": "exoedge_version",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        }
      }
    }
    """
    return __version__

def machine_info():
    """
        Get human readable info on the target machine.

    config_io:
    {
      "channels": {
        "machine_info": {
          "display_name": "Machine Info",
          "description": "Basic info about the gateway.",
          "properties": {
            "data_type": "STRING"
          },
          "protocol_config": {
            "application": "ExoSimulator",
            "report_on_change": true,
            "app_specific_config": {
              "function": "machine_info",
              "module": "exo_simulator",
              "parameters": {},
              "positionals": []
            }
          }
        }
      }
    }
    """
    return '\n'.join([
        system_platform(),
        machine_type(),
        python_version(),
        whoami(),
    ])

