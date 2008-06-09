%define name 	libungif
%define fakename ungif
%define version	4.1.4
%define majver 	4
%define major 	4
%define libname %mklibname %{fakename} %{major}

Name: 		%{name}
Summary: 	A library for manipulating GIF format image files
Version: 	%{version}
Release: 	%mkrel 5
License: 	MIT
URL: 		http://sourceforge.net/projects/libungif/
Source0: 	%{name}-%{version}.tar.bz2
Source1: 	%{name}-3.1.0.tar.bz2
# from https://secure.renaissoft.com/maia/wiki/FuzzyOCR23
# see http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=384773
Patch0:		http://users.own-hero.net/~decoder/fuzzyocr/giftext-segfault.patch
Group: 		System/Libraries
BuildRequires: 	X11-devel netpbm-devel
Buildroot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
# The following libgif.so handles packages built against the
# previous broken giflib package
Provides: 	libgif.so.4 libgif.so.3 libgif.so libungif.so giflib
Obsoletes: 	giflib

%description
The libungif package contains a shared library of functions for loading
and saving GIF format image files.  The libungif library can load any
GIF file, but it will save GIFs only in uncompressed format (i.e., it
won't use the patented LZW compression used to save "normal" compressed
GIF files).

Install the libungif package if you need to manipulate GIF files.  You
should also install the libungif-progs package.

%package -n	%{libname}
Summary:	A library for manipulating GIF format image files
Group:		System/Libraries
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
The libungif package contains a shared library of functions for loading
and saving GIF format image files.  The libungif library can load any
GIF file, but it will save GIFs only in uncompressed format (i.e., it
won't use the patented LZW compression used to save "normal" compressed
GIF files).

Install the libungif package if you need to manipulate GIF files.  You
should also install the libungif-progs package.

%package -n	%{libname}-devel
Summary:	Development tools for programs which will use the libungif library
Group:		Development/C
Requires:	%{libname} = %{version}
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	ungif-devel = %{version}-%{release}

%description -n	%{libname}-devel
This package contains the header files and documentation
necessary for development of programs that will use the libungif library
to load and save GIF format image files.

You should install this package if you need to develop programs which
will use the libungif library functions for loading and saving GIF format
image files.  You'll also need to install the libungif package.

%package -n	%{libname}-static-devel
Summary:	Static libraries for programs which will use the libungif library
Group:		Development/C
Requires:	%{libname}-devel = %{version}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	ungif-static-devel = %{version}-%{release}

%description -n	%{libname}-static-devel
This package contains the static libraries, necessary for development of 
programs that will use the libungif library
to load and save GIF format image files.

You should install this package if you need to develop programs which
will use the libungif library functions for loading and saving GIF format
image files.  You'll also need to install the libungif package.

%package	progs
Summary:	Programs for manipulating GIF format image files
Group:		Graphics
Requires:	%{libname} = %{version}

%description	progs
The libungif-progs package contains various programs for manipulating
GIF format image files.

Install this package if you need to manipulate GIF format image files.
You'll also need to install the libungif package.

%prep
%setup -q -a 1 -n %{name}-%{version}
pushd util
%patch0 -p0 -b .giftext
popd

%build
%configure2_5x
%make all

pushd %{name}-3.1.0
rm -f configure
test -x ./autogen.sh && ./autogen.sh
libtoolize --copy --force
%configure2_5x
%make all
popd

%install
rm -rf %buildroot

pushd %{name}-3.1.0/lib
%makeinstall
ln -sf libungif.so.3.1.0 %buildroot/%{_libdir}/libgif.so.3.1.0
ln -sf libgif.so.3.1.0   %buildroot/%{_libdir}/libgif.so.3
rm %buildroot/%{_libdir}/*.so
rm %buildroot/%{_libdir}/*.a
popd
 
%makeinstall
ln -sf libungif.so.%version	%buildroot/%_libdir/libgif.so.%version
ln -sf libgif.so.%version 	%buildroot/%_libdir/libgif.so.4
ln -sf libgif.so.4 		%buildroot/%_libdir/libgif.so
ln -sf libungif.a 		%buildroot/%_libdir/libgif.a
  
chmod 755 %buildroot/%_libdir/*.so*
chmod 644 %buildroot/%_libdir/*.a*
chmod 644 COPYING README UNCOMPRESSED_GIF NEWS ONEWS
chmod 644 doc/* util/giffiltr.c util/gifspnge.c

%clean
rm -rf %buildroot

%if %mdkversion < 200900
%post -n %libname   -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files -n %libname
%defattr(-,root,root)
%doc COPYING README UNCOMPRESSED_GIF NEWS ONEWS
%{_libdir}/lib*.so.*

%files -n %libname-devel
%defattr(-,root,root)
%doc doc/*  util/giffiltr.c util/gifspnge.c
%{_libdir}/lib*.so
%{_includedir}/*.h
%{_libdir}/lib*.la

%files -n %libname-static-devel
%defattr(-,root,root)
%doc COPYING
%{_libdir}/lib*.a


%files progs
%defattr(-,root,root)
%{_bindir}/*
%doc doc UNCOMPRESSED_GIF COPYING

