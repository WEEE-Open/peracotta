import os
from time import sleep

# launch script with: ./generate_files.pkexec /path/to/tmp

# in annotate key path to generate_files.sh
# this should be saved as /usr/share/polkit-1/actions/generate_files_pkexec.policy
dotpolicy_content = """ <?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE policyconfig PUBLIC
 "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
 "http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd">

<policyconfig>

  <action id="org.freedesktop.policykit.pkexec.run-generate_files">
    <description>Run P.E.R.A.C.O.T.T.A.</description>
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
dotpkexec_content = """#!/bin/bash
[[ $# -eq 0 ]] && OUT="." || OUT="$@"
pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY "" $(readlink -f "$OUT")
"""
path_to_dotpkexec = "./generate_files.pkexec"


def make_dotfiles(path_to_generate_files_sh: str):
    dotpolicy_split = '<annotate key="org.freedesktop.policykit.exec.path">'
    dotpkexec_split = '$XAUTHORITY "'

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

    with open(local_path_to_dotpolicy, 'w') as f:
        f.write(dotpolicy_with_path)
        os.system("./scripts/move_pkexec_policy_file.sh")
        while not os.path.exists(path_to_dotpolicy):
            sleep(0.1)
        print(path_to_dotpolicy, "was created!")

    with open(path_to_dotpkexec, 'w') as f:
        f.write(dotpkexec_with_path)
        # make file executable -- octal is needed
        os.chmod(path_to_dotpkexec, 0o776)
        print(path_to_dotpkexec, "was created!")


if __name__ == '__main__':
    working_directory = os.getcwd()
    if not os.path.isdir(os.path.join(working_directory, "tmp")):
        os.makedirs(os.path.join(working_directory, "tmp"))

    folder_name = "tmp"
    path_to_gen_files_sh = os.path.join(working_directory, "scripts", "generate_files.sh")
    print(path_to_gen_files_sh)
    make_dotfiles(path_to_generate_files_sh=path_to_gen_files_sh)
