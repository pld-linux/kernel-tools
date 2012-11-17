#
# Conditional build:
%bcond_without	verbose		# verbose build (V=1)

%define		rel		0.1
%define		basever	3.6
%define		postver	.6
Summary:	Assortment of tools for the Linux kernel
Name:		kernel-tools
Version:	%{basever}%{postver}
Release:	%{rel}
License:	GPL v2
Group:		Base
Source0:	http://www.kernel.org/pub/linux/kernel/v3.x/linux-%{basever}.tar.xz
# Source0-md5:	1a1760420eac802c541a20ab51a093d1
%if "%{postver}" != ".0"
Patch0:		http://www.kernel.org/pub/linux/kernel/v3.x/patch-%{version}.bz2
# Patch0-md5:	363e730147333182616cc687345e7fe2
%endif
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Provides:	cpufreq-utils = 1:009-0.6.p1
Provides:	cpufrequtils = 1:009-0.6.p1
Provides:	cpupowerutils = 1:009-0.6.p1
Obsoletes:	cpufreq-utils < 1:009-0.6.p1
Obsoletes:	cpufrequtils < 1:009-0.6.p1
Obsoletes:	cpupowerutils < 1:009-0.6.p1
Obsoletes:	cpuspeed < 1:1.5-16
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the tools/ directory from the kernel source and
the supporting documentation.

%package libs
Summary:	Libraries for the kernels-tools
License:	GPL v2
Group:		Libraries

%description libs
This package contains the libraries built from the tools/ directory
from the kernel source.

%package libs-devel
Summary:	Assortment of tools for the Linux kernel
License:	GPL v2
Group:		Development/Libraries
Requires:	kernel-tools = %{version}-%{release}
Requires:	kernel-tools-libs = %{version}-%{release}
Provides:	cpupowerutils-devel = 1:009-0.6.p1
Provides:	kernel-tools-devel
Obsoletes:	cpupowerutils-devel < 1:009-0.6.p1

%description libs-devel
This package contains the development files for the tools/ directory
from the kernel source.

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
	CC="%{__cc}" \
	%{?with_verbose:V=1} \
	CPUFREQ_BENCH=false

%ifarch %{ix86}
%{__make} -C tools/power/cpupower/debug/i386 centrino-decode powernow-k8-decode \
	CC="%{__cc}" \
	%{?with_verbose:V=1}
%endif

%ifarch %{x8664}
%{__make} -C tools/power/cpupower/debug/x86_64 centrino-decode powernow-k8-decode \
	CC="%{__cc}" \
	%{?with_verbose:V=1}
%endif

%ifarch %{ix86} %{x8664}
%{__make} -C tools/power/x86/x86_energy_perf_policy \
	CC="%{__cc}" \
	%{?with_verbose:V=1}
%{__make} -C tools/power/x86/turbostat \
	CC="%{__cc}" \
	%{?with_verbose:V=1}
%endif

%install
rm -rf $RPM_BUILD_ROOT
cd linux-%{basever}

%{__make} -C tools/power/cpupower  install \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=%{_libdir} \
	mandir=%{_mandir} \
	CPUFREQ_BENCH=false

%find_lang cpupower
mv cpupower.lang ..

%ifarch %{ix86}
cd tools/power/cpupower/debug/i386
install -p centrino-decode $RPM_BUILD_ROOT%{_bindir}/centrino-decode
install -p powernow-k8-decode $RPM_BUILD_ROOT%{_bindir}/powernow-k8-decode
cd -
%endif
%ifarch %{x8664}
cd tools/power/cpupower/debug/x86_64
install -p centrino-decode $RPM_BUILD_ROOT%{_bindir}/centrino-decode
install -p powernow-k8-decode $RPM_BUILD_ROOT%{_bindir}/powernow-k8-decode
cd -
%endif

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
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f cpupower.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cpupower
%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{_bindir}/centrino-decode
%attr(755,root,root) %{_bindir}/powernow-k8-decode
%endif
%{_mandir}/man[1-8]/cpupower*
%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{_bindir}/turbostat
%attr(755,root,root) %{_bindir}/x86_energy_perf_policy
%{_mandir}/man8/turbostat*
%{_mandir}/man8/x86_energy_perf_policy*
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcpupower.so.*.*.*
%ghost %{_libdir}/libcpupower.so.0

%files libs-devel
%defattr(644,root,root,755)
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
