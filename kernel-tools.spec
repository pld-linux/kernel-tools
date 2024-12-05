# TODO:
# - redefine: PACKAGE_BUGREPORT=cpufreq@vger.kernel.org
# - add -n python-perf?
# - add bcond to disable building docs (perf docs)
# - install of perf links perf binary again
# - build runqslower (needs vmlinux with BPF section)
#
# Conditional build:
%bcond_without	verbose		# verbose build (V=1)
%bcond_without	cpupower	# cpupower tools
%bcond_without	perf		# perf tools
%bcond_without	gtk		# GTK+ 2.x perf support
%bcond_without	libunwind	# libunwind perf support
%bcond_without	multilib	# multilib perf support
%bcond_with	runqslower	# runqslower bpf tool
%bcond_without	usbip		# usbip utils

%ifnarch %{x8664}
%undefine	with_multilib
%endif

%define		basever		6.12
%define		postver		.2
Summary:	Assortment of tools for the Linux kernel
Summary(pl.UTF-8):	Zestaw narzędzi dla jądra Linuksa
Name:		kernel-tools
Version:	%{basever}%{postver}
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://www.kernel.org/pub/linux/kernel/v6.x/linux-%{basever}.tar.xz
# Source0-md5:	844fae6a58c7f43af44d8cea8484b4a1
Source1:	cpupower.service
Source2:	cpupower.config
Source3:	cpupower@.service
%if "%{postver}" != ".0"
Patch0:		https://www.kernel.org/pub/linux/kernel/v6.x/patch-%{version}.xz
# Patch0-md5:	e5639b9a45ccac69b564f3ef88cd2920
%endif
Patch1:		x32.patch
Patch2:		regex.patch
Patch3:		%{name}-perf-update.patch
Patch4:		%{name}-perf-gtk2.patch
URL:		https://www.kernel.org/
BuildRequires:	bison
BuildRequires:	docutils
BuildRequires:	flex
BuildRequires:	gettext-tools
BuildRequires:	libtraceevent-devel
BuildRequires:	linux-libc-headers >= 7:4.12
BuildRequires:	ncurses-devel
BuildRequires:	ncurses-ext-devel
BuildRequires:	pciutils-devel
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	python3-modules
BuildRequires:	readline-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with perf}
BuildRequires:	asciidoc
BuildRequires:	audit-libs-devel
BuildRequires:	babeltrace-devel
BuildRequires:	binutils-devel >= 4:2.29
BuildRequires:	clang >= 12.0.1
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	elfutils-devel >= 0.158
%if %{with multilib}
BuildRequires:	gcc-multilib-32
BuildRequires:	gcc-multilib-x32
%endif
# for `btftool btf dump file ... format c` - requires vmlinux with BPF section
%{?with_runqslower:BuildRequires:	kernel-vmlinux >= 5.?}
BuildRequires:	libbpf-devel
BuildRequires:	libcap-devel
%{?with_libunwind:BuildRequires:	libunwind-devel >= 0.99}
BuildRequires:	numactl-devel
BuildRequires:	openssl-devel
BuildRequires:	perl-devel >= 5.1
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	slang-devel
BuildRequires:	xmlto
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
# openscd? (CORESIGHT=1 for %{arm}?)
%if %{with gtk}
BuildRequires:	gtk+2-devel >= 2.0
%endif
%endif
%if %{with usbip}
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	gcc >= 6:4.0
BuildRequires:	libtool >= 2:2
BuildRequires:	libwrap-devel
BuildRequires:	udev-devel
%endif
# /usr/bin/turbostat
Conflicts:	pmtools < 20110323-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# otherwise /usr/lib/rpm/bin/debugedit: canonicalization unexpectedly shrank by one character
%define		_enable_debug_packages	0

%ifarch ppc ppc64
%define		makearch	powerpc
%else
%ifarch aarch64
%define		makearch	arm64
%else
%define		makearch	%{_target_base_arch}
%endif
%endif

