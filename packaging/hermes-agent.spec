%global hermes_version %{?version}%{!?version:0}
Name:           hermes-agent
Version:        %{hermes_version}
Release:        1%{?dist}
Summary:        Native Hermes Agent runtime for Fedora CoreOS
License:        MIT
URL:            https://github.com/NousResearch/hermes-agent
Source0:        hermes-agent-%{version}.tar.gz
BuildArch:      x86_64
BuildRequires:  uv
Requires:       git
Requires:       nodejs
Requires:       ripgrep
Requires:       ffmpeg

%description
Hermes Agent with its current supported CPython runtime embedded in the RPM.
FCOS remains current; configuration, secrets, and mutable state are external.

%prep
%autosetup -n hermes-agent-%{version}

%build
mkdir runtime
uv python install --managed-python --install-dir runtime 3.13
python="$(find runtime -path '*/bin/python3' -executable | head -1)"
test -n "$python"
uv pip install --python "$python" .
mv runtime/cpython-* runtime/python

%install
install -d %{buildroot}%{_libexecdir}/hermes-agent
cp -a runtime/python %{buildroot}%{_libexecdir}/hermes-agent/runtime
install -d %{buildroot}%{_bindir}
printf '%s\n' '#!/bin/sh' 'exec %{_libexecdir}/hermes-agent/runtime/bin/hermes "$@"' > %{buildroot}%{_bindir}/hermes
chmod 0755 %{buildroot}%{_bindir}/hermes

%files
%license LICENSE
%{_bindir}/hermes
%{_libexecdir}/hermes-agent
