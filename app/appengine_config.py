"""`appengine_config` gets loaded when starting a new application instance."""
import sys
import os.path

# add `vendor` subdirectory to `sys.path`, so we can load third-party libraries.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'vendor'))
