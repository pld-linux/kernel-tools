# TODO:
# - redefine: PACKAGE_BUGREPORT=cpufreq@vger.kernel.org
# - add -n python-perf?
# - add bcond to disable building docs (perf docs)
# - install of perf links perf binary again

# Conditional build:
%bcond_without	verbose		# verbose build (V=1)
%bcond_without	perf		# perf tools
%bcond_without	gtk		# GTK+ 2.x perf support
%bcond_without	libunwind	# libunwind perf support
%bcond_without	multilib	# multilib perf support

%ifarch x32
%undefine	with_libunwind
%endif
%ifnarch %{x8664}
%undefine	with_multilib
%endif

%define		basever		4.4
%define		postver		.0
Summary:	Assortment of tools for the Linux kernel
Summary(pl.UTF-8):	Zestaw narzędzi dla jądra Linuksa
Name:		kernel-tools
Version:	%{basever}%{postver}
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://www.kernel.org/pub/linux/kernel/v4.x/linux-%{basever}.tar.xz
# Source0-md5:	9a78fa2eb6c68ca5a40ed5af08142599
Source1:	cpupower.service
Source2:	cpupower.config
%if "%{postver}" != ".0"
Patch0:		https://www.kernel.org/pub/linux/kernel/v4.x/patch-%{version}.xz
# Patch0-md5:	3a465c7cf55ec9dbf2d72d9292aa5fde
%endif
Patch1:		x32.patch
URL:		http://www.kernel.org/
BuildRequires:	gettext-tools
BuildRequires:	pciutils-devel
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with perf}
BuildRequires:	asciidoc
BuildRequires:	audit-libs-devel
BuildRequires:	binutils-devel
BuildRequires:	bison
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	elfutils-devel
BuildRequires:	flex
%if %{with multilib}
BuildRequires:	gcc-multilib-32
BuildRequires:	gcc-multilib-x32
%endif
%{?with_libunwind:BuildRequires:	libunwind-devel >= 0.99}
BuildRequires:	numactl-devel
BuildRequires:	perl-devel >= 5.1
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	slang-devel
BuildRequires:	xmlto
%if %{with gtk}
BuildRequires:	gtk+2-devel >= 2.0
BuildRequires:	pkgconfig
%endif
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# otherwise /usr/lib/rpm/bin/debugedit: canonicalization unexpectedly shrank by one character
%define		_enable_debug_packages	0

%define		makeopts	CC="%{__cc}" %{?with_verbose:V=1}

%description
This package contains the software from tools/ subdirectory from Linux
kernel source and the supporting documentation.

%description -l pl.UTF-8
Ten pakiet zawiera oprogramowanie z podkatalogu tools/ ze źródeł jądra
Linuksa oraz związaną z nim dokumentację.

%package cpupower
Summary:	cpupower - Shows and sets processor power related values
Summary(pl.UTF-8):	cpupower - wyświetlanie i ustawianie wartości związanych z zużyciem energii przez procesor
Group:		Applications/System
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-cpupower-libs = %{version}-%{release}
Requires:	systemd-units >= 0.38
Provides:	cpupowerutils = 1:009-0.6.p1
Obsoletes:	cpupowerutils < 1:009-0.6.p1
Obsoletes:	cpuspeed < 1:1.5-16

%description cpupower
cpupower is a collection of tools to examine and tune power saving
related features of your processor.

%description cpupower -l pl.UTF-8
cpupower to zbiór narzędzi do sprawdzania i ustawiania opcji procesora
związanych z oszczędzaniem energii.

%package cpupower-libs
Summary:	cpupower library
Summary(pl.UTF-8):	Biblioteka cpupower
Group:		Libraries

%description cpupower-libs
cpupower library.

%description cpupower-libs -l pl.UTF-8
Biblioteka cpupower.

%package cpupower-libs-devel
Summary:	Development files for the cpupower library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki cpupower
Group:		Development/Libraries
Requires:	%{name}-cpupower-libs = %{version}-%{release}
Provides:	cpupowerutils-devel = 1:009-0.6.p1
Obsoletes:	cpupowerutils-devel < 1:009-0.6.p1
Conflicts:	cpufrequtils-devel

%description cpupower-libs-devel
Development files for the cpupower library.

%description cpupower-libs-devel -l pl.UTF-8
Pliki programistyczne biblioteki cpupower.

