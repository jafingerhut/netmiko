"""MRV Communications Driver (OptiSwitch)."""
import time
import re

from netmiko.cisco_base_connection import CiscoSSHConnection


class MrvOptiswitchSSH(CiscoSSHConnection):
    """MRV Communications Driver (OptiSwitch)."""

    def session_preparation(self):
        """Prepare the session after the connection has been established."""
        self._test_channel_read(pattern=r"[>#]")
        self.set_base_prompt()
        self.enable()
        self.disable_paging(command="no cli-paging")
        # Clear the read buffer
        time.sleep(0.3 * self.global_delay_factor)
        self.set_base_prompt()
        self.clear_buffer()

    def enable(self, cmd="enable", pattern=r"#", re_flags=re.IGNORECASE):
        """Enable mode on MRV uses no password."""
        output = ""
        if not self.check_enable_mode():
            self.write_channel(self.normalize_cmd(cmd))
            output += self.read_until_prompt_or_pattern(
                pattern=pattern, re_flags=re_flags, read_entire_line=True
            )
            if not self.check_enable_mode():
                msg = (
                    "Failed to enter enable mode. Please ensure you pass "
                    "the 'secret' argument to ConnectHandler."
                )
                raise ValueError(msg)
        return output

    def save_config(self, cmd="save config flash", confirm=False, confirm_response=""):
        """Saves configuration."""
        return super().save_config(
            cmd=cmd, confirm=confirm, confirm_response=confirm_response
        )
