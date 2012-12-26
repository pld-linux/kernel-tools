# TODO
# - optflags

#
# Conditional build:
%bcond_without	verbose		# verbose build (V=1)
%bcond_without	perf		# perf tools

%define		rel		0.5
%define		basever	3.7
%define		postver	.1
Summary:	Assortment of tools for the Linux kernel
Summary(pl.UTF-8):	Zestaw narzędzi dla jądra Linuksa
Name:		kernel-tools
Version:	%{basever}%{postver}
Release:	%{rel}
License:	GPL v2
Group:		Applications/System
Source0:	http://www.kernel.org/pub/linux/kernel/v3.x/linux-%{basever}.tar.xz
# Source0-md5:	21223369d682bcf44bcdfe1521095983
%if "%{postver}" != ".0"
Patch0:		http://www.kernel.org/pub/linux/kernel/v3.x/patch-%{version}.bz2
# Patch0-md5:	c391dc1a1b4dae81aaef6f08a0594813
%endif
Source1:	cpupower.service
Source2:	cpupower.config
URL:		http://www.kernel.org/
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with perf}
BuildRequires:	asciidoc
BuildRequires:	audit-libs-devel
BuildRequires:	binutils-devel
BuildRequires:	bison
BuildRequires:	docbook-style-xsl
BuildRequires:	elfutils-devel
BuildRequires:	flex
BuildRequires:	gtk+2-devel >= 2.0
BuildRequires:	libunwind-devel >= 0.99
BuildRequires:	newt-devel
BuildRequires:	perl-devel >= 5.1
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	slang-devel
BuildRequires:	xmlto
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	systemd-units >= 0.38
Provides:	cpufreq-utils = 1:009-0.6.p1
Provides:	cpufrequtils = 1:009-0.6.p1
Provides:	cpupowerutils = 1:009-0.6.p1
Obsoletes:	cpufreq-utils < 1:009-0.6.p1
Obsoletes:	cpufrequtils < 1:009-0.6.p1
Obsoletes:	cpupowerutils < 1:009-0.6.p1
Obsoletes:	cpuspeed < 1:1.5-16
Requires:	%{name}-cpupower-libs = %{version}-%{release}

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
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-cpupower-libs = %{version}-%{release}
Provides:	cpupowerutils-devel = 1:009-0.6.p1
Obsoletes:	cpupowerutils-devel < 1:009-0.6.p1

%description cpupower-libs-devel
Development files for the cpupower library.

%description cpupower-libs-devel -l pl.UTF-8
Pliki programistyczne biblioteki cpupower.

%package perf-core
Summary:	perf profiler tool (core package)
Summary(pl.UTF-8):	Narzędzie profilujące perf (podstawowe narzędzia)
Group:		Applications/System

%description perf-core
Perf is a profiler tool for Linux 2.6+ based systems that abstracts
away CPU hardware differences in Linux performance measurements and
presents a simple commandline interface. Perf is based on the
perf_events interface exported by recent versions of the Linux kernel.

This package contains core files and scripts.

%description perf-core -l pl.UTF-8
Perf to narzędzie profilujące dla systemów opartych na Linuksie 2.6+,
odseparowujące od różnic sprzętowych między pomiarami wydajności w
zależności od procesora oraz udostępniające prosty interfejs linii
poleceń. Perf jest oparty na interfejsie perf_events eksportowanym
przez nowe wersje jądra Linuksa.

Ten pakiet zawiera podstawowe pliki i skrypty.

%package perf-gtk
Summary:	perf profiler tool (GTK+ GUI)
Summary(pl.UTF-8):	Narzędzie profilujące perf (interfejs graficzny GTK+)
Group:		X11/Applications
Requires:	%{name}-perf-core = %{version}-%{release}
Provides:	%{name}-perf = %{version}-%{release}

%description perf-gtk
Perf is a profiler tool for Linux 2.6+ based systems that abstracts
away CPU hardware differences in Linux performance measurements and
presents a simple commandline interface. Perf is based on the
perf_events interface exported by recent versions of the Linux kernel.

This package contains GTK+ based GUI.

%description perf-gtk -l pl.UTF-8
Perf to narzędzie profilujące dla systemów opartych na Linuksie 2.6+,
odseparowujące od różnic sprzętowych między pomiarami wydajności w
zależności od procesora oraz udostępniające prosty interfejs linii
poleceń. Perf jest oparty na interfejsie perf_events eksportowanym
przez nowe wersje jądra Linuksa.

Ten pakiet zawiera graficzny interfejs oparty na GTK+.

%package perf-slang
Summary:	perf profiler tool (Slang TUI)
Summary(pl.UTF-8):	Narzędzie profilujące perf (interfejs tekstowy Slang)
Group:		X11/Applications
Requires:	%{name}-perf-core = %{version}-%{release}
Provides:	%{name}-perf = %{version}-%{release}

%description perf-slang
Perf is a profiler tool for Linux 2.6+ based systems that abstracts
away CPU hardware differences in Linux performance measurements and
presents a simple commandline interface. Perf is based on the
perf_events interface exported by recent versions of the Linux kernel.

This package contains Slang based TUI.

%description perf-slang -l pl.UTF-8
Perf to narzędzie profilujące dla systemów opartych na Linuksie 2.6+,
odseparowujące od różnic sprzętowych między pomiarami wydajności w
zależności od procesora oraz udostępniające prosty interfejs linii
poleceń. Perf jest oparty na interfejsie perf_events eksportowanym
przez nowe wersje jądra Linuksa.