%package perf
Summary:	perf profiler tool
Summary(pl.UTF-8):	Narzędzie profilujące perf
Group:		Applications/System
Suggests:	binutils
Obsoletes:	perf-core
Obsoletes:	perf-slang

%description perf
Perf is a profiler tool for Linux 2.6+ based systems that abstracts
away CPU hardware differences in Linux performance measurements and
presents a simple commandline interface. Perf is based on the
perf_events interface exported by recent versions of the Linux kernel.

This package contains core files, scripts and text interface (TUI).

%description perf -l pl.UTF-8
Perf to narzędzie profilujące dla systemów opartych na Linuksie 2.6+,
odseparowujące od różnic sprzętowych między pomiarami wydajności w
zależności od procesora oraz udostępniające prosty interfejs linii
poleceń. Perf jest oparty na interfejsie perf_events eksportowanym
przez nowe wersje jądra Linuksa.

Ten pakiet zawiera podstawowe pliki, skrypty oraz interfejs tekstowy
(TUI).

%package perf-vdso32
Summary:	perf profiler tool - VDSO 32-bit ABI reader
Summary(pl.UTF-8):	Narzędzie profilujące perf - odczyt VDSO dla ABI 32-bitowego
Group:		Applications/System
Requires:	%{name}-perf = %{version}-%{release}

%description perf-vdso32
Perf is a profiler tool for Linux 2.6+ based systems that abstracts
away CPU hardware differences in Linux performance measurements and
presents a simple commandline interface. Perf is based on the
perf_events interface exported by recent versions of the Linux kernel.

This package contains perf-read-vdso32 tool for reading the 32-bit
compatibility VDSO in 64-bit mode.

%description perf-vdso32 -l pl.UTF-8
Perf to narzędzie profilujące dla systemów opartych na Linuksie 2.6+,
odseparowujące od różnic sprzętowych między pomiarami wydajności w
zależności od procesora oraz udostępniające prosty interfejs linii
poleceń. Perf jest oparty na interfejsie perf_events eksportowanym
przez nowe wersje jądra Linuksa.

Ten pakiet zawiera narzędzie perf-read-vdso32 do odczytu VDSO dla
binariów 32-bitowych w trybie 64-bitowym.

%package perf-vdsox32
Summary:	perf profiler tool - VDSO x32 ABI reader
Summary(pl.UTF-8):	Narzędzie profilujące perf - odczyt VDSO dla ABI x32
Group:		Applications/System
Requires:	%{name}-perf = %{version}-%{release}

%description perf-vdsox32
Perf is a profiler tool for Linux 2.6+ based systems that abstracts
away CPU hardware differences in Linux performance measurements and
presents a simple commandline interface. Perf is based on the
perf_events interface exported by recent versions of the Linux kernel.

This package contains perf-read-vdso32 tool for reading the x32 mode
32-bit compatibility VDSO in 64-bit mode.

%description perf-vdsox32 -l pl.UTF-8
Perf to narzędzie profilujące dla systemów opartych na Linuksie 2.6+,
odseparowujące od różnic sprzętowych między pomiarami wydajności w
zależności od procesora oraz udostępniające prosty interfejs linii
poleceń. Perf jest oparty na interfejsie perf_events eksportowanym
przez nowe wersje jądra Linuksa.

Ten pakiet zawiera narzędzie perf-read-vdso32 do odczytu VDSO dla
binariów ABI x32 w trybie 64-bitowym.

%package perf-gtk
Summary:	perf profiler tool (GTK+ 2 GUI)
Summary(pl.UTF-8):	Narzędzie profilujące perf (interfejs graficzny GTK+ 2)
Group:		X11/Applications
Requires:	%{name}-perf = %{version}-%{release}

%description perf-gtk
Perf is a profiler tool for Linux 2.6+ based systems that abstracts
away CPU hardware differences in Linux performance measurements and
presents a simple commandline interface. Perf is based on the
perf_events interface exported by recent versions of the Linux kernel.

This package contains GTK+ 2 based GUI.

%description perf-gtk -l pl.UTF-8
Perf to narzędzie profilujące dla systemów opartych na Linuksie 2.6+,
odseparowujące od różnic sprzętowych między pomiarami wydajności w
zależności od procesora oraz udostępniające prosty interfejs linii
poleceń. Perf jest oparty na interfejsie perf_events eksportowanym
przez nowe wersje jądra Linuksa.

