import argparse

from tools.userconfig_editor.ConfigEditorWindow import ConfigEditorWindow


def main():
    parser = argparse.ArgumentParser("Tool launcher")

    parser.add_argument("-config_editor", action="store_true",
        help="Launches the user config editor UI tool")
    

    args = parser.parse_args()

    if args.config_editor:
        app = ConfigEditorWindow()
        app.mainloop()


if __name__ == "__main__":
    main()
