import re

import sublime
import sublime_plugin

class HexToRgbCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for selection in self.view.sel():
            word_region = self.view.word(selection)
            if not word_region.empty():
                rgb_css = self.convert_to_rgb_css(word_region)
                if rgb_css:
                    if (self.view.substr(word_region.begin()-1) == "#"):
                        tmp_region = sublime.Region(word_region.begin()-1, word_region.end())
                        self.view.replace(edit, tmp_region, rgb_css)
                    elif (self.view.substr(word_region.begin()) == "#"):
                        tmp_region = sublime.Region(word_region.begin(), word_region.end())
                        self.view.replace(edit, tmp_region, rgb_css)

    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        if len(value) == 3:
            value = ''.join([v*2 for v in list(value)])
        return tuple(int(value[i:i+2], 16) for i in range(0, 6, 2))

    def convert_to_rgb_css(self, word_region):
        word = self.view.substr(word_region)
        re_hex_color = re.compile('#?([0-9a-fA-F]{3}([0-9a-fA-F]{3})?){1}$')
        if re_hex_color.match(word):
            rgb = self.hex_to_rgb(word)
            rgb_css = 'rgb(%s, %s, %s)' % rgb
            return rgb_css
        return False