Ten pakiet zawiera graficzny interfejs oparty na GTK+ 2.

%package -n bash-completion-perf
Summary:	Bash completion for perf command
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów dla polecenia perf
Group:		Applications/Shells
Requires:	%{name}-perf
Requires:	bash-completion
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n bash-completion-perf
Bash completion for perf command.

%description -n bash-completion-perf -l pl.UTF-8
Bashowe uzupełnianie parametrów dla polecenia perf.

%prep
%setup -qc
cd linux-%{basever}

%if "%{postver}" != ".0"
%patch0 -p1
%endif

%patch1 -p1

sed -i -e 's#libexec/perf-core#%{_datadir}/perf-core#g' tools/perf/config/Makefile

%build
cd linux-%{basever}

# Simple Disk Sleep Monitor
%{__cc} %{rpmcppflags} %{rpmcflags} %{rpmldflags} Documentation/laptops/dslm.c -o dslm

# cpupower
%{__make} -C tools/power/cpupower \
	%{makeopts} \
	CPUFREQ_BENCH=false \
	OPTIMIZATION="%{rpmcflags}" \
	STRIPCMD=true

%ifarch %{ix86} x32
%{__make} -C tools/power/cpupower/debug/i386 centrino-decode powernow-k8-decode \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"
%endif

%ifarch %{x8664} x32
%{__make} -C tools/power/cpupower/debug/x86_64 centrino-decode powernow-k8-decode \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"
%endif

%ifarch %{ix86} %{x8664} x32
%{__make} -C tools/power/x86/x86_energy_perf_policy \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"
CFLAGS="%{rpmcflags}" \
%{__make} -C tools/power/x86/turbostat \
	CC="%{__cc}"
%endif

# page-types, slabinfo
%{__make} -C tools/vm page-types slabinfo \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -Wextra -I../lib"

%if %{with perf}
%{__make} -C tools/perf all man \
%ifarch %{x8664}
	IS_X86_64=1 \
	%{!?with_multilib:NO_PERF_READ_VDSO32=1 NO_PERF_READ_VDSOX32=1} \
%endif
	%{!?with_gtk:NO_GTK2=1} \
	%{!?with_libunwind:NO_LIBUNWIND=1} \
	%{makeopts} \
	CFLAGS_OPTIMIZE="%{rpmcflags}" \
	WERROR=0 \
	prefix=%{_prefix} \
	perfexecdir=%{_datadir}/perf-core \
	lib=%{_lib} \
	template_dir=%{_datadir}/perf-core/templates
%endif

# gen_init_cpio
%{__make} -C usr gen_init_cpio \
	%{makeopts} \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

cd linux-%{basever}
install -d $RPM_BUILD_ROOT%{_sbindir}

%{__make} -C tools/power/cpupower install \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=%{_libdir} \
	mandir=%{_mandir} \
	CPUFREQ_BENCH=false

%find_lang cpupower
mv cpupower.lang ..

install -d $RPM_BUILD_ROOT{/etc/sysconfig,%{systemdunitdir}}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}/cpupower.service
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/cpupower

%ifarch %{ix86} x32
install -p tools/power/cpupower/debug/i386/{centrino,powernow-k8}-decode $RPM_BUILD_ROOT%{_bindir}
%endif
%ifarch %{x8664} x32
install -p tools/power/cpupower/debug/x86_64/{centrino,powernow-k8}-decode $RPM_BUILD_ROOT%{_bindir}
%endif

install -p tools/vm/slabinfo $RPM_BUILD_ROOT%{_bindir}
install -p tools/vm/page-types $RPM_BUILD_ROOT%{_sbindir}
install -p dslm $RPM_BUILD_ROOT%{_sbindir}

%ifarch %{ix86} %{x8664} x32
install -d $RPM_BUILD_ROOT%{_mandir}/man8
%{__make} -C tools/power/x86/x86_energy_perf_policy install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C tools/power/x86/turbostat install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%if %{with perf}
%{__make} -C tools/perf -j1 install install-man \
%ifarch %{x8664}
	IS_X86_64=1 \
	%{!?with_multilib:NO_PERF_READ_VDSO32=1 NO_PERF_READ_VDSOX32=1} \
