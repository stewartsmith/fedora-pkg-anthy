%define use_utf8_dict 1
%define pkg  anthy

Name:  anthy
Version: 9100h
Release: 21%{?dist}
# The entire source code is LGPLv2+ and dictionaries is GPLv2. the corpus data is under Public Domain.
License: LGPLv2+ and GPLv2 and Public Domain
URL:  http://sourceforge.jp/projects/anthy/
BuildRequires: emacs
%if 0%{?rhel} == 0
BuildRequires: xemacs
%endif

Source0: http://osdn.dl.sourceforge.jp/anthy/37536/anthy-%{version}.tar.gz
Source1: anthy-init.el
Patch0:  anthy-fix-typo-in-dict.patch
Patch1:  anthy-fix-typo-in-dict-name.patch
Patch10: anthy-corpus.patch
Patch11: anthy-fix-elisp.patch

Summary: Japanese character set input library
Group:  System Environment/Libraries

%description
Anthy provides the library to input Japanese on the applications, such as
X applications and emacs. and the user dictionaries and the users information
which is used for the conversion, is stored into their own home directory.
So Anthy is secure than other conversion server.

%package devel
Summary: Header files and library for developing programs which uses Anthy
Group:  Development/Libraries
Requires: anthy = %{version}-%{release}
Requires: pkgconfig

%description devel
The anthy-devel package contains the development files which is needed to build
the programs which uses Anthy.

%package -n emacs-%{pkg}
Summary: Compiled elisp files to run Anthy under GNU Emacs
Group:  System Environment/Libraries
Requires: emacs(bin) >= %{_emacs_version}
Requires: anthy = %{version}-%{release}
BuildArch: noarch

%description -n emacs-%{pkg}
This package contains the byte compiled elisp packages to run Anthy with GNU
Emacs.

%package -n emacs-%{pkg}-el
Summary: Elisp source files for Anthy under GNU Emacs
Group:  System Environment/Libraries
Requires: emacs-%{pkg} = %{version}-%{release}
BuildArch: noarch

%description -n emacs-%{pkg}-el
This package contains the elisp source files for Anthy under GNU Emacs. You
do not need to install this package to run Anthy. Install the emacs-%{pkg}
package to use Anthy with GNU Emacs.

%if 0%{?rhel} == 0
%package -n xemacs-%{pkg}
Summary: Compiled elisp files to run Anthy under XEmacs
Group:  System Environment/Libraries
Requires: xemacs(bin) >= %{_xemacs_version}
Requires: anthy = %{version}-%{release}
BuildArch: noarch

%description -n xemacs-%{pkg}
This package contains the byte compiled elisp packages to use Anthy with
XEmacs.

%package -n xemacs-%{pkg}-el
Summary: Elisp source files for Anthy under XEmacs
Group:  System Environment/Libraries
Requires: xemacs-%{pkg} = %{version}-%{release}
BuildArch: noarch

%description -n xemacs-%{pkg}-el
This package contains the elisp source files for Anthy under XEmacs. You do
not need to install this package to run Anthy. Install the xemacs-%{pkg}
package to use Anthy with XEmacs.
%endif


%prep
%setup -q #-a 2
%patch0 -p1 -b .0-typo
%patch1 -p1 -b .1-typo-name
%patch10 -p1 -b .10-corpus
%patch11 -p1 -b .11-elisp

