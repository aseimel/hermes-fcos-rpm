%global hermes_version %{?version}%{!?version:0}
%global debug_package %{nil}
%global __brp_mangle_shebangs %{nil}
Name:           hermes-agent
Version:        %{hermes_version}
Release:        1%{?dist}
Summary:        Native Hermes Agent runtime for Fedora CoreOS
License:        MIT
URL:            https://github.com/NousResearch/hermes-agent
Source0:        hermes-agent-%{version}.tar.gz
BuildArch:      x86_64
AutoReqProv:    no
BuildRequires:  uv
BuildRequires:  patchelf
Requires:       git
Requires:       nodejs
Requires:       ripgrep

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
uv pip install --break-system-packages --python "$python" .
runtime_dir="$(dirname "$(dirname "$python")")"
mv "$runtime_dir" runtime/python

%install
install -d %{buildroot}%{_libexecdir}/hermes-agent
cp -a runtime/python %{buildroot}%{_libexecdir}/hermes-agent/runtime
find %{buildroot}%{_libexecdir}/hermes-agent/runtime/lib -name 'libtcl*.so' -type f -exec patchelf --remove-rpath {} +
install -d %{buildroot}%{_bindir}
printf '%s\n' '#!/bin/sh' 'exec %{_libexecdir}/hermes-agent/runtime/bin/python3 -c "from hermes_cli.main import main; main()" "$@"' > %{buildroot}%{_bindir}/hermes
chmod 0755 %{buildroot}%{_bindir}/hermes

%files
%license LICENSE
%{_bindir}/hermes
%{_libexecdir}/hermes-agent
