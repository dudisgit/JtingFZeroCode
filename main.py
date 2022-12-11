import logging
import os
import argparse
import commentjson

from UserConfig import UserConfig

LOGGING_FORMAT = "%(asctime)s [%(levelname)s]: %(message)s"
LOGGING_LEVELS = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warn": logging.WARNING,
    "error": logging.ERROR
}

def parse_arguments() -> argparse.Namespace:
    """ Creates an argument parser and parses the command line arguments
    
    Returns:
        argparse.Namespace: The namespace object generated from argparse
    """
    parser = argparse.ArgumentParser("JtingF zerogen")

    parser.add_argument("-config", type=str, default=os.path.join(os.path.dirname(__file__), "config.jsonc"),
        help="The json configuration file to load for the application")
    
    parser.add_argument("-simulate", action="store_true",
        help="Launch a simulator instead of interfacing with the real hardware")
    
    parser.add_argument("-loglevel", type=str, default="debug", choices=list(LOGGING_LEVELS),
        help="The logging level to run the application in")
    
    parser.add_argument("-resetconfig", action="store_true",
        help="Wipes the user configuration and saves a default empty one")
    
    return parser.parse_args()


def main(args:argparse.Namespace):
    """ Main entry point for the zerogen application

    Args:
        args: The parsed arguments from the argument parser function
    """
    logging.basicConfig(
        format=LOGGING_FORMAT,
        level=LOGGING_LEVELS.get(args.loglevel.lower(), logging.NOTSET)
    )
    
    logging.debug(f"Loading json configuration file at {args.config}")
    with open(args.config, "rb") as jfile:
        config = commentjson.load(jfile)
    
    userConfig = UserConfig(config["UserConfig"])
    if not os.path.exists(config["UserConfig"]):
        logging.info("UserConfig doesn't exist, creating a blank")
        userConfig.save_userconfig()

    if args.resetconfig:
        if input("Are you sure you want to reset the user config? (yes|no): ").lower() == "yes":
            logging.warning("Saving an empty user configuration")
            userConfig.save_userconfig()
    
    userConfig.load_userconfig()



if __name__ == "__main__":
    arguments = parse_arguments()
    main(arguments)
