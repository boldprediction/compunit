from hubs.confighub import ConfigHub


class Main:

    def start(self):
        config_hub = ConfigHub()
        print(config_hub.config)


if __name__ == "__main__":
    Main().start()
