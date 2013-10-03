import sublime, sublime_plugin

class FindResourceCommand(sublime_plugin.WindowCommand):
    def run(self):
        resources = sublime.find_resources('*')
        def on_done(index):
            if index >= 0:
                resource_name = resources[index]
                try:
                    content = sublime.load_resource(resource_name)
                    binary = False
                except UnicodeDecodeError:
                    content = sublime.load_binary_resource(resource_name)
                    binary = True

                scratch_file = self.window.new_file()
                scratch_file.set_name(resource_name)
                scratch_file.set_scratch(True)
                if not binary:
                    scratch_file.assign_syntax("Packages/Text/Plain text.tmLanguage") # FIXME: Choose proper syntax
                    scratch_file.run_command('find_resource_scratch_output', {"content": content})
                else:
                    scratch_file.set_encoding('Hexadecimal')
                    scratch_file.run_command('find_resource_scratch_output', {"content": self.bytearray_to_string(content)})
                scratch_file.set_read_only(True)

        self.window.show_quick_panel(resources, on_done, sublime.MONOSPACE_FONT, -1, None)

    def bytearray_to_string(self, bytearray):
        return ' '.join('%02x' % byte for byte in bytearray) # FIXME: Improve to be same style as the general in Sublime Text

class FindResourceScratchOutputCommand(sublime_plugin.TextCommand):
    def run(self, edit, content = ''):
        self.view.insert(edit, 0, content)