# Convert to utf-8
for file in ChangeLog doc/protocol.txt; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%if %{use_utf8_dict}
function normalize_extra_dict() {
 sed -e 's/^\([^  ]*\)t[  ]*\(#[A-Z0-9\*]*\)[  ]*\([^  ]*\)$/\1 \2 \3/g' $1 > $1.norm
}
function dict_conv() {
 iconv -f euc-jp -t utf-8 $1 > $1.utf8
}
function gen_dict_args() {
 if ! test -f $RPM_BUILD_DIR/%{name}-%{version}/mkworddic/dict.args.in-orig; then
  cp -a $RPM_BUILD_DIR/%{name}-%{version}/mkworddic/dict.args.in{,-orig}
 fi
 cat <<_EOF_ > $RPM_BUILD_DIR/%{name}-%{version}/mkworddic/dict.args.in
# Generated by rpm script
set_input_encoding utf8
read @top_srcdir@/alt-cannadic/gcanna.ctd.utf8
read @top_srcdir@/alt-cannadic/gcannaf.ctd.utf8
read @top_srcdir@/alt-cannadic/gtankan.ctd.utf8
read @top_srcdir@/alt-cannadic/extra/g-jiritu-34.t.norm
read @top_srcdir@/alt-cannadic/extra/gc-fullname-34.t.norm
read @top_srcdir@/alt-cannadic/extra/gt-tankanji_kanji-34.t.norm
read @top_srcdir@/alt-cannadic/extra/gt-tankanji_hikanji-34.t.norm
read @top_srcdir@/alt-cannadic/extra/gf-fuzoku-34.t.norm
read @top_srcdir@/mkworddic/adjust.t.utf8
read @top_srcdir@/mkworddic/compound.t.utf8
read @top_srcdir@/mkworddic/extra.t.utf8
read @top_srcdir@/alt-cannadic/g_fname.t
#
build_reverse_dict
set_dict_encoding utf8
read_uc @top_srcdir@/mkworddic/udict.utf8
write anthy.wdic
done
_EOF_
touch -r $RPM_BUILD_DIR/%{name}-%{version}/mkworddic/dict.args.in{-orig,}
}

(
 cd alt-cannadic
 for i in gcanna.ctd gcannaf.ctd gtankan.ctd; do
  dict_conv $i
 done
 cd extra
 for i in g-jiritu-34.t gc-fullname-34.t gf-fuzoku-34.t gt-tankanji_hikanji-34.t gt-tankanji_kanji-34.t; do
  normalize_extra_dict $i
 done
);(
 cd mkworddic
 for i in adjust.t compound.t extra.t udict zipcode.t; do
  dict_conv $i
 done
)
gen_dict_args
%endif


%build
%configure --disable-static
# fix rpath issue
sed -ie 's/^hardcode_libdir_flag_spec.*$'/'hardcode_libdir_flag_spec=" -D__LIBTOOL_IS_A_FOOL__ "/' libtool
LD_LIBRARY_PATH=$RPM_BUILD_DIR/%{name}-%{version}/src-main/.libs:$RPM_BUILD_DIR/%{name}-%{version}/src-worddic/.libs make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# remove unnecessary files
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.{la,a}

## for emacs-anthy
%__mkdir_p $RPM_BUILD_ROOT%{_emacs_sitestartdir}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_emacs_sitestartdir}

