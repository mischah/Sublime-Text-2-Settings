import sublime
import sublime_plugin
import re


class ConsoleTimeCommand(sublime_plugin.TextCommand):

    def is_visible(self):
        return self.check_scope()

    def is_enabled(self):
        return self.check_scope()

    def check_scope(self):
        scope = self.view.scope_name(self.view.sel()[0].a)
        allowed_scopes = ['source.js', 'source.coffee']
        score = 0
        for a in allowed_scopes:
            score = score + sublime.score_selector(scope, a)
        return score > 0

    def description(self):
        return "Wrap in console.time()"

    def strip_white_space(self, region):
        contents = self.view.substr(region)
        new_begin = region.begin() + region.size() - len(contents.lstrip())
        new_end = region.begin() + len(contents.rstrip())
        return sublime.Region(new_begin, new_end)

    def get_indents(self, region):
        tab_size = self.view.settings().get('tab_size')
        lines = self.view.substr(region).splitlines()
        lines[1:-1] = []
        lines = [i[:len(i) - len(i.lstrip(' \t'))] for i in lines]
        indents = []
        for l in lines:
            l = re.sub('\t', ' ' * tab_size, l)
            l = re.sub(' {%s}' % tab_size, '\t', l)
            indents.append(l)
        if len(indents) is 1:
            indents.append(indents[0])
        return dict(zip(['first_indent', 'last_indent'], indents))

    def run(self, edit):
        for sel in self.view.sel():
            sel = self.strip_white_space(sel)
            text = self.view.substr(sel)
            text = text.replace('$', '\$')
            line = self.view.line(sel)
            text_split = self.view.substr(line)
            text_split = text_split.replace('$', '\$')
            if text:
                text_split = text_split.split(text)
            else:
                sel_pos = sel.begin() - line.begin()
                text_split = [text_split[:sel_pos], text_split[sel_pos:]]

            text = text.replace('}', '\\}')
            reps = dict(zip(['pre_text', 'post_text'], text_split))
            reps.update(text=text)
            reps.update(self.get_indents(line))

            snippet = """{first_indent}console.time('${{1:Timer Title}}');
{pre_text}${{2:{text}}}{post_text}$0
{last_indent}console.timeEnd('${{1:Timer Title}}');"""

            self.view.sel().clear()
            self.view.sel().add(line)
            snippet = snippet.format(**reps)

            self.view.run_command("insert_snippet", {"contents": snippet})