%define		makeopts	ARCH=%{makearch} CC="%{__cc}" %{?with_verbose:V=1}

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

%package -n bash-completion-cpupower
Summary:	Bash completion for cpupower tools
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów dla poleceń cpupower
Group:		Applications/Shells
Requires:	%{name}-cpupower = %{version}-%{release}
Requires:	bash-completion
BuildArch:	noarch

%description -n bash-completion-cpupower
Bash completion for cpupower tools.

%description -n bash-completion-cpupower -l pl.UTF-8
Bashowe uzupełnianie parametrów dla poleceń cpupower.

%package hv
Summary:	Hyper-V virtualization tools
Summary(pl.UTF-8):	Narzędzia do wirtualizacji Hyper-V
Group:		Applications/System

%description hv
Hyper-V virtualization tools.

%description hv -l pl.UTF-8
Narzędzia do wirtualizacji Hyper-V.

%package perf
Summary:	perf profiler tool
Summary(pl.UTF-8):	Narzędzie profilujące perf
Group:		Applications/System
Suggests:	binutils
Obsoletes:	kernel-tools-perf-core < 3.16.2
Obsoletes:	kernel-tools-perf-slang < 3.16.2

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
Requires:	%{name}-perf = %{version}-%{release}
Requires:	bash-completion
BuildArch:	noarch

%description -n bash-completion-perf
Bash completion for perf command.

%description -n bash-completion-perf -l pl.UTF-8
Bashowe uzupełnianie parametrów dla polecenia perf.

%package -n bash-completion-kernel-tools
Summary:	Bash completion for kernel-tools commands
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów dla poleceń kernel-tools
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-kernel-tools
Bash completion for kernel-tools commands (currently bpftool).

%description -n bash-completion-kernel-tools -l pl.UTF-8
Bashowe uzupełnianie parametrów dla poleceń kernel-tools (obecnie
bpftool).

%package -n usbip
Summary:	USB device sharing system over IP network
Summary(pl.UTF-8):	System współdzielenia urządzeń USB po sieci IP
Group:		Networking/Utilities
Requires:	usbip-libs = %{version}-%{release}
# /lib/hwdata/usb.ids (note: only uncompressed file supported)
Requires:	hwdata >= 0.243-2

%description -n usbip
The USB/IP Project aims to develop a general USB device sharing system
over IP network. To share USB devices between computers with their
full functionality, USB/IP encapsulates "USB requests" into IP packets
and transmits them between computers. Original USB device drivers and
applications can be also used for remote USB devices without any
modification of them. A computer can use remote USB devices as if they
were directly attached; for example, we can:
 - USB storage devices: fdisk, mkfs, mount/umount, file operations,
   play a DVD movie and record a DVD-R media.
 - USB keyboards and USB mice: use with Linux console and X Window
   System.
 - USB webcams and USB speakers: view webcam, capture image data and
   play some music.
 - USB printers, USB scanners, USB serial converters and USB Ethernet
   interfaces: ok, use fine.

%description -n usbip -l pl.UTF-8
Projekt USB/IP ma na celu stworzenie ogólnego systemu współdzielenia
urządzeń USB po sieci IP. W celu współdzielenia urządzeń USB między
komputerami z zachowaniem pełnej funkcjonalności, USB/IP obudowuje
żądania SUB w pakiety IP i przesyła je między komputerami. Oryginalne
sterowniki urządzeń USB oraz aplikacje mogą być używane bez żadnych
modyfikacji. Komputer może wykorzystywać zdaln urządzenia USB tak,
jakby były podłączone bezpośrednio. Przykładowe możliwości:
 - urządzenia USB do przechowywania danych: można używać programów
   fdisk, mkfs, mount/umount, operacji na plikach, odtwarzać filmy
   DVD oraz nagrywać nośniki DVD-R
 - klawiatury i myszy USB: można ich używać na linuksowej konsoli oraz
   w systemie X Window
 - kamery i głośniki USB: można oglądać obraz z kamery, robić zdjęcia
   i odtwarzać muzykę
 - drukarki, skanery, konwertery portów szeregowych oraz interfejsy
   sieciowe USB: można ich normalnie używać

