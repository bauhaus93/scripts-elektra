import os

from glob import ELEKTRA_PREFIX, LCDPROC_PREFIX, OUTPUT_PREFIX, BUILD_PREFIX, INSTALL_PREFIX

def generate_build_command(root_dir, target, build_type, install, run_tests, run_shell, clean_build):
    elektra_path = os.path.join(root_dir, ELEKTRA_PREFIX)
    build_path = os.path.join(root_dir, OUTPUT_PREFIX, BUILD_PREFIX)
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
    elif "toml" in target:
        plugins = "MAINTAINED;-EXPERIMENTAL;toml"
    if clean_build:
        clean_cmd = f"rm -rf {build_path} && \\\n"
    else:
        clean_cmd = ""

    setup_cmd = f"{clean_cmd}mkdir -p {build_path} && \\\ncd {build_path}"
    if not target == "toml_min":
        cmake_cmd = "&& \\\n" + generate_cmake(build_type, elektra_path, kdb_config_path, build_doc, run_tests, plugins, tools, bindings)
    else:
        cmake_cmd = ""
    make_cmd = generate_make(install, 8)
    if install:
        ld_cmd = f"&& \\\nsudo ldconfig"
    else:
        ld_cmd = ""

    cmd = f"{setup_cmd} {cmake_cmd} {make_cmd} {ld_cmd}"

    if lcdproc_cmd:
        cmd += f" && \\\n{lcdproc_cmd}"

    if run_tests:
        test_cmd = generate_test(16)
        cmd += f" && \\\n{test_cmd}"

    if run_shell:
        cmd += f" && \\\nbash"

    return cmd

def generate_cmake(build_type, elektra_path, kdb_config_path, build_doc, build_testing, plugins, tools, bindings):
    kdb_system_path = os.path.join(kdb_config_path, "system")
    kdb_spec_path = os.path.join(kdb_config_path, "spec")
    kdb_home_path = os.path.join(kdb_config_path, "home")
    
    cmd = f"cmake {elektra_path}"
    cmd += f"\\\n\t-DCMAKE_BUILD_TYPE={build_type}"
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
        cmd += " &&\\\nsudo make install"
    return "&& \\\n" + cmd

def generate_test(jobs = 8):
    cmd = f"ctest -j {jobs} --force-new-ctest-process --output-on-failure --no-compress-output"
    cmd += "\\\n\t-T Test -E \"testmod_(crypto_(botan|openssl)|dbus(recv)?|fcrypt|gpgme|zeromqsend)\""
    return cmd

def generate_lcdproc(root_dir):
    install_path = os.path.join(root_dir, OUTPUT_PREFIX, INSTALL_PREFIX)
    lcdproc_path = os.path.join(root_dir, LCDPROC_PREFIX)
    
    setup_cmd = f"cd {lcdproc_path} && \\\nmake clean"
    configure_cmd = generate_lcdproc_configure(install_path)
    build_cmd = f"sh ./autogen.sh && \\\n{configure_cmd} && \\\nsudo make install"
    post_build_cmd = "./post-install.sh"
    set_driver_cmd = f"kdb set '/sw/lcdproc/lcdd/#0/current/server/drivers/#0' '@/curses/#0'"

    cmd = f"{setup_cmd} && \\\n{build_cmd} && \\\n{post_build_cmd} && \\\n{set_driver_cmd}"

    return cmd

def generate_lcdproc_configure(debug = True):
    cmd = f'PKG_CONFIG_PATH="/usr/local/lib/pkgconfig" ./configure'
    if debug:
        cmd += f" \\\n\t--enable-debug"
    return cmd
