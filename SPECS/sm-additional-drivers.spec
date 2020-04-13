Summary: Additional storage drivers for sm
Name:    sm-additional-drivers
Version: 0.4.0
Release: 1%{?dist}
License: LGPLv2
URL: https://github.com/xcp-ng/sm-additional-drivers
Source0: https://github.com/xcp-ng/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: python
Requires: sm
Requires: xapi-core
Requires: xfsprogs
Requires: ceph-common

%description
This package contains additional storage drivers for sm

%prep
%autosetup -p1

%build

%install
install -d -m 0755 %{buildroot}/opt/xensource/sm
install -m 0755 EXT4SR.py %{buildroot}/opt/xensource/sm
install -m 0755 XFSSR.py %{buildroot}/opt/xensource/sm
install -m 0755 CEPHFSSR.py %{buildroot}/opt/xensource/sm
pushd %{buildroot}/opt/xensource/sm
ln -s EXT4SR.py EXT4SR
ln -s XFSSR.py XFSSR
ln -s CEPHFSSR.py CEPHFSSR
popd

install -d -m 0755 %{buildroot}/etc/xapi.conf.d
touch %{buildroot}/etc/xapi.conf.d/sm-additional-drivers.conf

%triggerin -- xapi-core
# create configuration file from the whitelist in xapi.conf
WHITELIST_ORIG=$(grep /etc/xapi.conf -e "^sm-plugins=")
cat << EOF > /etc/xapi.conf.d/sm-additional-drivers.conf
# This overrides sm-plugins from xapi.conf to take additional storage drivers into account.
# This file is re-created each time either xapi-core or sm-additional-drivers is updated.
$WHITELIST_ORIG ext4 xfs cephfs
EOF

%postun
if [ $1 == 0 ]; then
    # remove .rpmsave file that could confuse xapi
    if [ -f /etc/xapi.conf.d/sm-additional-drivers.conf.rpmsave ]; then
        rm /etc/xapi.conf.d/sm-additional-drivers.conf.rpmsave
    fi
fi

%files
%doc LICENSE
/opt/xensource/sm/EXT4SR
/opt/xensource/sm/EXT4SR.py
/opt/xensource/sm/EXT4SR.pyc
/opt/xensource/sm/EXT4SR.pyo
/opt/xensource/sm/XFSSR
/opt/xensource/sm/XFSSR.py
/opt/xensource/sm/XFSSR.pyc
/opt/xensource/sm/XFSSR.pyo
/opt/xensource/sm/CEPHFSSR
/opt/xensource/sm/CEPHFSSR.py
/opt/xensource/sm/CEPHFSSR.pyc
/opt/xensource/sm/CEPHFSSR.pyo
# empty config file because it is written by scripts
# just listing it here to say we own it
%config /etc/xapi.conf.d/sm-additional-drivers.conf

%changelog
* Mon Apr 13 2020 Rushikesh Jadhav <rushikesh7@gmail.com> - 0.4.0-1
- Add experimental CEPH FS storage driver

* Thu Feb 20 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.3.0-1
- EXTSR now defaults to ext4 so EXT4SR is now deprecated
- Raise an exception if someone attempts to create a SR with type ext4
- Keep the EXT4SR driver for existing SRs... For now...

* Fri Dec 20 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.2.1-2
- Rebuild for XCP-ng 8.1

* Mon Jan 21 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.2.1-1
- Remove unknown -F parameter to mkfs.xfs

* Fri Jan 18 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.2.0-1
- Add experimental XFS storage driver

* Mon Jan 14 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.1.0-1
- Initial release with EXT4 storage driver
