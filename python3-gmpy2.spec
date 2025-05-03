#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_with	tests	# unit tests (many inf or nan sign differences)

Summary:	Python interface to GMP/MPIR, MPFR and MPC libraries
Summary(pl.UTF-8):	Interfejs do bibliotek GMP/MPIR, MPFR oraz MPC
Name:		python3-gmpy2
Version:	2.2.0
Release:	1
License:	LGPL v3+
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/gmpy2/
Source0:	https://files.pythonhosted.org/packages/source/g/gmpy2/gmpy2-%{version}.tar.gz
# Source0-md5:	e5c732466cc422b929dfde92375bc4cc
URL:		https://pypi.org/project/gmpy2/
BuildRequires:	gmp-devel
BuildRequires:	libmpc-devel >= 1.0.3
BuildRequires:	mpfr-devel
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	libmpc >= 1.0.3
Requires:	python3-modules >= 1:3.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gmpy2 is an optimized, C-coded Python extension module that supports
fast multiple-precision arithmetic. gmpy2 is based on the original
gmpy module. gmpy2 adds support for correctly rounded
multiple-precision real arithmetic (using the MPFR library) and
complex arithmetic (using the MPC library).

%description -l pl.UTF-8
gmpy2 to zoptymalizowany, napisany w C moduł rozszerzenia Pythona,
obsługujący szybką arytmetykę wielokrotnej precyzji. Moduł gmpy2 jest
oparty na oryginalnym module gmpy. Dodaje obsługę poprawnie
zaokrąglanej arytmetyki rzeczywistej wielokrotnej precyzji (przy
użyciu biblioteki MPFR) oraz arytmetyki zespolonej (przy użyciu
biblioteki MPC).

%package apidocs
Summary:	API documentation for Python gmpy2 module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona gmpy2
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python gmpy2 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona gmpy2.

%prep
%setup -q -n gmpy2-%{version}

%build
%py3_build

%if %{with tests}
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(echo $PWD/build-3/*lib*) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%dir %{py3_sitedir}/gmpy2
%attr(755,root,root) %{py3_sitedir}/gmpy2/gmpy2.cpython-*.so
%{py3_sitedir}/gmpy2/__init__.py
%{py3_sitedir}/gmpy2/*.pxd
%{py3_sitedir}/gmpy2/gmpy2.h
%{py3_sitedir}/gmpy2/__pycache__
%{py3_sitedir}/gmpy2-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
