import sublime
import traceback
import os
import sys
import time
import imp
import re

settings = sublime.load_settings('SFTP.sublime-settings')

if sublime.platform() == 'linux' and settings.get('linux_enable_ssl'):
    print 'SFTP: enabling custom linux ssl module'
    arch_lib_path = os.path.join(sublime.packages_path(), 'SFTP', 'lib',
        'linux-' + sublime.arch())
    for ssl_ver in ['0.9.8', '1.0.0', '10']:
        lib_path = os.path.join(arch_lib_path, 'libssl-' + ssl_ver)
        try:
            m_info = imp.find_module('_ssl', [lib_path])
            m = imp.load_module('_ssl', *m_info)
            print 'SFTP: successfully loaded _ssl module for libssl.so.%s' % ssl_ver
            break
        except (ImportError) as (e):
            print 'SFTP: _ssl module import error - ' + str(e)
    if '_ssl' in sys.modules:
        plat_lib_path = os.path.join(sublime.packages_path(), 'SFTP', 'lib',
            'linux')
        try:
            m_info = imp.find_module('ssl', [plat_lib_path])
            m = imp.load_module('ssl', *m_info)
        except (ImportError) as (e):
            print 'SFTP: ssl module import error - ' + str(e)

reloading = {
    'happening': False,
    'shown': False
}

reload_mods = []
for mod in sys.modules:
    if (mod[0:5] == 'sftp.' or mod == 'sftp') and sys.modules[mod] != None:
        reload_mods.append(mod)
        reloading['happening'] = True

# Prevent popups during reload, saving the callbacks for re-adding later
if reload_mods:
    old_callbacks = {}
    hook_match = re.search("<class '(\w+).ExcepthookChain'>", str(sys.excepthook))
    if hook_match:
        _temp = __import__(hook_match.group(1), globals(), locals(),
            ['ExcepthookChain'], -1)
        ExcepthookChain = _temp.ExcepthookChain
        old_callbacks = ExcepthookChain.names
    sys.excepthook = sys.__excepthook__

mods_load_order = [
    'sftp',
    'sftp.times',
    'sftp.views',
    'sftp.paths',
    'sftp.debug',
    'sftp.errors',
    'sftp.threads',
    'sftp.secure_input',
    'sftp.proc',
    'sftp.vcs',
    'sftp.config',
    'sftp.panel_printer',
    'sftp.file_transfer',
    'sftp.ftplib2',
    'sftp.ftp_transport',
    'sftp.ftps_transport',
    'sftp.sftp_transport',
    'sftp.commands',
    'sftp.listeners'
]

for mod in mods_load_order:
    if mod in reload_mods:
        reload(sys.modules[mod])

from sftp.commands import (SftpShowPanelCommand, SftpCreateServerCommand,
    SftpBrowseServerCommand, SftpLastServerCommand, SftpEditServerCommand,
    SftpDeleteServerCommand, SftpBrowseCommand, SftpUploadFileCommand,
    SftpMonitorFileCommand, SftpUploadOpenFilesCommand,
    SftpDiffRemoteFileCommand, SftpRenameLocalAndRemotePathsCommand,
    SftpDeleteRemotePathCommand, SftpDownloadFileCommand,
    SftpUploadFolderCommand, SftpSyncUpCommand, SftpSyncDownCommand,
    SftpSyncBothCommand, SftpDownloadFolderCommand, SftpVcsChangedFilesCommand,
    SftpCancelUploadCommand, SftpEditConfigCommand, SftpCreateConfigCommand,
    SftpCreateSubConfigCommand, SftpThread,
    SftpDeleteLocalAndRemotePathsCommand, SftpSwitchConfigCommand,
    SftpCreateAltConfigCommand)
from sftp.listeners import (SftpCloseListener, SftpLoadListener,
    SftpFocusListener, SftpAutoUploadListener, SftpAutoConnectListener)

import sftp.debug
import sftp.paths
import sftp.times

sftp.debug.set_debug(settings.get('debug', False))


hook_match = re.search("<class '(\w+).ExcepthookChain'>", str(sys.excepthook))

if not hook_match:
    class ExcepthookChain(object):
        callbacks = []
        names = {}

        @classmethod
        def add(cls, name, callback):
            if name == 'sys.excepthook':
                if name in cls.names:
                    return
                cls.callbacks.append(callback)
            else:
                if name in cls.names:
                    cls.callbacks.remove(cls.names[name])
                cls.callbacks.insert(0, callback)
            cls.names[name] = callback

        @classmethod
        def hook(cls, type, value, tb):
            for callback in cls.callbacks:
                callback(type, value, tb)

        @classmethod
        def remove(cls, name):
            if name not in cls.names:
                return
            callback = cls.names[name]
            del cls.names[name]
            cls.callbacks.remove(callback)
else:
    _temp = __import__(hook_match.group(1), globals(), locals(),
        ['ExcepthookChain'], -1)
    ExcepthookChain = _temp.ExcepthookChain


# Override default uncaught exception handler
def sftp_uncaught_except(type, value, tb):
    message = ''.join(traceback.format_exception(type, value, tb))

    if message.find('/sftp/') != -1 or message.find('\\sftp\\') != -1:
        def append_log():
            log_file_path = os.path.join(sublime.packages_path(), 'User',
                'SFTP.errors.log')
            send_log_path = log_file_path
            timestamp = sftp.times.timestamp_to_string(time.time(),
                    '%Y-%m-%d %H:%M:%S\n')
            with open(log_file_path, 'a') as f:
                f.write(timestamp)
                f.write(message)
            if sftp.debug.get_debug() and sftp.debug.get_debug_log_file():
                send_log_path = sftp.debug.get_debug_log_file()
                sftp.debug.debug_print(message)
            sublime.error_message(('%s: An unexpected error occurred, ' +
                'please send the file %s to support@wbond.net') % ('SFTP',
                send_log_path))
            sublime.active_window().run_command('open_file',
                {'file': sftp.paths.fix_windows_path(send_log_path)})
        if reloading['happening']:
            if not reloading['shown']:
                sublime.error_message('SFTP: Sublime SFTP was just upgraded' +
                    ', please restart Sublime to finish the upgrade')
                reloading['shown'] = True
        else:
            sublime.set_timeout(append_log, 10)

if reload_mods and old_callbacks:
    for name in old_callbacks:
        ExcepthookChain.add(name, old_callbacks[name])

ExcepthookChain.add('sys.excepthook', sys.__excepthook__)
ExcepthookChain.add('sftp_uncaught_except', sftp_uncaught_except)

if sys.excepthook != ExcepthookChain.hook:
    sys.excepthook = ExcepthookChain.hook


def unload_handler():
    SftpThread.cleanup()

    ExcepthookChain.remove('sftp_uncaught_except')
