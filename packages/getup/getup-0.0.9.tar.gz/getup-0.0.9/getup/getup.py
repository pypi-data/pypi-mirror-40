#!/usr/bin/env python3

import os
import sys
import json
import environ
import pathlib


BASE_DIR = pathlib.Path(os.environ.get("OLDPWD"))
sys.path.append(str(BASE_DIR.absolute()))


def path_import(importable_module_path):
    import importlib

    path, var = importable_module_path.rsplit(".", 1)
    imported = importlib.import_module(path)
    return (imported, getattr(imported, var))


def manual_setup(conf):
    """
  If configuration is meant to happen from scripts &c
  conf is supposed to be dictionary to override defaults
  """
    from django.conf import settings

    if not settings.configured:
        settings.configure(**conf)
        import django

        django.setup()


def env_setup(conf):
    # Convenience for some environment settings
    env = environ.Env(
        DEBUG=(bool, conf.get("DEBUG")),
        SECRET_KEY=(str, conf.get("SECRET_KEY")),
        ALLOWED_HOSTS=(list, []),
        DATABASE_URL=(str, "postgres:///pakastin"),
        SENTRY_DSN=(str, ""),
    )
    environ.Env.read_env()
    conf.update(
        dict(
            DEBUG=env("DEBUG"),
            ALLOWED_HOSTS=env("ALLOWED_HOSTS"),
            DATABASES={"default": env.db()},
            # Well you need to keep some secrets,
            SECRET_KEY=env("SECRET_KEY"),
        )
    )

    # Wish this was simpler
    if env("SENTRY_DSN"):
        conf["RAVEN_CONFIG"] = {
            "dsn": env("SENTRY_DSN"),
            "release": raven.fetch_git_sha(BASE_DIR),
        }
        conf["INSTALLED_APPS"].append("raven.contrib.django.raven_compat")


def json_conf(confpath):
    # Set everything with one conf file created by Jsonnet perhaps
    if not confpath:
        confpath = pathlib.Path(".").absolute().joinpath("conf.json")
    else:
        confpath = pathlib.Path(confpath)

    conf = json.load(open(confpath))

    # Simple defaults if no one has any apps
    conf.setdefault("INSTALLED_APPS", [])

    return conf, confpath


def env_conf(conf):
    if os.environ.get("GETUP_READ_ENV"):
        env_setup(conf)


def py_conf(confpath):
    app, var = path_import(confpath)
    app_root = app.__file__
    return var, pathlib.Path(app_root)


def create_url_patterns(paths):
    """
    For given iterable of url, module path pairs creates urlpatterns
    Imports given path's package and uses path's last part as the view callable
    This allows defining URL patterns using JSON.
    """
    from django.urls import path

    urlpatterns = (
        path(url, path_import(importable_module_path)[0])
        for url, importable_module_path in paths
    )
    return tuple(urlpatterns)


COMBINER_CONFIG = """
    local basic = import "conf.jsonnet";
    basic.conf(
        urls=std.extVar("urls"), 
        debug=std.extVar("debug"), 
        secret_key=std.extVar("secret_key"), 
        apps=std.extVar("apps"),
        allowed_hosts=std.extVar("allowed_hosts")
        ) + std.extVar("extra")
"""


def combine_config(conf, base_conf="conf.jsonnet"):
    """
    Creates JSON config from given Python dict and Jsonnet base config
    Use dictionary such as this:
        dict(
            apps=["APPNAME"]
            debug=True, 
            secret_key="hoh",
            allowed_hosts=["localhost"]
            extra={"MYCONFIG":"MYVALUE"},
        )
    Apps, debug, secret_key and allowed_hosts are kind of important
    so setting them is mandatory 
    """
    import _jsonnet
    
    conf["base_conf"] = conf.get("base_conf", base_conf) # conf might have its own base_conf

    convert = lambda arg: {k: json.dumps(v) for k, v in arg.items()}
    conf = convert(conf)
    
    if not conf.get("extra"):
        conf["extra"] = "{}" # extVar doesn't like missing things
    config = _jsonnet.evaluate_snippet(
        "snip", COMBINER_CONFIG, 
        ext_codes=conf
    )
    return config


def main():
    import sys
    
    confpath = os.environ.get("GETUP_CONF_PATH")
    if confpath.endswith(".json"):
        # Conf is JSON and its location is app root
        conf, app_root = json_conf(confpath)
    else:
        # Now path is expected to be package path to Python dict
        conf, app_root = py_conf(confpath)
    
    # Required for app_root being importable
    sys.path.append(str(app_root.absolute().parent))
    
    # Make app folder importable by name
    sys.path.append(str(app_root.absolute().parent.parent))

    # Urlpattern conversion for arbitrary view functions
    if conf.get("urlpatterns"):
        conf["ROOT_URLCONF"] = create_url_patterns(conf.get("urlpatterns"))
    
    # Support environment variables
    env_conf(conf)
    
    # Configure Django 
    manual_setup(conf)

    from django.conf import settings

    from django.core.management import execute_from_command_line

    # Delegate to Django management
    execute_from_command_line(sys.argv)
