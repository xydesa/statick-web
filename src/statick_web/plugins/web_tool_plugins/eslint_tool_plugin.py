"""Apply eslint tool and gather results."""

import logging
import re
import subprocess
from typing import List, Match, Optional, Pattern

from statick_tool.issue import Issue
from statick_tool.package import Package
from statick_tool.tool_plugin import ToolPlugin


class ESLintToolPlugin(ToolPlugin):  # type: ignore
    """Apply eslint tool and gather results."""

    def get_name(self) -> str:
        """Get name of tool."""
        return "eslint"

    # pylint: disable=too-many-locals
    def scan(self, package: Package, level: str) -> Optional[List[Issue]]:
        """Run tool and gather output."""
        tool_bin = "eslint"

        tool_config = ".eslintrc"
        user_config = self.plugin_context.config.get_tool_config(
            self.get_name(), level, "config"
        )
        if user_config is not None:
            tool_config = user_config

        format_file_name = self.plugin_context.resources.get_file(tool_config)
        flags = []  # type: List[str]
        if format_file_name is not None:
            flags += ["-c", format_file_name]
        flags += ["--ext", ".js,.html", "-f", "unix"]
        user_flags = self.get_user_flags(level)
        flags += user_flags

        files = []  # type: List[str]
        if "html_src" in package:
            files += package["html_src"]
        if "javascript_src" in package:
            files += package["javascript_src"]

        total_output = []  # type: List[str]

        for src in files:
            try:
                exe = [tool_bin] + flags + [src]
                output = subprocess.check_output(
                    exe, stderr=subprocess.STDOUT, universal_newlines=True
                )
                total_output.append(output)

            except subprocess.CalledProcessError as ex:
                if ex.returncode == 1:  # eslint returns 1 upon linting errors
                    total_output.append(ex.output)
                else:
                    logging.warning(
                        "%s failed! Returncode = %d", tool_bin, ex.returncode
                    )
                    logging.warning("%s exception: %s", self.get_name(), ex.output)
                    return None

            except OSError as ex:
                logging.warning("Couldn't find %s! (%s)", tool_bin, ex)
                return None

        for output in total_output:
            logging.debug("%s", output)

        with open(self.get_name() + ".log", "w") as fid:
            for output in total_output:
                fid.write(output)

        issues = self.parse_output(total_output)  # type: List[Issue]
        return issues

    # pylint: enable=too-many-locals

    def parse_output(self, total_output: List[str]) -> List[Issue]:
        """Parse tool output and report issues."""
        eslint_re = r"(.+):(\d+):(\d+):\s(.+)\s\[(.+)\/(.+)\]"
        parse = re.compile(eslint_re)  # type: Pattern[str]
        issues = []  # type: List[Issue]

        for output in total_output:
            lines = output.split("\n")
            count = 0
            for line in lines:
                match = parse.match(line)  # type: Optional[Match[str]]
                if match:
                    severity_str = match.group(5).lower()
                    severity = 3
                    if severity_str == "warning":
                        severity = 3
                    elif severity_str == "error":
                        severity = 5

                    count += 1

                    issues.append(
                        Issue(
                            match.group(1),
                            match.group(2),
                            self.get_name(),
                            match.group(6),
                            severity,
                            match.group(4),
                            None,
                        )
                    )
        return issues