%package -n usbip-libs
Summary:	USB/IP library
Summary(pl.UTF-8):	Biblioteka USB/IP
Group:		Libraries

%description -n usbip-libs
USB over IP library.

%description -n usbip-libs -l pl.UTF-8
Biblioteka USB po IP.

%package -n usbip-devel
Summary:	Header files for usbip library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki usbip
Group:		Development/Libraries
Requires:	usbip-libs = %{version}-%{release}

%description -n usbip-devel
This package contains the header files needed to develop programs
which make use of USB/IP.

%description -n usbip-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
wykorzystujących USB/IP.

%package -n usbip-static
Summary:	Static usbip library
Summary(pl.UTF-8):	Statyczna biblioteka usbip
Group:		Development/Libraries
Requires:	usbip-devel = %{version}-%{release}

%description -n usbip-static
Static usbip library.

%description -n usbip-static -l pl.UTF-8
Statyczna biblioteka usbip.

%prep
%setup -qc
cd linux-%{basever}

%if "%{postver}" != ".0"
%patch0 -p1
%endif

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%{__sed} -i -e '/^CFLAGS = /s/ -g / $(OPTFLAGS) /' tools/hv/Makefile
%{__sed} -i -e '/^CFLAGS+=/s/ -O1 / $(OPTFLAGS) /' tools/thermal/tmon/Makefile
%{__sed} -i -e 's#libexec/perf-core#%{_lib}/perf-core#g' tools/perf/Makefile.config

# don't rebuild on make install
%{__sed} -i -e '/^\$(LIBBPF): FORCE/ s/FORCE$//' tools/bpf/bpftool/Makefile

%if %{without runqslower}
%{__sed} -i -e '/^all: / s/ runqslower//' \
	-e '/^install: / s/ runqslower_install//' \
	tools/bpf/Makefile
%endif

%build
Wstringop=""
Waddressof=""
%if "%{cc_version}" >= "8"
Wstringop="-Wno-error=stringop-truncation"
%endif
%if "%{cc_version}" >= "9"
Waddressof="-Wno-error=address-of-packed-member"
%endif
cd linux-%{basever}

# Simple Disk Sleep Monitor
%{__make} -C tools/laptop/dslm \
	%{makeopts} \
	EXTRA_CFLAGS="%{rpmcflags}"

# tools common (used eg. by tools/mm)
%{__make} -C tools/lib/api \
	%{makeopts} \
	EXTRA_CFLAGS="%{rpmcflags} $Wstringop"

# lsgpio
CFLAGS="%{rpmcflags}" \
%{__make} -C tools/gpio -j1 \
	%{makeopts}

# HyperV is Windows based, x86 specific
%ifarch %{ix86} %{x8664} x32
%{__make} -C tools/hv \
	%{makeopts} \
	OPTFLAGS="%{rpmcflags}"
%endif

CFLAGS="%{rpmcflags}" \
%{__make} -C tools/iio -j1 \
	%{makeopts}

%{__make} -C tools/laptop/freefall \
	%{makeopts} \
	CFLAGS="%{rpmcflags}"

# make bpftool first, top-level bpf CFLAGS cause includes conflict
CFLAGS="%{rpmcflags}" \
%{__make} -C tools/bpf/bpftool \
	%{makeopts}

CFLAGS="%{rpmcflags}" \
%{__make} -C tools/bpf \
	%{makeopts} \
	EXTRA_CFLAGS="%{rpmcflags}" \
	%{?with_runqslower:VMLINUX_BTF=$(rpm -ql kernel-vmlinux | head -n 1)}