%if 0%{?rhel} == 0
## for xemacs-anthy
%__mkdir_p $RPM_BUILD_ROOT%{_xemacs_sitestartdir}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_xemacs_sitestartdir}
pushd $RPM_BUILD_DIR/%{name}-%{version}/src-util
make clean
make EMACS=xemacs lispdir="%{_xemacs_sitelispdir}/%{pkg}"
make install-lispLISP DESTDIR=$RPM_BUILD_ROOT EMACS=xemacs lispdir="%{_xemacs_sitelispdir}/%{pkg}"
popd
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr (-, root, root, -)
%doc AUTHORS COPYING ChangeLog DIARY NEWS README
%{_bindir}/*
%{_sysconfdir}/*
%{_libdir}/lib*.so.*
%{_datadir}/anthy/

%files devel
%defattr (-, root, root, -)
%doc doc/DICLIB doc/DICUTIL doc/GLOSSARY doc/GRAMMAR doc/GUIDE.english doc/ILIB doc/LEARNING doc/LIB doc/MISC doc/POS doc/SPLITTER doc/TESTING doc/protocol.txt
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%files -n emacs-%{pkg}
%defattr(-, root, root, -)
%doc doc/ELISP
%{_emacs_sitelispdir}/%{pkg}/*.elc
%{_emacs_sitestartdir}/*.el
%dir %{_emacs_sitelispdir}/%{pkg}

%files -n emacs-%{pkg}-el
%defattr(-, root, root, -)
%{_emacs_sitelispdir}/%{pkg}/*.el

%if 0%{?rhel} == 0
%files -n xemacs-%{pkg}
%defattr(-, root, root, -)
%doc doc/ELISP
%{_xemacs_sitelispdir}/%{pkg}/*.elc
%{_xemacs_sitestartdir}/*.el
%dir %{_xemacs_sitelispdir}/%{pkg}

%files -n xemacs-%{pkg}-el
%defattr(-, root, root, -)
%{_xemacs_sitelispdir}/%{pkg}/*.el
%endif

%changelog
* Fri Mar  8 2013 Akira TAGOH <tagoh@redhat.com> - 9100h-21
- Apply a patch from Mike FABIAN to get anthy.el working back on Emacs 24.3.1.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9100h-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Akira TAGOH <tagoh@redhat.com> - 9100h-19
- Update License tag.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9100h-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9100h-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9100h-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct  7 2010 Akira TAGOH <tagoh@redhat.com> - 9100h-15
- Fix a typo in the dictionary. (#629908)

* Mon Sep 27 2010 Akira TAGOH <tagoh@redhat.com> - 9100h-14
- spec file clean up (Parag AN, #552855)

* Thu Jun 24 2010 Akira TAGOH <tagoh@redhat.com> - 9100h-13
- build emacs-* packages as noarch.

* Mon May 10 2010 Akira TAGOH <tagoh@redhat.com> - 9100h-12
- Fix a typo in g_fname.t. (#584614)

* Mon Mar 15 2010 Akira TAGOH <tagoh@redhat.com> - 9100h-11
- enable UTF-8 dictionaries really.

* Sun Mar 14 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com>
- Update spec file to comply with Emacs add-on packaging guidelines (#573449)

* Mon Dec 21 2009 Akira TAGOH <tagoh@redhat.com> - 9100h-10
- Fix more typos in dictionary. (#548078)
- correct the source URL.

* Thu Sep  3 2009 Dennis Gregorovic <dgregor@redhat.com> - 9100h-9
- Do not build against xemacs on RHEL

* Fri Aug 28 2009 Akira TAGOH <tagoh@redhat.com> - 9100h-8
- Fix more typos in dictionary. (#519769)

* Thu Aug 20 2009 Akira TAGOH <tagoh@redhat.com> - 9100h-7
- Stop updating corpus at the build time to avoid creating different dictionary
  among arch. (#816563)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9100h-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  8 2009 Akira TAGOH <tagoh@redhat.com> - 9100h-5
- Update the corpus.
- Fix typos in dictionary. (#509534)

* Mon May 11 2009 Akira TAGOH <tagoh@redhat.com> - 9100h-4
- Take off the ownership of %%{_libdir}/pkgconfig. (#499663)
- Add R: pkgconfig to -devel.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9100h-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Akira TAGOH <tagoh@redhat.com> - 9100h-1
- New upstream release.

* Fri Feb  6 2009 Akira TAGOH <tagoh@redhat.com> - 9100g-2
- Apply a patch reported upstream to fix dictionary's indexing.

* Wed Feb  4 2009 Akira TAGOH <tagoh@redhat.com> - 9100g-1
- New upstream release.
- convert all words in dictionaries to UTF-8.
- Rename anthy-el and anthy-el-xemacs to emacs-anthy{,-el} and xemacs-anthy{,-el}.
- Fix RPATH issue.
- Support words for JIS X 0213:2004 in dictionary. (#195437)

* Fri Nov 21 2008 Akira TAGOH <tagoh@redhat.com> - 9100e-4
- Fix a source URL.

* Fri Jun 27 2008 Akira TAGOH <tagoh@redhat.com> - 9100e-3
- Fix a segfault with some words containing vu. (#452779)

* Tue Feb 12 2008 Akira TAGOH <tagoh@redhat.com> - 9100e-2
- Rebuild for gcc-4.3.

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

