%global hermes_version %{?version}%{!?version:0}
Name:           hermes-agent
Version:        %{hermes_version}
Release:        1%{?dist}
Summary:        Native Hermes Agent runtime for Fedora CoreOS
License:        MIT
URL:            https://github.com/NousResearch/hermes-agent
Source0:        hermes-agent-%{version}.tar.gz
BuildArch:      x86_64
BuildRequires:  python3-devel
BuildRequires:  python3-pip
Requires:       python3
Requires:       git
Requires:       nodejs
Requires:       ripgrep
Requires:       ffmpeg

%description
Hermes Agent installed as a native immutable-host runtime. Configuration,
secrets, and mutable state are supplied outside this package.

%prep
%autosetup -n hermes-agent-%{version}

%build
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install .

%install
install -d %{buildroot}%{_libexecdir}/hermes-agent
cp -a . %{buildroot}%{_libexecdir}/hermes-agent/source
install -d %{buildroot}%{_bindir}
printf '%s\n' '#!/bin/sh' 'exec %{_libexecdir}/hermes-agent/source/.venv/bin/hermes "$@"' > %{buildroot}%{_bindir}/hermes
chmod 0755 %{buildroot}%{_bindir}/hermes

%files
%license LICENSE
%{_bindir}/hermes
%{_libexecdir}/hermes-agent

%changelog
* Tue Jul 14 2026 Armin Seimel <armin.seimel@gesis.org> - %{version}-1
- Native FCOS Hermes Agent package