# perf
%if %{with perf}
%{__make} -j1 -C tools/perf all man \
%ifarch %{x8664}
	IS_X86_64=1 \
	%{!?with_multilib:NO_PERF_READ_VDSO32=1 NO_PERF_READ_VDSOX32=1} \
%endif
	%{?with_gtk:GTK2=1} \
	%{!?with_libunwind:NO_LIBUNWIND=1} \
	%{makeopts} \
	EXTRA_CFLAGS="%{rpmcflags}" \
	VF=1 \
	WERROR=0 \
	prefix=%{_prefix} \
	perfexecdir=%{_libdir}/perf-core \
	lib=%{_lib} \
	template_dir=%{_datadir}/perf-core/templates
%endif

# cpupower
%if %{with cpupower}
%{__make} -C tools/power/cpupower \
	%{makeopts} \
	CPUFREQ_BENCH=false \
	OPTIMIZATION="%{rpmcflags}" \
	STRIPCMD=true

%ifarch %{ix86} x32
%{__make} -C tools/power/cpupower/debug/i386 centrino-decode powernow-k8-decode \
	%{makeopts} \
	CFLAGS="%{rpmcflags}"
%endif

%ifarch %{x8664} x32
%{__make} -C tools/power/cpupower/debug/x86_64 centrino-decode powernow-k8-decode \
	%{makeopts} \
	CFLAGS="%{rpmcflags}"
%endif
%endif

%ifarch %{ix86} %{x8664} x32
CFLAGS="%{rpmcflags}" \
%{__make} -C tools/power/x86/x86_energy_perf_policy \
	%{makeopts}

CFLAGS="%{rpmcflags}" \
%{__make} -C tools/power/x86/turbostat \
	%{makeopts}
%endif

%{__make} -C tools/thermal/tmon \
	%{makeopts} \
	OPTFLAGS="%{rpmcflags}"

# usbip-utils
%if %{with usbip}
cd tools/usb/usbip
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CFLAGS="%{rpmcflags} $Wstringop $Waddressof" \
	--disable-silent-rules \
	--with-usbids-dir=/lib/hwdata
%{__make}
cd ../../..
%endif

# page-types, slabinfo
%{__make} -C tools/mm page-types slabinfo \
	%{makeopts}
	CFLAGS="%{rpmcflags} -Wall -Wextra -I../lib"

# gen_init_cpio
%{__make} -C usr gen_init_cpio \
	%{makeopts} \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

cd linux-%{basever}

%if %{with cpupower}
%{__make} -C tools/power/cpupower install \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=%{_libdir} \
	mandir=%{_mandir} \
	CPUFREQ_BENCH=false

%find_lang cpupower
%{__mv} cpupower.lang ..

install -d $RPM_BUILD_ROOT{/etc/sysconfig,%{systemdunitdir}}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}/cpupower.service
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/cpupower
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/cpupower@.service

%ifarch %{ix86} x32
install -p tools/power/cpupower/debug/i386/{centrino,powernow-k8}-decode $RPM_BUILD_ROOT%{_bindir}
%endif
%ifarch %{x8664} x32
install -p tools/power/cpupower/debug/x86_64/{centrino,powernow-k8}-decode $RPM_BUILD_ROOT%{_bindir}
%endif
%endif

%if %{with perf}
%{__make} -C tools/perf install \
%ifarch %{x8664}
	IS_X86_64=1 \
	%{!?with_multilib:NO_PERF_READ_VDSO32=1 NO_PERF_READ_VDSOX32=1} \
%endif
	%{?with_gtk:GTK2=1} \
	%{!?with_libunwind:NO_LIBUNWIND=1} \
	%{makeopts} \
	EXTRA_CFLAGS="%{rpmcflags}" \
	WERROR=0 \
	prefix=%{_prefix} \
	perfexecdir=%{_libdir}/perf-core \
	template_dir=%{_datadir}/perf-core/templates \
	bash_compdir=%{bash_compdir} \
	lib=%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT

%py3_comp $RPM_BUILD_ROOT%{_libdir}/perf-core/scripts/python
%py3_ocomp $RPM_BUILD_ROOT%{_libdir}/perf-core/scripts/python

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/perf-core/tests
%endif

%if %{with usbip}
%{__make} -C tools/usb/usbip install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libusbip.la
%endif

install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man8}

install -p tools/laptop/dslm/dslm $RPM_BUILD_ROOT%{_sbindir}

install -p tools/gpio/lsgpio $RPM_BUILD_ROOT%{_bindir}

%ifarch %{ix86} %{x8664} x32
install -p tools/hv/hv_{fcopy_uio,kvp,vss}_daemon $RPM_BUILD_ROOT%{_sbindir}
# TODO: PLD-specific hv_get_dhcp_info,hv_get_dns_info,hv_set_ifconfig
%{__sed} -e '1s,/usr/bin/env python3,%{__python3},' tools/hv/lsvmbus >$RPM_BUILD_ROOT%{_bindir}/lsvmbus
chmod 755 $RPM_BUILD_ROOT%{_bindir}/lsvmbus
%endif

install -p tools/iio/{iio_event_monitor,iio_generic_buffer,lsiio} $RPM_BUILD_ROOT%{_bindir}

install -p tools/laptop/freefall/freefall $RPM_BUILD_ROOT%{_sbindir}

%{__make} -C tools/bpf install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	bash_compdir=$RPM_BUILD_ROOT%{bash_compdir} \
	%{?with_verbose:V=1}
%{__make} -C tools/bpf/bpftool doc-install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	%{?with_verbose:V=1}

install -p tools/thermal/tmon/tmon $RPM_BUILD_ROOT%{_bindir}
cp -p tools/thermal/tmon/tmon.8 $RPM_BUILD_ROOT%{_mandir}/man8

install -p tools/mm/slabinfo $RPM_BUILD_ROOT%{_bindir}
install -p tools/mm/page-types $RPM_BUILD_ROOT%{_sbindir}

%ifarch %{ix86} %{x8664} x32
install -d $RPM_BUILD_ROOT%{_mandir}/man8
%{__make} -C tools/power/x86/x86_energy_perf_policy install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C tools/power/x86/turbostat install \
	DESTDIR=$RPM_BUILD_ROOT
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

%post	-n usbip-libs -p /sbin/ldconfig
%postun	-n usbip-libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bpf_asm
%attr(755,root,root) %{_bindir}/bpf_dbg
%attr(755,root,root) %{_bindir}/bpf_jit_disasm
%attr(755,root,root) %{_bindir}/gen_init_cpio
%attr(755,root,root) %{_bindir}/iio_event_monitor
%attr(755,root,root) %{_bindir}/iio_generic_buffer
%attr(755,root,root) %{_bindir}/lsgpio
%attr(755,root,root) %{_bindir}/lsiio
%attr(755,root,root) %{_bindir}/slabinfo
%attr(755,root,root) %{_bindir}/tmon
%attr(755,root,root) %{_sbindir}/bpftool
%attr(755,root,root) %{_sbindir}/dslm
%attr(755,root,root) %{_sbindir}/freefall
%attr(755,root,root) %{_sbindir}/page-types
%{_mandir}/man8/bpftool*.8*
%{_mandir}/man8/tmon.8*
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
%{systemdunitdir}/cpupower@.service
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/cpupower

%files cpupower-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcpupower.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcpupower.so.1

%files cpupower-libs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%{_includedir}/cpuidle.h
%{_includedir}/powercap.h

%files -n bash-completion-cpupower
%defattr(644,root,root,755)
%{bash_compdir}/cpupower