%endif
	%{!?with_gtk:NO_GTK2=1} \
	%{!?with_libunwind:NO_LIBUNWIND=1} \
	CC="%{__cc}" \
	CFLAGS_OPTIMIZE="%{rpmcflags}" \
	WERROR=0 \
	%{?with_verbose:V=1} \
	prefix=%{_prefix} \
	perfexecdir=%{_datadir}/perf-core \
	template_dir=%{_datadir}/perf-core/templates \
	lib=%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{_datadir}/perf-core/scripts/python
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/perf-core/scripts/python

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/perf-core/tests
%endif

# gen_init_cpio
install -p usr/gen_init_cpio $RPM_BUILD_ROOT%{_bindir}/gen_init_cpio

%clean
rm -rf $RPM_BUILD_ROOT

%post	cpupower-libs -p /sbin/ldconfig
%postun	cpupower-libs -p /sbin/ldconfig

%post cpupower
%systemd_post cpupower.service

%preun cpupower
%systemd_preun cpupower.service

%postun cpupower
%systemd_reload

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gen_init_cpio
%attr(755,root,root) %{_bindir}/slabinfo
%attr(755,root,root) %{_sbindir}/dslm
%attr(755,root,root) %{_sbindir}/page-types
%ifarch %{ix86} %{x8664} x32
%attr(755,root,root) %{_bindir}/centrino-decode
%attr(755,root,root) %{_bindir}/powernow-k8-decode
%endif
%ifarch %{ix86} %{x8664} x32
%attr(755,root,root) %{_bindir}/turbostat
%attr(755,root,root) %{_bindir}/x86_energy_perf_policy
%{_mandir}/man8/turbostat.8*
%{_mandir}/man8/x86_energy_perf_policy.8*
%endif

%files cpupower -f cpupower.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cpupower
%{_mandir}/man1/cpupower*.1*
%{systemdunitdir}/cpupower.service
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/cpupower

%files cpupower-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcpupower.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcpupower.so.0

%files cpupower-libs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h

%if %{with perf}
%files perf
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/perf
%attr(755,root,root) %{_bindir}/trace
%{_mandir}/man1/perf*.1*
%dir %{_datadir}/perf-core
%attr(755,root,root) %{_datadir}/perf-core/perf-archive
%attr(755,root,root) %{_datadir}/perf-core/perf-with-kcore

%dir %{_datadir}/perf-core/scripts

%dir %{_datadir}/perf-core/scripts/perl
%dir %{_datadir}/perf-core/scripts/perl/Perf-Trace-Util
%dir %{_datadir}/perf-core/scripts/perl/Perf-Trace-Util/lib
%dir %{_datadir}/perf-core/scripts/perl/Perf-Trace-Util/lib/Perf
%dir %{_datadir}/perf-core/scripts/perl/Perf-Trace-Util/lib/Perf/Trace
%{_datadir}/perf-core/scripts/perl/Perf-Trace-Util/lib/Perf/Trace/*.pm
%dir %{_datadir}/perf-core/scripts/perl/bin
%attr(755,root,root) %{_datadir}/perf-core/scripts/perl/bin/*
%{_datadir}/perf-core/scripts/perl/*.pl

%dir %{_datadir}/perf-core/scripts/python
%dir %{_datadir}/perf-core/scripts/python/Perf-Trace-Util
%dir %{_datadir}/perf-core/scripts/python/Perf-Trace-Util/lib
%dir %{_datadir}/perf-core/scripts/python/Perf-Trace-Util/lib/Perf
%dir %{_datadir}/perf-core/scripts/python/Perf-Trace-Util/lib/Perf/Trace
%{_datadir}/perf-core/scripts/python/Perf-Trace-Util/lib/Perf/Trace/*.py*
%dir %{_datadir}/perf-core/scripts/python/bin
%attr(755,root,root) %{_datadir}/perf-core/scripts/python/bin/*
%{_datadir}/perf-core/scripts/python/*.py*

%dir %{_libdir}/traceevent
%dir %{_libdir}/traceevent/plugins
%attr(755,root,root) %{_libdir}/traceevent/plugins/plugin_*.so

%if %{with multilib}
%files perf-vdso32
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/perf-read-vdso32

%files perf-vdsox32
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/perf-read-vdsox32
%endif

%if %{with gtk}
%files perf-gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libperf-gtk.so
%endif

%files -n bash-completion-perf
%defattr(644,root,root,755)
/etc/bash_completion.d/perf
%endif