Ten pakiet zawiera tekstowy interfejs oparty na bibliotece Slang.

%package -n bash-completion-perf
Summary:	Bash completion for perf command
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów dla polecenia perf
Group:		Applications/Shells
Requires:	%{name}-perf = %{version}-%{release}
Requires:	bash-completion

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

%build
cd linux-%{basever}

# cpupower
%{__make} -C tools/power/cpupower \
	%{makeopts} \
	CPUFREQ_BENCH=false

%ifarch %{ix86}
%{__make} -C tools/power/cpupower/debug/i386 centrino-decode powernow-k8-decode \
	%{makeopts} \
%endif

%ifarch %{x8664}
%{__make} -C tools/power/cpupower/debug/x86_64 centrino-decode powernow-k8-decode \
	%{makeopts}
%endif

%ifarch %{ix86} %{x8664}
%{__make} -C tools/power/x86/x86_energy_perf_policy \
	%{makeopts}
%{__make} -C tools/power/x86/turbostat \
	%{makeopts}
%endif

# slabinfo
%{__make} -C tools/vm \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -Wextra"

%if %{with perf}
# perf slang version
PWD=${PWD:-$(pwd)}
install -d $PWD/perf-{slang,gtk}
%{__make} -C tools/perf all man \
	O=$PWD/perf-slang \
	NO_GTK2=1 \
	%{makeopts} \
	prefix=%{_prefix} \
	perfexecdir=%{_datadir}/perf-core \
	template_dir=%{_datadir}/perf-core/templates

# perf gtk version
%{__make} -C tools/perf all man \
	O=$PWD/perf-gtk \
	%{makeopts} \
	prefix=%{_prefix} \
	perfexecdir=%{_datadir}/perf-core \
	template_dir=%{_datadir}/perf-core/templates
%endif

# gen_init_cpio
%{__make} -C usr gen_init_cpio \
	%{makeopts} \

%install
rm -rf $RPM_BUILD_ROOT
cd linux-%{basever}

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

%ifarch %{ix86}
install -p tools/power/cpupower/debug/i386/{centrino,powernow-k8}-decode $RPM_BUILD_ROOT%{_bindir}
%endif
%ifarch %{x8664}
install -p tools/power/cpupower/debug/x86_64/{centrino,powernow-k8}-decode $RPM_BUILD_ROOT%{_bindir}
%endif

install tools/vm/slabinfo $RPM_BUILD_ROOT%{_bindir}

%ifarch %{ix86} %{x8664}
install -d $RPM_BUILD_ROOT%{_mandir}/man8
# broken makefile, install manually
%if 0
%{__make} install \
	-C tools/power/x86/x86_energy_perf_policy \
	DESTDIR=$RPM_BUILD_ROOT
%else
cd tools/power/x86/x86_energy_perf_policy
install -p x86_energy_perf_policy $RPM_BUILD_ROOT%{_bindir}
install -p x86_energy_perf_policy.8 $RPM_BUILD_ROOT%{_mandir}/man8
cd -
%endif

# broken makefile, install manually
%if 0
%{__make} install \
	-C tools/power/x86/turbostat \
	DESTDIR=$RPM_BUILD_ROOT
%else
cd tools/power/x86/turbostat
install -p turbostat $RPM_BUILD_ROOT%{_bindir}/turbostat
install -p turbostat.8 $RPM_BUILD_ROOT%{_mandir}/man8
cd -
%endif
%endif

%if %{with perf}
# perf slang
PWD=${PWD:-$(pwd)}
# perf slang version
%{__make} -j1 install install-man \
	-C tools/perf \
	O=$PWD/perf-slang \
	NO_GTK2=1 \
	CC="%{__cc}" \
	%{?with_verbose:V=1} \
	prefix=%{_prefix} \
	perfexecdir=%{_datadir}/perf-core \
	template_dir=%{_datadir}/perf-core/templates \
	DESTDIR=$RPM_BUILD_ROOT
%{__mv} $RPM_BUILD_ROOT%{_bindir}/perf{,-slang}

# perf gtk
%{__make} -j1 install install-man \
	-C tools/perf \
	O=$PWD/perf-gtk \
	CC="%{__cc}" \
	%{?with_verbose:V=1} \
	prefix=%{_prefix} \
	perfexecdir=%{_datadir}/perf-core \
	template_dir=%{_datadir}/perf-core/templates \
	DESTDIR=$RPM_BUILD_ROOT
%{__mv} $RPM_BUILD_ROOT%{_bindir}/perf{,-gtk}

%py_comp $RPM_BUILD_ROOT%{_datadir}/perf-core/scripts/python
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/perf-core/scripts/python
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
%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{_bindir}/centrino-decode
%attr(755,root,root) %{_bindir}/powernow-k8-decode
%endif
%ifarch %{ix86} %{x8664}
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
%files perf-core
%defattr(644,root,root,755)
%{_mandir}/man1/perf*.1*
%dir %{_datadir}/perf-core
%attr(755,root,root) %{_datadir}/perf-core/perf-archive

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

%files perf-gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/perf-gtk

%files perf-slang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/perf-slang

%files -n bash-completion-perf
%defattr(644,root,root,755)
/etc/bash_completion.d/perf
%endif