%ifarch %{ix86} %{x8664} x32
%files hv
%defattr(644,root,root,755)
# TODO: PLDify these scripts and move to bindir
%doc linux-%{basever}/tools/hv/hv_{get_dhcp_info,get_dns_info,set_ifconfig}.sh
%attr(755,root,root) %{_bindir}/lsvmbus
%attr(755,root,root) %{_sbindir}/hv_fcopy_uio_daemon
%attr(755,root,root) %{_sbindir}/hv_kvp_daemon
%attr(755,root,root) %{_sbindir}/hv_vss_daemon
%endif

%if %{with perf}
%files perf
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/perf
%attr(755,root,root) %{_bindir}/trace
%{_mandir}/man1/perf*.1*
%{_docdir}/perf-tip
%dir %{_datadir}/perf-core
%{_datadir}/perf-core/strace
%dir %{_libdir}/perf-core
%attr(755,root,root) %{_libdir}/perf-core/perf-archive
%attr(755,root,root) %{_libdir}/perf-core/perf-iostat
%dir %{_libdir}/perf-core/dlfilters
%attr(755,root,root) %{_libdir}/perf-core/dlfilters/dlfilter-show-cycles.so
%attr(755,root,root) %{_libdir}/perf-core/dlfilters/dlfilter-test-api-v0.so
%attr(755,root,root) %{_libdir}/perf-core/dlfilters/dlfilter-test-api-v2.so

%dir %{_libdir}/perf-core/scripts

%dir %{_libdir}/perf-core/scripts/perl
%dir %{_libdir}/perf-core/scripts/perl/Perf-Trace-Util
%dir %{_libdir}/perf-core/scripts/perl/Perf-Trace-Util/lib
%dir %{_libdir}/perf-core/scripts/perl/Perf-Trace-Util/lib/Perf
%dir %{_libdir}/perf-core/scripts/perl/Perf-Trace-Util/lib/Perf/Trace
%{_libdir}/perf-core/scripts/perl/Perf-Trace-Util/lib/Perf/Trace/*.pm
%dir %{_libdir}/perf-core/scripts/perl/bin
%attr(755,root,root) %{_libdir}/perf-core/scripts/perl/bin/*
%{_libdir}/perf-core/scripts/perl/*.pl

%dir %{_libdir}/perf-core/scripts/python
%dir %{_libdir}/perf-core/scripts/python/Perf-Trace-Util
%dir %{_libdir}/perf-core/scripts/python/Perf-Trace-Util/lib
%dir %{_libdir}/perf-core/scripts/python/Perf-Trace-Util/lib/Perf
%dir %{_libdir}/perf-core/scripts/python/Perf-Trace-Util/lib/Perf/Trace
%{_libdir}/perf-core/scripts/python/Perf-Trace-Util/lib/Perf/Trace/*.py
%dir %{_libdir}/perf-core/scripts/python/Perf-Trace-Util/lib/Perf/Trace/__pycache__
%{_libdir}/perf-core/scripts/python/Perf-Trace-Util/lib/Perf/Trace/__pycache__/*.py[co]
%dir %{_libdir}/perf-core/scripts/python/bin
%attr(755,root,root) %{_libdir}/perf-core/scripts/python/bin/*
%{_libdir}/perf-core/scripts/python/*.py
%dir %{_libdir}/perf-core/scripts/python/__pycache__
%{_libdir}/perf-core/scripts/python/__pycache__/*.py[co]

%{_includedir}/perf

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

%files -n bash-completion-kernel-tools
%defattr(644,root,root,755)
%{bash_compdir}/bpftool

%if %{with usbip}
%files -n usbip
%defattr(644,root,root,755)
%doc linux-%{basever}/tools/usb/usbip/{AUTHORS,README}
%attr(755,root,root) %{_sbindir}/usbip
%attr(755,root,root) %{_sbindir}/usbipd
%{_mandir}/man8/usbip.8*
%{_mandir}/man8/usbipd.8*

%files -n usbip-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libusbip.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libusbip.so.0

%files -n usbip-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libusbip.so
%{_includedir}/usbip

%files -n usbip-static
%defattr(644,root,root,755)
%{_libdir}/libusbip.a
%endif
