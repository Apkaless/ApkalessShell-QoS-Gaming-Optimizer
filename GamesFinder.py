import psutil
import os
import re

"""
Currently, support is only available for Epic Games and Steam.
"""


class Steam:
    """
    A class to locate the Steam Launcher installation directory.
    """

    def __init__(self):
        pass

    def find_steam(self):
        all_partitions = [partiotion.device for partiotion in psutil.disk_partitions(all=False)]

        possible_paths = [(os.path.join(partition, 'Program Files (x86)', 'Steam'),
                           os.path.join(partition, 'Program Files', 'Steam'),
                           os.path.join(partition, 'Steam'),
                           os.path.join(partition, 'Games', 'Steam'),
                           os.path.join(partition, 'My Programs', 'Steam'),
                           os.path.join(partition, 'Launchers', 'Steam'),
                           os.path.join(partition, 'Launcher', 'Steam'),
                           os.path.join(partition, 'launchers', 'Steam'),
                           os.path.join(partition, 'launcher', 'Steam')) for partition in all_partitions]

        for p in possible_paths:
            for path in p:
                steam_exe = os.path.join(path, 'steam.exe')
                if os.path.exists(steam_exe):
                    return path
        else:
            return None

    def get_steam_games(self, steam_app):

        """
        Search for the Steam Games in possible directories.

        Returns:
            The path to the Steam Games if found, otherwise None.
        """

        not_required_files = ['Trial', 'trial', 'installer', 'Installer', 'Service', 'EAAntiCheat', 'bootstrapper',
                              'ReportCodBug', 'GameServiceLauncher', 'Handler', 'cleaner', 'prep',
                              'bootstrapperCrashHandler.exe', 'codinstallcleaner', 'launcher', 'report', 'Report',
                              'Launcher']
        not_required_exe = []
        executables = []
        steamlib = os.path.join(steam_app, 'steamapps', 'libraryfolders.vdf')
        if os.path.exists(steamlib):
            with open(steamlib, 'r', encoding='utf-8', errors='ignore') as f:
                data = f.read()

            steam_libs_paths = re.findall(r'"path"\s+"([A-Z]:\\\\[A-Z].+)"', data)
            if steam_libs_paths:
                for steam_lib in steam_libs_paths:
                    common_folder = os.path.join(steam_lib, 'steamapps', 'common')
                    if os.path.exists(common_folder):
                        dirs = os.listdir(common_folder)
                        for dir in dirs:
                            game_dir = os.path.join(common_folder, dir)
                            for game in os.listdir(game_dir):
                                if game[-3:] == 'exe':
                                    executables.append((game, os.path.join(game_dir, game)))

        for game, game_path in executables:
            for i in not_required_files:
                index = game.find(i)
                if index == -1:
                    continue
                else:
                    not_required_exe.append((game, game_path))
                    break
        for not_required_exe in not_required_exe:
            executables.remove(not_required_exe)

        return executables


class EpicGames:
    """
    A class to locate the Epic Games Launcher installation directory.
    """

    def __init__(self):
        self.all_partitions = [partition.device for partition in psutil.disk_partitions(all=False)]
        self.possible_paths = self._generate_possible_paths()

    def _generate_possible_paths(self):
        """
        Generate a list of possible paths where the Epic Games Launcher might be installed.

        Returns:
            List of potential paths.
        """
        paths = []
        for partition in self.all_partitions:
            paths.extend([
                os.path.join(partition, 'Program Files (x86)', 'Epic Games', 'Launcher', 'Engine', 'Binaries', 'Win64'),
                os.path.join(partition, 'Program Files', 'Epic Games', 'Launcher', 'Engine', 'Binaries', 'Win64'),
                os.path.join(partition, 'Epic Games', 'Launcher', 'Engine', 'Binaries', 'Win64'),
                os.path.join(partition, 'Games', 'Epic Games', 'Launcher', 'Engine', 'Binaries', 'Win64'),
                os.path.join(partition, 'My Programs', 'Epic Games', 'Launcher', 'Engine', 'Binaries', 'Win64'),
                os.path.join(partition, 'Launchers', 'Epic Games', 'Launcher', 'Engine', 'Binaries', 'Win64'),
                os.path.join(partition, 'Launcher', 'Epic Games', 'Launcher', 'Engine', 'Binaries', 'Win64'),
                os.path.join(partition, 'launchers', 'Epic Games', 'Launcher', 'Engine', 'Binaries', 'Win64'),
                os.path.join(partition, 'launcher', 'Epic Games', 'Launcher', 'Engine', 'Binaries', 'Win64')
            ])
        return paths

    def find_epic(self):
        """
        Search for the Epic Games Launcher executable in possible directories.

        Returns:
            The path to the Epic Games Launcher executable if found, otherwise None.
        """
        for path in self.possible_paths:
            epic_exe = os.path.join(path, 'EpicGamesLauncher.exe')
            if os.path.exists(epic_exe):
                return path
        return None

    def get_epic_games(self):
        not_required_files = ['Trial', 'trial', 'installer', 'Installer', 'Service', 'EAAntiCheat', 'bootstrapper',
                              'ReportCodBug', 'GameServiceLauncher', 'Handler', 'cleaner', 'prep',
                              'bootstrapperCrashHandler.exe', 'codinstallcleaner', 'launcher', 'report', 'Report',
                              'Launcher',
                              'Helper', 'DXSETUP', 'vcredist', 'Rockstar', 'Social-Club', 'AntiCheat', 'Epic']
        paths = []
        exists_paths = []
        exe_apps = []
        not_required_exes = []
        for partition in self.all_partitions:
            paths.extend([
                os.path.join(partition, 'Program Files (x86)', 'Epic Games'),
                os.path.join(partition, 'Program Files', 'Epic Games'),
                os.path.join(partition, 'Epic Games'),
                os.path.join(partition, 'Games', 'Epic Games'),
                os.path.join(partition, 'My Programs', 'Epic Games'),
                os.path.join(partition, 'Launchers', 'Epic Games'),
                os.path.join(partition, 'Launcher', 'Epic Games'),
                os.path.join(partition, 'launchers', 'Epic Games'),
                os.path.join(partition, 'launcher', 'Epic Games')
            ])

        for path in paths:
            if os.path.exists(path):
                if 'Launcher' in os.listdir(path):
                    pass
                elif 'Epic Online Services' in os.listdir(path):
                    pass
                else:
                    exists_paths.append(path)

        for path in exists_paths:
            for gameFolder in os.listdir(path):
                for root, dirs, files in os.walk(os.path.join(path, gameFolder)):
                    for file in files:
                        if file.endswith('.exe'):
                            exe_apps.append((file, os.path.join(root, file)))
                            for not_required_exe in not_required_files:
                                index = file.find(not_required_exe)
                                if index == -1:
                                    continue
                                else:
                                    not_required_exes.append((file, os.path.join(root, file)))
                                    break
        for not_required_exe in not_required_exes:
            exe_apps.remove(not_required_exe)

        return exe_apps


if __name__ == '__main__':
    epic = EpicGames()
    steam = Steam()
    epic_launcher = epic.find_epic()
    steam_launcher = steam.find_steam()
    if epic_launcher and steam_launcher:
        epic_games = epic.get_epic_games()
        steam_games = steam.get_steam_games(steam_launcher)
        print('Epic Games: \n')
        for egame, path in epic_games:
            print(f'Game: {egame}\nPath: {path}\n')
        print('\nSteam Games: \n')
        for sgame, path in steam_games:
            print(f'Game: {sgame}\nPath: {path}\n')
    else:
        print('Error')
