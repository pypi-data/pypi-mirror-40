import click
import sys

from ..logger import Logger
from subprocess import run, PIPE
from datetime import datetime


class NinjaPatcher(Logger):
    def __init__(self, config):
        super().__init__(config)
        self.datetime_str = str(datetime.now()).replace(" ", "-").replace(":", "-").replace(".", "-")
        self.folder_name = "ninja-patching-" + self.datetime_str
        self.seed_repo_path = "/seed"
        self.all_repo_path = "/all"
        self.patch_filename = "patch.patch"

    def execute(self):
        run(["mkdir", self.folder_name], check=True)
        click.echo("Created folder " + self.folder_name)

        self._prompt_repo_configuration()
        self._update_all_repo()
        self._read_submodule_names()
        self._create_patch()
        self._apply_patch()

        run(["rm", "-rf", self.folder_name], check=True)
        click.echo("Removed folder " + self.folder_name)
        sys.exit(0)

    def _prompt_repo_configuration(self):
        """
        Prompt user inputs about
            1. URL of the seed repository
            2. Commit SHA-1 of the current patch
            3. Commit SHA-1 of the new patch

        :return: None
        """
        seed_repo_url = click.prompt(click.style('SSH URL of the seed repo (git@ada....git)', fg='magenta'),
                                     type=str)
        completed_process = run(["git", "clone", seed_repo_url, self.folder_name + self.seed_repo_path],
                                stderr=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))

        all_repo_url = seed_repo_url[:-4] + "-all.git"
        completed_process = run(["git", "clone", all_repo_url, "--recursive", self.folder_name + self.all_repo_path],
                                stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))

        self.current_sha = click.prompt(click.style('Patch from commit (8-digit/40-digit Git Commit SHA-1)',
                                                    fg='magenta'), type=str)
        completed_process = run(["git", "--git-dir=" + self.folder_name + self.seed_repo_path + "/.git",
                                 "cat-file", "commit", self.current_sha], stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit("Not a valid commit: " + self.current_sha)

        self.new_sha = click.prompt(click.style('Patch to commit (8-digit/40-digit Git Commit SHA-1)',
                                                fg='magenta'), type=str)
        completed_process = run(["git", "--git-dir=" + self.folder_name + self.seed_repo_path + "/.git",
                                 "cat-file", "commit", self.new_sha], stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit("Not a valid commit: " + self.new_sha)

        click.echo()

    def _update_all_repo(self):
        completed_process = run(["rc", "git", "checkout", "master"],
                                cwd=self.folder_name+self.all_repo_path+"/",
                                stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))

        completed_process = run(["rc", "git", "pull", "origin", "master"],
                                cwd=self.folder_name+self.all_repo_path+"/",
                                stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))

    def _read_submodule_names(self):
        completed_process = run(["git", "config", "--file", ".gitmodules", "--name-only",
                                 "--get-regexp", "path"],
                                cwd=self.folder_name+self.all_repo_path+"/",
                                stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))
        if completed_process.stdout is None:
            self._error_and_exit("-all repo does not contain any submodules")

        submodule_paths = str(completed_process.stdout, "utf-8").splitlines()
        self.submodule_names = []
        for path in submodule_paths:
            self.submodule_names.append(path.split(".")[1])

    def _create_patch(self):
        completed_process = run(["git", "--git-dir=" + self.folder_name + self.seed_repo_path + "/.git",
                                 "format-patch", "-k", "--stdout", self.current_sha + ".." + self.new_sha],
                                stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))
        with click.open_file(self.folder_name + "/" + self.patch_filename, 'w') as f:
            f.write(str(completed_process.stdout, "utf-8"))
        self._success("Generated patch file")
        click.echo()

    def _apply_patch(self):
        click.echo("Started patching...")

        patch_path = "../../" + self.patch_filename
        parent_path = self.folder_name + self.all_repo_path + "/"
        success_count = 0
        fail_count = 0
        for name in self.submodule_names:
            cwd = parent_path + name + "/"
            completed_process = run(["git", "apply", "--check", patch_path],
                                    cwd=cwd, stderr=PIPE, stdout=PIPE)
            if completed_process.returncode:
                self._error("Skipped " + name + " due to merge conflicts")
                fail_count += 1
            else:
                completed_process = run(["git", "am", "--signoff", patch_path],
                                        cwd=cwd, stderr=PIPE, stdout=PIPE)
                if completed_process.returncode:
                    self._error("Skipped " + name + ": " + str(completed_process.stderr, "utf-8"))
                    fail_count += 1
                else:
                    self._success("Patched " + name)
                    success_count += 1

        click.echo()
        if success_count:
            click.echo("Populating changes to students' repositories...")
            completed_process = run(["rc", "git", "push", "origin", "master"],
                                    cwd=self.folder_name + self.all_repo_path + "/",
                                    stderr=PIPE, stdout=PIPE)
            if completed_process.returncode:
                self._error_and_exit(str(completed_process.stderr, "utf-8"))
            click.echo()
        self._success("Ninja Patching completed")
        self._success("     Patched " + str(success_count))
        self._error("     Skipped " + str(fail_count))
        click.echo()

    def _error_and_exit(self, msg):
        self._error(msg)
        run(["rm", "-rf", self.folder_name], check=True)
        click.echo("Removed folder " + self.folder_name)
        sys.exit(1)
