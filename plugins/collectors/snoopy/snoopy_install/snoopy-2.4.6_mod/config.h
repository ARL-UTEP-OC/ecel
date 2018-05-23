/* config.h.  Generated from config.h.in by configure.  */
/* config.h.in.  Generated from configure.ac by autoheader.  */

/* Define to 1 if you have the <ctype.h> header file. */
#define HAVE_CTYPE_H 1

/* Define to 1 if you have the <dlfcn.h> header file. */
#define HAVE_DLFCN_H 1

/* Define to 1 if you have the <errno.h> header file. */
#define HAVE_ERRNO_H 1

/* Define to 1 if you have the <features.h> header file. */
#define HAVE_FEATURES_H 1

/* Define to 1 if you have the `fork' function. */
#define HAVE_FORK 1

/* Define to 1 if you have the `getcwd' function. */
#define HAVE_GETCWD 1

/* Define to 1 if you have the `gethostname' function. */
#define HAVE_GETHOSTNAME 1

/* Define to 1 if you have the `getsid' function. */
#define HAVE_GETSID 1

/* Define to 1 if you have the `gettimeofday' function. */
#define HAVE_GETTIMEOFDAY 1

/* Define to 1 if you have the <grp.h> header file. */
#define HAVE_GRP_H 1

/* Define to 1 if you have the <inttypes.h> header file. */
#define HAVE_INTTYPES_H 1

/* Define to 1 if you have the `dl' library (-ldl). */
#define HAVE_LIBDL 1

/* Define to 1 if you have the `pthread' library (-lpthread). */
#define HAVE_LIBPTHREAD 1

/* Define to 1 if you have the <limits.h> header file. */
#define HAVE_LIMITS_H 1

/* Define to 1 if you have the `localtime_r' function. */
#define HAVE_LOCALTIME_R 1

/* Define to 1 if your system has a GNU libc compatible `malloc' function, and
   to 0 otherwise. */
#define HAVE_MALLOC 1

/* Define to 1 if you have the <memory.h> header file. */
#define HAVE_MEMORY_H 1

/* Define to 1 if you have the <pwd.h> header file. */
#define HAVE_PWD_H 1

/* Define to 1 if you have the `socket' function. */
#define HAVE_SOCKET 1

/* Define to 1 if you have the <stdint.h> header file. */
#define HAVE_STDINT_H 1

/* Define to 1 if you have the <stdio.h> header file. */
#define HAVE_STDIO_H 1

/* Define to 1 if you have the <stdlib.h> header file. */
#define HAVE_STDLIB_H 1

/* Define to 1 if you have the `strchr' function. */
#define HAVE_STRCHR 1

/* Define to 1 if you have the `strdup' function. */
#define HAVE_STRDUP 1

/* Define to 1 if you have the <strings.h> header file. */
#define HAVE_STRINGS_H 1

/* Define to 1 if you have the <string.h> header file. */
#define HAVE_STRING_H 1

/* Define to 1 if you have the `strstr' function. */
#define HAVE_STRSTR 1

/* Define to 1 if you have the <syslog.h> header file. */
#define HAVE_SYSLOG_H 1

/* Define to 1 if you have the <sys/socket.h> header file. */
#define HAVE_SYS_SOCKET_H 1

/* Define to 1 if you have the <sys/stat.h> header file. */
#define HAVE_SYS_STAT_H 1

/* Define to 1 if you have the <sys/syscall.h> header file. */
#define HAVE_SYS_SYSCALL_H 1

/* Define to 1 if you have the <sys/time.h> header file. */
#define HAVE_SYS_TIME_H 1

/* Define to 1 if you have the <sys/types.h> header file. */
#define HAVE_SYS_TYPES_H 1

/* Define to 1 if you have the <sys/un.h> header file. */
#define HAVE_SYS_UN_H 1

/* Define to 1 if you have the <time.h> header file. */
#define HAVE_TIME_H 1

/* Define to 1 if you have the <unistd.h> header file. */
#define HAVE_UNISTD_H 1

/* Define to 1 if you have the `vfork' function. */
#define HAVE_VFORK 1

/* Define to 1 if you have the <vfork.h> header file. */
/* #undef HAVE_VFORK_H */

/* Define to 1 if `fork' works. */
#define HAVE_WORKING_FORK 1

/* Define to 1 if `vfork' works. */
#define HAVE_WORKING_VFORK 1

/* Define to the sub-directory in which libtool stores uninstalled libraries.
   */
#define LT_OBJDIR ".libs/"

/* Name of package */
#define PACKAGE "snoopy"

/* Define to the address where bug reports for this package should be sent. */
#define PACKAGE_BUGREPORT "https://github.com/a2o/snoopy/issues/"

/* Define to the full name of this package. */
#define PACKAGE_NAME "Snoopy Logger"

/* Define to the full name and version of this package. */
#define PACKAGE_STRING "Snoopy Logger 2.4.6"

/* Define to the one symbol short name of this package. */
#define PACKAGE_TARNAME "snoopy"

/* Define to the home page for this package. */
#define PACKAGE_URL "https://github.com/a2o/snoopy/"

/* Define to the version of this package. */
#define PACKAGE_VERSION "2.4.6"

/* Is config file parsing enabled? */
#define SNOOPY_CONF_CONFIGFILE_ENABLED 1

/* INI configuration file path to use */
#define SNOOPY_CONF_CONFIGFILE_PATH "/etc/snoopy.ini"

