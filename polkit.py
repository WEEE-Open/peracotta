import os
import subprocess
import shlex

# launch script with: ./generate_files.pkexec /path/to/tmp

# in annotate key path to generate_files.sh
# this should be saved as /usr/share/polkit-1/actions/generate_files_pkexec.policy
dotpolicy_content = """ <?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE policyconfig PUBLIC
 "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
 "http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd">

<policyconfig>

  <action id="org.freedesktop.policykit.pkexec.run-generate_files">
    <description>Run FlashTool</description>
    <message>Authentication is required to run generate_files</message>
    <defaults>
      <allow_any>no</allow_any>
      <allow_inactive>no</allow_inactive>
      <allow_active>auth_admin_keep</allow_active>
    </defaults>
    <annotate key="org.freedesktop.policykit.exec.path"></annotate>
    <annotate key="org.freedesktop.policykit.exec.allow_gui">TRUE</annotate>
  </action>

</policyconfig>
"""
path_to_dotpolicy = "/usr/share/polkit-1/actions/generate_files_pkexec.policy"
local_path_to_dotpolicy = "./generate_files_pkexec.policy"

# path to generate_files.sh in between dquotes
# this should be saved as ./generate_files.pkexec
dotpkexec_content = """#!/bin/sh
pkexec "" "$@"
"""
path_to_dotpkexec = "./generate_files.pkexec"


def make_dotfiles(path_to_generate_files_sh: str):
    dotpolicy_split = '<annotate key="org.freedesktop.policykit.exec.path">'
    dotpkexec_split = 'pkexec "'

    dotpolicy_with_path = dotpolicy_content.split(dotpolicy_split)[0] + \
                          dotpolicy_split + \
                          path_to_generate_files_sh + \
                          dotpolicy_content.split(dotpolicy_split)[1]

    dotpkexec_with_path = dotpkexec_content.split(dotpkexec_split)[0] + \
                          dotpkexec_split + \
                          path_to_generate_files_sh + \
                          dotpkexec_content.split(dotpkexec_split)[1]

    # print(dotpolicy_with_path)
    # print()
    # print(dotpkexec_with_path)

    if not os.path.isfile(path_to_dotpolicy):
        with open(local_path_to_dotpolicy, 'w') as f:
            f.write(dotpolicy_with_path)
            print("I need root permissions to move the file just this one time.")
            os.system("x-terminal-emulator -e sudo mv " + local_path_to_dotpolicy + " " + path_to_dotpolicy)
            print(path_to_dotpolicy, "was created!")
    else:
        print(path_to_dotpolicy, "already existed.")

    if not os.path.isfile(path_to_dotpkexec):
        with open(path_to_dotpkexec, 'w') as f:
            f.write(dotpkexec_with_path)
            # make file executable -- octal is needed
            os.chmod(path_to_dotpkexec, 0o776)
            print(path_to_dotpkexec, "was created!")
    else:
        print(path_to_dotpkexec, "already existed.")


if __name__ == '__main__':
    make_dotfiles("./generate_files.sh")
