%define	version		6801

Name:		anthy
Version:	%{version}
Release:	1
License:	GPL
URL:		http://sourceforge.jp/projects/anthy/
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	emacs
#BuildRequires:	xemacs

Source0:	http://prdownloads.sourceforge.jp/anthy/9723/anthy-%{version}.tar.gz
Source1:	anthy-init.el

Summary:	Japanese character set input library
Group:		System Environment/Libraries
Obsoletes:	anthy-libs
Provides:	anthy-libs = %{name}-%{version}
%description
Anthy provides the library to input Japanese on the applications, such as
X applications and emacs. and the user dictionaries and the users information
which is used for the conversion, is stored into their own home directory.
So Anthy is secure than other conversion server.

%package	devel
Summary:	Header files and library for developing programs which uses Anthy
Group:		Development/Libraries
Requires:	anthy = %{version}-%{release}
%description	devel
The anthy-devel package contains the development files which is needed to build
the programs which uses Anthy.

%package	el
Summary:	Emacs Lisp files to use Anthy on Emacs
Group:		System Environment/Libraries
Requires:	emacs
Requires:	anthy = %{version}-%{release}
%description	el
The anthy-el package contains the emacs lisp to be able to input Japanese
character set on Emacs.

#%%package	el-xemacs
#Summary:	Emacs Lisp files to use Anthy on XEmacs
#Group:		System Environment/Libraries
#Requires:	xemacs
#Requires:	anthy = %{version}-%{release}
#%description	el-xemacs
#The anthy-el-xemacs package contains the emacs lisp to be able to input Japanese
#character set on XEmacs.

%prep
%setup -q

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

## for anthy-el
%__mkdir_p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d

## for anthy-el-xemacs
#%%__mkdir_p $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lisp/site-start.d
#install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lisp/site-start.d
#pushd $RPM_BUILD_DIR/%{name}-%{version}/src-util
#make clean
#make EMACS=xemacs lispdir="\${datadir}/xemacs/xemacs-packages/lisp/anthy"
#make install-lispLISP DESTDIR=$RPM_BUILD_ROOT EMACS=xemacs lispdir="\${datadir}/xemacs/xemacs-packages/lisp/anthy"
#popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog DIARY NEWS README doc
%{_bindir}/*
%{_sysconfdir}/*
%{_libdir}/lib*.so.*
%{_datadir}/anthy/

%files devel
%defattr (-, root, root)
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/pkgconfig

%files el
%defattr (-, root, root)
%{_datadir}/emacs/site-lisp/anthy/
%{_datadir}/emacs/site-lisp/site-start.d/anthy-init.el

#%%files el-xemacs
#%%defattr (-, root, root)
#%%{_datadir}/xemacs/xemacs-packages/lisp/anthy/
#%%{_datadir}/xemacs/site-packages/lisp/site-start.d/anthy-init.el

%changelog
* Wed Aug 24 2005 Akira TAGOH <tagoh@redhat.com> - 6801-1
- updates to the snapshot version.

* Tue Aug  9 2005 Akira TAGOH <tagoh@redhat.com>
- added dist tag in Release.

* Mon Aug  1 2005 Akira TAGOH <tagoh@redhat.com> - 6700b-2
- added Provides: anthy-libs = %%{name}-%%{version}

* Fri Jul 29 2005 Akira TAGOH <tagoh@redhat.com> - 6700b-1
- New upstream release.
- Import into Core.
- includes the libraries into anthy and added Obsoletes: anthy-libs.

* Wed Jun 29 2005 Akira TAGOH <tagoh@redhat.com> - 6700-1
- New upstream release.

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 6300d-3
- include anthy datadir in main package, and anthy site directory
  in -el and -el-xemacs packages

* Sun Mar 27 2005 Akira TAGOH <tagoh@redhat.com> - 6300d-2
- real updates (#152203)

* Sun Mar 20 2005 Akira TAGOH <tagoh@redhat.com> - 6300d-1
- New upstream release.

* Thu Feb 24 2005 Akira TAGOH <tagoh@redhat.com> - 6131-1
- New upstream release.

* Wed Jan 12 2005 Akira TAGOH <tagoh@redhat.com> - 6024-1
- New upstream release.

* Wed Sep 08 2004 Akira TAGOH <tagoh@redhat.com> 5704-1
- New upstream release.

* Mon Jul 05 2004 Akira TAGOH <tagoh@redhat.com> 5500-1
- New upstream release.

* Wed Jun 23 2004 Akira TAGOH <tagoh@redhat.com> 5414-1
- New upstream release.

* Tue Jun 08 2004 Akira TAGOH <tagoh@redhat.com> 5406-1
- New upstream release.

* Fri Jun 04 2004 Warren Togami <wtogami@redhat.com> 5330-3
- some spec cleanups

* Tue Jun 01 2004 Akira TAGOH <tagoh@redhat.com> 5330-2
- anthy-init.el: add some elisp to configure anthy.

* Tue Jun 01 2004 Akira TAGOH <tagoh@redhat.com> 5330-1
- Initial package.

