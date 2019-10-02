import os

from glob import ELEKTRA_PREFIX, OUTPUT_PREFIX, BUILD_PREFIX, INSTALL_PREFIX

def generate_build_command_default(root_dir, run_tests = False, clean_build = False):
    return generate_build_command(root_dir, run_tests, clean_build, False, None, None, None, 8)

def generate_build_command_all(root_dir, run_tests = False, clean_build = False):
    return generate_build_command(root_dir, run_tests, clean_build, True, "ALL", "ALL", "ALL", 8)

def generate_build_command(root_dir, run_tests, clean_build, build_doc, plugins, tools, bindings, jobs):
    elektra_path = os.path.join(root_dir, ELEKTRA_PREFIX)
    build_path = os.path.join(root_dir, OUTPUT_PREFIX, BUILD_PREFIX)
    install_path = os.path.join(root_dir, OUTPUT_PREFIX, INSTALL_PREFIX)
    kdb_config_path = os.path.join(root_dir, OUTPUT_PREFIX, "config", "kdb")

    clean_cmd = f"rm -rf {install_path} {kdb_config_path}"
    if clean_build:
        clean_cmd += f" {build_path}"

    setup_cmd = f"{clean_cmd} && \\\nmkdir -p {build_path} {install_path} && \\\ncd {build_path}"
    cmake_cmd = generate_cmake(elektra_path, install_path, kdb_config_path, build_doc, plugins, tools, bindings)
    make_cmd = generate_make(8)

    cmd = f"{setup_cmd} && \\\n{cmake_cmd} && \\\n{make_cmd}"

    if run_tests:
        test_cmd = generate_test(16)
        cmd += f" && \\\n{test_cmd}"

    return cmd

def generate_cmake(elektra_path, install_path, kdb_config_path, build_doc, plugins, tools, bindings):
    kdb_system_path = os.path.join(kdb_config_path, "system")
    kdb_spec_path = os.path.join(kdb_config_path, "spec")
    kdb_home_path = os.path.join(kdb_config_path, "home")

    cmd = f'cmake {elektra_path} \\\n\t-DCMAKE_INSTALL_PREFIX="{install_path}"'
    cmd += f' \\\n\t-DKDB_DB_SYSTEM="{kdb_system_path}"'
    cmd += f' \\\n\t-DKDB_DB_SPEC="{kdb_spec_path}"'
    cmd += f' \\\n\t-DKDB_DB_HOME="{kdb_home_path}"'
    cmd += " \\\n\t-DBUILD_STATIC=ON -DBUILD_COVERAGE=ON"

    if build_doc:
        cmd += f" \\\n\t-DBUILD_DOCUMENTATION=ON"
    else:
        cmd += f" \\\n\t-DBUILD_DOCUMENTATION=OFF"

    if plugins:
        cmd += f" \\\n\t-DPLUGINS=\"{plugins}\""
    if tools:
        cmd += f" \\\n\t-DTOOLS=\"{tools}\""
    if bindings:
        cmd += f" \\\n\t-DBINDINGS=\"{bindings}\""
    return cmd

def generate_make(jobs = 8):
    cmd = f"make -j{jobs} install"
    return cmd

def generate_test(jobs = 8):
    cmd = f"ctest -j {jobs} --force-new-ctest-process --output-on-failure --no-compress-output"
    cmd += "\\\n\t-T Test -E \"testmod_(crypto_(botan|openssl)|dbus(recv)?|fcrypt|gpgme|zeromqsend)\""
    return cmd
