from dataclasses import dataclass

@dataclass
class AppArguments:
    listen_host: str        = '127.0.0.1'
    listen_port: int        = 8080
    log_dir_to_save: str    = None

    def __str__(self):
        return (f"AppArguments("
            f" {self.listen_host=}"
            f", {self.listen_port=}"
            f", {self.log_dir_to_save=}"
            ")"
        )