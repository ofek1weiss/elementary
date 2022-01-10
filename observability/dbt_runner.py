import subprocess

from utils.log import get_logger

logger = get_logger(__name__)


class DbtRunner(object):
    def __init__(self, project_dir: str, profiles_dir: str):
        self.project_dir = project_dir
        self.profiles_dir = profiles_dir

    def _run_command(self, command_args: list) -> bool:
        dbt_command = ['dbt']
        dbt_command.extend(command_args)
        dbt_command.extend(['--project-dir', self.project_dir])
        dbt_command.extend(['--profiles-dir', self.profiles_dir])
        logger.debug(f"Running {' '.join(dbt_command)} (this might take a while)")
        result = subprocess.run(dbt_command, check=False, capture_output=True)
        logger.info(result.stdout.decode('utf-8'))
        if result.returncode != 0:
            return False

        return True

    def deps(self) -> bool:
        return self._run_command(['deps'])

    def seed(self) -> bool:
        return self._run_command(['seed'])

    def snapshot(self) -> bool:
        return self._run_command(['snapshot'])

    def run(self, model=None) -> bool:
        command_args = ['run']
        if model is not None:
            command_args.extend(['-m', model])
        return self._run_command(command_args)