/* Is datasource "cmdline" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_cmdline 1

/* Is datasource "cwd" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_cwd 1

/* Is datasource "datetime" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_datetime 1

/* Is datasource "domain" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_domain 1

/* Is datasource "egid" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_egid 1

/* Is datasource "egroup" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_egroup 1

/* Is datasource "env" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_env 1

/* Is datasource "env_all" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_env_all 1

/* Is datasource "euid" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_euid 1

/* Is datasource "eusername" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_eusername 1

/* Is datasource "filename" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_filename 1

/* Is datasource "gid" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_gid 1

/* Is datasource "group" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_group 1

/* Is datasource "hostname" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_hostname 1

/* Is datasource "login" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_login 1

/* Is datasource "pid" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_pid 1

/* Is datasource "ppid" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_ppid 1

/* Is datasource "rpname" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_rpname 1

/* Is datasource "sid" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_sid 1

/* Is datasource "snoopy_literal" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_snoopy_literal 1

/* Is datasource "snoopy_threads" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_snoopy_threads 1

/* Is datasource "snoopy_version" available? Forced "Yes". */
#define SNOOPY_CONF_DATASOURCE_ENABLED_snoopy_version 1

/* Is datasource "tid" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_tid 1

/* Is datasource "tid_kernel" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_tid_kernel 1

/* Is datasource "timestamp" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_timestamp 1

/* Is datasource "timestamp_ms" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_timestamp_ms 1

/* Is datasource "timestamp_us" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_timestamp_us 1

/* Is datasource "tty" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_tty 1

/* Is datasource "tty_uid" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_tty_uid 1

/* Is datasource "tty_username" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_tty_username 1

/* Is datasource "uid" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_uid 1

/* Is datasource "username" available? */
#define SNOOPY_CONF_DATASOURCE_ENABLED_username 1

/* Enable error logging */
/* #undef SNOOPY_CONF_ERROR_LOGGING_ENABLED */

/* filtering subsystem */
#define SNOOPY_CONF_FILTERING_ENABLED 1

/* Filter chain to use */
#define SNOOPY_CONF_FILTER_CHAIN ""

/* Is filter "exclude_spawns_of" available? */
#define SNOOPY_CONF_FILTER_ENABLED_exclude_spawns_of 1

/* Is filter "exclude_uid" available? */
#define SNOOPY_CONF_FILTER_ENABLED_exclude_uid 1

/* Is filter "only_root" available? */
#define SNOOPY_CONF_FILTER_ENABLED_only_root 1

/* Is filter "only_tty" available? */
#define SNOOPY_CONF_FILTER_ENABLED_only_tty 1

/* Is filter "only_uid" available? */
#define SNOOPY_CONF_FILTER_ENABLED_only_uid 1

/* Custom message format to use */
#define SNOOPY_CONF_MESSAGE_FORMAT "[uid:%{uid} sid:%{sid} tty:%{tty} cwd:%{cwd} filename:%{filename}]: %{cmdline}"

/* Default output provider */
/* #undef SNOOPY_CONF_OUTPUT_DEFAULT */

/* Default output arguments */
/* #undef SNOOPY_CONF_OUTPUT_DEFAULT_ARG */

/* Is output "devlog" available? */
#define SNOOPY_CONF_OUTPUT_ENABLED_devlog 1

/* Is output "devnull" available? */
#define SNOOPY_CONF_OUTPUT_ENABLED_devnull 1

/* Is output "devtty" available? */
#define SNOOPY_CONF_OUTPUT_ENABLED_devtty 1

/* Is output "file" available? Forced "Yes". */
#define SNOOPY_CONF_OUTPUT_ENABLED_file 1

/* Is output "socket" available? Forced "Yes". */
#define SNOOPY_CONF_OUTPUT_ENABLED_socket 1

/* Is output "stderr" available? */
#define SNOOPY_CONF_OUTPUT_ENABLED_stderr 1

/* Is output "stdout" available? */
#define SNOOPY_CONF_OUTPUT_ENABLED_stdout 1

/* Is output "syslog" available? */
/* #undef SNOOPY_CONF_OUTPUT_ENABLED_syslog */

/* Syslog facility to use by default */
#define SNOOPY_CONF_SYSLOG_FACILITY LOG_AUTHPRIV

/* Syslog ident to use by default */
#define SNOOPY_CONF_SYSLOG_IDENT "snoopy"

/* Syslog level to use by default */
#define SNOOPY_CONF_SYSLOG_LEVEL LOG_INFO

/* thread safety */
/* #undef SNOOPY_CONF_THREAD_SAFETY_ENABLED */

/* Define to 1 if you have the ANSI C header files. */
#define STDC_HEADERS 1

/* Version number of package */
#define VERSION "2.4.6"

/* Define to `int' if <sys/types.h> doesn't define. */
/* #undef gid_t */

/* Define to `__inline__' or `__inline' if that's what the C compiler
   calls it, or to nothing if 'inline' is not supported under any name.  */
#ifndef __cplusplus
/* #undef inline */
#endif

/* Define to rpl_malloc if the replacement function should be used. */
/* #undef malloc */

/* Define to `int' if <sys/types.h> does not define. */
/* #undef pid_t */

/* Define to `unsigned int' if <sys/types.h> does not define. */
/* #undef size_t */

/* Define to `int' if <sys/types.h> doesn't define. */
/* #undef uid_t */

/* Define as `fork' if `vfork' does not work. */
/* #undef vfork */
