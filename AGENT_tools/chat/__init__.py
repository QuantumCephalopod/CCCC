"""Import helpers for chat context."""

from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

FILE = Path(__file__).with_name('o.chat.py')
loader = SourceFileLoader('ochat', str(FILE))
spec = spec_from_loader('ochat', loader)
module = module_from_spec(spec)
loader.exec_module(module)

append_entry = module.append_entry
show_history = module.show_history
CHAT_FILE = module.CHAT_FILE
