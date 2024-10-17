%define name 	libungif
%define fakename ungif
%define version	4.1.4
%define majver 	4
%define major 	4
%define libname %mklibname %{fakename} %{major}

Name: 		%{name}
Summary: 	A library for manipulating GIF format image files
Version: 	%{version}
Release: 	%mkrel 9
License: 	MIT
URL: 		https://sourceforge.net/projects/libungif/
Source0: 	%{name}-%{version}.tar.bz2
Source1: 	%{name}-3.1.0.tar.bz2
# from https://secure.renaissoft.com/maia/wiki/FuzzyOCR23
# see http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=384773
Patch0:		http://users.own-hero.net/~decoder/fuzzyocr/giftext-segfault.patch
Patch1:		libungif-4.1.4-format_not_a_string_literal_and_no_format_arguments.diff
Group: 		System/Libraries
BuildRequires: 	X11-devel netpbm-devel
# The following libgif.so handles packages built against the
# previous broken giflib package
Provides: 	libgif.so.4 libgif.so.3 libgif.so libungif.so giflib
Obsoletes: 	giflib

%description
The libungif package contains a shared library of functions for loading
and saving GIF format image files.  The libungif library can load any
GIF file, but it will save GIFs only in uncompressed format (i.e., it
won't use the LZW compression used to save "normal" compressed GIF
files.  The reason for this was that the LZW compression was patented
in the past, but it fell in the public domain in 2004.  So now you can
use the libgif which does use this algorithm without any patent issue
in any country).

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
won't use the LZW compression used to save "normal" compressed GIF
files.  The reason for this was that the LZW compression was patented
in the past, but it fell in the public domain in 2004.  So now you can
use the libgif which does use this algorithm without any patent issue
in any country).

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

%setup -q -n %{name}-%{version} -a1

pushd util
%patch0 -p0 -b .giftext
popd

%patch1 -p1 -b .format_not_a_string_literal_and_no_format_arguments

%build
%configure2_5x
%make all

pushd %{name}-3.1.0
rm -f configure
autoreconf -fis
%configure2_5x
%make all
popd

%install
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

%files -n %libname
%doc COPYING README UNCOMPRESSED_GIF NEWS ONEWS
%{_libdir}/lib*.so.*

%files -n %libname-devel
%doc doc/*  util/giffiltr.c util/gifspnge.c
%{_libdir}/lib*.so
%{_includedir}/*.h

%files -n %libname-static-devel
%doc COPYING
%{_libdir}/lib*.a


%files progs
%{_bindir}/*
%doc doc UNCOMPRESSED_GIF COPYING

