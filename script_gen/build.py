import os

from glob import ELEKTRA_PREFIX, LCDPROC_PREFIX, OUTPUT_PREFIX, BUILD_PREFIX, INSTALL_PREFIX

def generate_build_command_toml(root_dir, build_type = "Release", run_tests = False, clean_build = False):
    return generate_build_command(root_dir, build_type, run_tests, clean_build, True, "MAINTAINED;-EXPERIMENTAL;toml;-yajl", None, None, 8)

def generate_build_command(root_dir, target, build_type, run_tests, run_shell, clean_build):
    elektra_path = os.path.join(root_dir, ELEKTRA_PREFIX)
    build_path = os.path.join(root_dir, OUTPUT_PREFIX, BUILD_PREFIX)
    install_path = os.path.join(root_dir, OUTPUT_PREFIX, INSTALL_PREFIX)
    kdb_config_path = os.path.join(root_dir, OUTPUT_PREFIX, "config", "kdb")

    plugins = None
    tools = None
    bindings = None
    build_doc = False
    lcdproc_cmd = None
    if target == "all":
        plugins = "ALL"
        tools = "ALL"
        bindings = "ALL"
    elif target == "lcdproc":
        plugins = "c;cache;dump;gopts;hexnumber;ini;list;mmapstorage;network;ni;noresolver;path;quickdump;range;reference;resolver;resolver_fm_hpu_b;spec;specload;type;validation;sync"
        lcdproc_cmd = generate_lcdproc(root_dir)
    elif target == "toml":
        plugins = "MAINTAINED;-EXPERIMENTAL;toml"

    clean_cmd = f"rm -rf {install_path} {kdb_config_path}"
    if clean_build:
        clean_cmd += f" {build_path}"

    setup_cmd = f"{clean_cmd} && \\\nmkdir -p {build_path} {install_path} && \\\ncd {build_path}"
    cmake_cmd = generate_cmake(build_type, elektra_path, install_path, kdb_config_path, build_doc, run_tests, plugins, tools, bindings)
    make_cmd = generate_make(8)

    cmd = f"{setup_cmd} && \\\n{cmake_cmd} && \\\n{make_cmd}"

    if lcdproc_cmd:
        cmd += f" && \\\n{lcdproc_cmd}"

    if run_tests:
        test_cmd = generate_test(16)
        cmd += f" && \\\n{test_cmd}"

    if run_shell:
        cmd += f" && \\\nbash"

    return cmd

def generate_cmake(build_type, elektra_path, install_path, kdb_config_path, build_doc, build_testing, plugins, tools, bindings):
    kdb_system_path = os.path.join(kdb_config_path, "system")
    kdb_spec_path = os.path.join(kdb_config_path, "spec")
    kdb_home_path = os.path.join(kdb_config_path, "home")

    cmd = f"cmake {elektra_path}"
    cmd += f"\\\n\t-DCMAKE_BUILD_TYPE={build_type}"
    cmd += f'\\\n\t-DCMAKE_INSTALL_PREFIX="{install_path}"'
    cmd += f' \\\n\t-DKDB_DB_SYSTEM="{kdb_system_path}"'
    cmd += f' \\\n\t-DKDB_DB_SPEC="{kdb_spec_path}"'
    cmd += f' \\\n\t-DKDB_DB_HOME="{kdb_home_path}"'
    cmd += " \\\n\t-DBUILD_STATIC=ON"

    if build_doc:
        cmd += " \\\n\t-DBUILD_DOCUMENTATION=ON"
    else:
        cmd += " \\\n\t-DBUILD_DOCUMENTATION=OFF"

    if build_testing:
        cmd += " \\\n\t-DBUILD_TESTING=ON"
        cmd += " \\\n\t-DENABLE_TESTING=ON"
        cmd += " \\\n\t-DINSTALL_TESTING=ON"
    else:
        cmd += " \\\n\t-DBUILD_TESTING=OFF"
        cmd += " \\\n\t-DENABLE_TESTING=OFF"
        cmd += " \\\n\t-DINSTALL_TESTING=OFF"

    if plugins:
        cmd += f" \\\n\t-DPLUGINS=\"{plugins}\""
    if tools:
        cmd += f" \\\n\t-DTOOLS=\"{tools}\""
    if bindings:
        cmd += f" \\\n\t-DBINDINGS=\"{bindings}\""
    return cmd

def generate_make(install = True, jobs = 8):
    cmd = f"make -j{jobs}"
    if install:
        cmd += " install"
    return cmd

def generate_test(jobs = 8):
    cmd = f"ctest -j {jobs} --force-new-ctest-process --output-on-failure --no-compress-output"
    cmd += "\\\n\t-T Test -E \"testmod_(crypto_(botan|openssl)|dbus(recv)?|fcrypt|gpgme|zeromqsend)\""
    return cmd

def generate_lcdproc(root_dir):
    install_path = os.path.join(root_dir, OUTPUT_PREFIX, INSTALL_PREFIX)
    lcdproc_path = os.path.join(root_dir, LCDPROC_PREFIX)
    
    setup_cmd = f"cd {lcdproc_path} && \\\nmake clean"
    configure_cmd = generate_lcdproc_configure(install_path)
    build_cmd = f"sh ./autogen.sh && \\\n{configure_cmd} && \\\n {path_extend_bin(root_dir)} make install"
    post_build_cmd = "./post-install.sh"
    set_driver_cmd = f"kdb set '/sw/lcdproc/lcdd/#0/current/server/drivers/#0' '@/curses/#0'"
    invoke_LCDd_cmd = "LCDd -f"

    cmd = f"{setup_cmd} && \\\n{build_cmd} && \\\n{post_build_cmd} && \\\n{set_driver_cmd} && \\\n{invoke_LCDd_cmd}"

    return cmd

def generate_lcdproc_configure(install_path, debug = True):
    cmd = f'PKG_CONFIG_PATH="{install_path}/lib/pkgconfig" ./configure'
    cmd += f" \\\n\t--prefix={install_path}"
    if debug:
        cmd += f" \\\n\t--enable-debug"
    return cmd

def path_extend_bin(root_dir):
    bin_dir = os.path.join(root_dir, OUTPUT_PREFIX, INSTALL_PREFIX, "bin")
    cmd = f'PATH="$PATH:{bin_dir}"'
    return cmd
