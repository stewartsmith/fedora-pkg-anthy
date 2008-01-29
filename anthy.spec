Name:		anthy
Version:	9100e
Release:	1%{?dist}
# The entire source code is LGPLv2+ and dictionaries is GPLv2.
License:	LGPLv2+ and GPLv2
URL:		http://sourceforge.jp/projects/anthy/
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	automake autoconf
BuildRequires:	emacs
BuildRequires:	xemacs

Source0:	http://prdownloads.sourceforge.jp/anthy/29142/anthy-%{version}.tar.gz
Source1:	anthy-init.el

Summary:	Japanese character set input library
Group:		System Environment/Libraries
Obsoletes:	anthy-libs
Provides:	anthy-libs = %{version}
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

%package	el-xemacs
Summary:	Emacs Lisp files to use Anthy on XEmacs
Group:		System Environment/Libraries
Requires:	xemacs
Requires:	anthy = %{version}-%{release}
%description	el-xemacs
The anthy-el-xemacs package contains the emacs lisp to be able to input Japanese
character set on XEmacs.

%prep
%setup -q #-a 2
#cp alt-cannadic-%{altcannadicver}/* alt-cannadic/

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# remove unnecessary files
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.la

## for anthy-el
%__mkdir_p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d

## for anthy-el-xemacs
%__mkdir_p $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lisp/site-start.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lisp/site-start.d
pushd $RPM_BUILD_DIR/%{name}-%{version}/src-util
make clean
make EMACS=xemacs lispdir="\${datadir}/xemacs/xemacs-packages/lisp/anthy"
make install-lispLISP DESTDIR=$RPM_BUILD_ROOT EMACS=xemacs lispdir="\${datadir}/xemacs/xemacs-packages/lisp/anthy"
popd

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog DIARY NEWS README
%{_bindir}/*
%{_sysconfdir}/*
%{_libdir}/lib*.so.*
%{_datadir}/anthy/

%files devel
%defattr (-, root, root)
%doc doc/DICLIB doc/DICUTIL doc/GLOSSARY doc/GRAMMAR doc/GUIDE.english doc/ILIB doc/LEARNING doc/LIB doc/MISC doc/POS doc/SPLITTER doc/TESTING doc/protocol.txt
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig

%files el
%defattr (-, root, root)
%doc doc/ELISP
%{_datadir}/emacs/site-lisp/anthy/
%{_datadir}/emacs/site-lisp/site-start.d/anthy-init.el

%files el-xemacs
%defattr (-, root, root)
%doc doc/ELISP
%{_datadir}/xemacs/xemacs-packages/lisp/anthy/
%{_datadir}/xemacs/site-packages/lisp/site-start.d/anthy-init.el

%changelog
* Tue Jan 29 2008 Akira TAGOH <tagoh@redhat.com> - 9100e-1
- New upstream release.

* Mon Oct 29 2007 Akira TAGOH <tagoh@redhat.com> - 9100d-1
- New upstream release.
- anthy-enable-dict-gtankan.patch: removed. no need to be applied anymore.

* Tue Sep 18 2007 Akira TAGOH <tagoh@redhat.com> - 9100b-1
- New upstream release.

* Thu Aug 23 2007 Akira TAGOH <tagoh@redhat.com> - 9100-3
- Rebuild

* Wed Aug  8 2007 Akira TAGOH <tagoh@redhat.com> - 9100-2
- Update alt-cannadic to 070805.
- Use gtankan.ctd instead of tankanji.t.
- Update License tag.

* Tue Jul  3 2007 Akira TAGOH <tagoh@redhat.com> - 9100-1
- New upstream release.

* Wed Jun 13 2007 Akira TAGOH <tagoh@redhat.com> - 9011-1
- New upstream release

* Fri Jun  8 2007 Akira TAGOH <tagoh@redhat.com> - 9006-1
- New upstream release.
- Get back the anthy-el-xemacs package. (#243078)

* Fri Apr 27 2007 Akira TAGOH <tagoh@redhat.com> - 8706-2
- Fix wrong Provides line. (#237987)

* Fri Mar  9 2007 Akira TAGOH <tagoh@redhat.com> - 8706-1
- New upstream release.

* Mon Feb 26 2007 Akira TAGOH <tagoh@redhat.com> - 8622-1
- New upstream release.

* Mon Feb 19 2007 Akira TAGOH <tagoh@redhat.com> - 8616-1
- New upstream release.

* Tue Feb 13 2007 Akira TAGOH <tagoh@redhat.com> - 8607-1
- New upstream release.
- correct doc installation. (#228311)

* Tue Feb  6 2007 Akira TAGOH <tagoh@redhat.com> - 8604-1
- New upstream release.
- no longer needed to regenerate autotools files. (#224146)
- use original gcanna dict.
- build with --disable-static.

* Fri Aug 11 2006 Akira TAGOH <tagoh@redhat.com> - 7900-2
- anthy-7900-fix-undef-non-weak-symbol.patch: removed the unnecessary library
  chain.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 7900-1.1
- rebuild

* Tue Jul 11 2006 Akira TAGOH <tagoh@redhat.com> - 7900-1
- New upstream release.
- anthy-7900-fix-undef-non-weak-symbol.patch: fixed the undefined non-weak
  symbols issue. (#198180)
- use dist tag.

* Mon Jun 26 2006 Akira TAGOH <tagoh@redhat.com> - 7824-1
- New upstream snapshot release.

* Tue Jun 20 2006 Akira TAGOH <tagoh@redhat.com> - 7818-1
- New upstream snapshot release.

* Mon Jun 12 2006 Akira TAGOH <tagoh@redhat.com> - 7811-1
- New upstream snapshot release.
- use make install DESTDIR=... instead of %%makeinstall.

* Mon Jun  5 2006 Akira TAGOH <tagoh@redhat.com> - 7802-2
- exclude ppc64 to make anthy-el package. right now emacs.ppc64 isn't provided
  and buildsys became much stricter.

* Fri Jun  2 2006 Akira TAGOH <tagoh@redhat.com> - 7802-1
- New upstream snapshot release.

* Wed May 17 2006 Akira TAGOH <tagoh@redhat.com> - 7716-1
- New upstream snapshot release.

* Mon May 15 2006 Akira TAGOH <tagoh@redhat.com> - 7714-1
- New upstream snapshot release.

* Thu May 11 2006 Akira TAGOH <tagoh@redhat.com> - 7710-1
- New upstream snapshot release.

* Mon Apr 24 2006 Akira TAGOH <tagoh@redhat.com> - 7622-1
- New upstream snapshot release.
  - removed unnecessary patches:
    - anthy-2832.patch
    - anthy-2834.patch

* Fri Mar 17 2006 Akira TAGOH <tagoh@redhat.com> - 7500-1
- New upstream release.
  - larning words works now. (#178764)
- anthy-2832.patch: patch from upstream that fixes wrong order of candidate list.
- anthy-2834.patch: patch from upstream that fixes unexpected word segment.
- anthy-gcanna-nakaguro.patch: added a word to dictionary to convert nakaguro to slash.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 7100b-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 7100b-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Akira TAGOH <tagoh@redhat.com> - 7100b-2
- run ldconfig in %%post and %%postun. (#172768)

* Sat Nov  5 2005 Akira TAGOH <tagoh@redhat.com> - 7100b-1
- New upstream release.

* Mon Oct 31 2005 Akira TAGOH <tagoh@redhat.com> - 7029-1
- New upstream snapshot release.

* Fri Oct 14 2005 Akira TAGOH <tagoh@redhat.com> - 7015-1
- New upstream snapshot release.

* Thu Oct 13 2005 Akira TAGOH <tagoh@redhat.com> - 7013-1
- New upstream snapshot release.
- removed the patches:
  - anthy-add-placename-dict.patch: isn't needed anymore.
  - anthy_base.t.diff: merged into upstream.
  - zipcode-20050831.tar.bz2: merged into upstream.

* Wed Sep 21 2005 Akira TAGOH <tagoh@redhat.com> - 6829-3
- applied some patches from anthy-dev mailing list to improve the dictionaries.
  - anthy_base.t.diff
  - anthy_gcanna.ctd.diff
  - anthy_gcanna.ctd_20050918.diff
  - anthy_gcanna.ctd_20050920.diff
- parameterize anthy-el-xemacs build.

* Thu Sep  1 2005 Akira TAGOH <tagoh@redhat.com> - 6829-2
- Added the place name dictionary.

* Tue Aug 30 2005 Akira TAGOH <tagoh@redhat.com> - 6829-1
- New upstream snapshot release.

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

