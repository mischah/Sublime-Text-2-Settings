import sublime
import sublime_plugin
import urllib


ST3 = sublime.version() == '' or int(sublime.version()) > 3000


def get_current_encoding(view, default='utf8'):
    """Get the encoding of view, else return default
    """
    view_encoding = view.encoding()
    if view_encoding == 'Undefined':
        view_encoding = view.settings().get('default_encoding', default)

    br1 = view_encoding.find('(')
    br2 = view_encoding.find(')')
    if br2 > br1:
        view_encoding = view_encoding[br1+1:br2].replace(' ', '-')

    return view_encoding


def selections(view, default_to_all=True):
    """Return all non-empty selections in view
    If None, return entire view if default_to_all is True
    """
    regions = [r for r in view.sel() if not r.empty()]

    if not regions and default_to_all:
        regions = [sublime.Region(0, view.size())]

    return regions


if ST3:

    def quote(view, s):
        return urllib.parse.quote(s)

    def unquote(view, s):
        return urllib.parse.unquote(s)

else:
    # py26 urllib does not quote unicode, so encode first

    def quote(view, s):
        enc = get_current_encoding(view)
        return urllib.quote(s.encode(enc))

    def unquote(view, s):
        settings = sublime.load_settings('URLEncode.sublime-settings')
        fallback_encodings = settings.get('fallback_encodings', [])
        fallback_encodings.insert(0, get_current_encoding(view))

        s = urllib.unquote(s.encode('utf8'))

        ## Now decode (to unicode) using best guess encoding
        for enc in fallback_encodings:
            try:
                return s.decode(enc)
            except UnicodeDecodeError:
                continue
        return s



class UrlencodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        """Main plugin logic for the 'urlencode' command.
        """
        view = self.view
        for region in selections(view):
            s = view.substr(region)
            view.replace(edit, region, quote(view, s))


class UrldecodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        """Main plugin logic for the 'urldecode' command.
        """
        view = self.view
        for region in selections(view):
            s = view.substr(region)
            view.replace(edit, region, unquote(view, s))
