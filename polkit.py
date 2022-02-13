import os

# launch script with: ./generate_files.pkexec /path/to/tmp


def make_dotfiles(path_to_generate_files_sh: str):
    dotpolicy_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE policyconfig PUBLIC
     "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
     "http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd">

    <policyconfig>

      <action id="it.weeeopen.peracotta.generate-files">
        <description>Run P.E.R.A.C.O.T.T.A.</description>
        <message>Authentication is required to run generate_files</message>
        <defaults>
          <allow_any>yes</allow_any>
          <allow_inactive>yes</allow_inactive>
          <allow_active>yes</allow_active>
        </defaults>
        <annotate key="org.freedesktop.policykit.exec.path">{path_to_generate_files_sh}</annotate>
        <annotate key="org.freedesktop.policykit.exec.allow_gui">TRUE</annotate>
      </action>

    </policyconfig>
    """

    dotpkexec_content = f"""#!/bin/bash
    [[ $# -eq 0 ]] && OUT="." || OUT="$@"
    pkexec "{path_to_generate_files_sh}" $(readlink -f "$OUT")
    """

    path_to_dotpolicy = "/usr/share/polkit-1/actions/it.weeeopen.peracotta.generate-files.policy"
    path_to_tmp_dotpolicy = "./it.weeeopen.peracotta.generate-files.policy"
    path_to_dotpkexec = "./generate_files.pkexec"

    with open(path_to_tmp_dotpolicy, "w") as f:
        f.write(dotpolicy_content)
        os.system(f'sudo mv "{path_to_tmp_dotpolicy}" "{path_to_dotpolicy}"')
        print(path_to_dotpolicy, "was created!")

    with open(path_to_dotpkexec, "w") as f:
        f.write(dotpkexec_content)
        # make file executable -- octal is needed
        os.chmod(path_to_dotpkexec, 0o775)
        print(path_to_dotpkexec, "was created!")


if __name__ == "__main__":
    working_directory = os.getcwd()

    path_to_gen_files_sh = os.path.join(working_directory, "scripts", "generate_files.sh")
    make_dotfiles(path_to_gen_files_sh)
