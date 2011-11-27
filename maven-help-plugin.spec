Name:           maven-help-plugin
Version:        2.1.1
Release:        4
Summary:        Plugin to to get relative information about a project or the system

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-help-plugin/
# svn export http://svn.apache.org/repos/asf/maven/plugins/tags/maven-help-plugin-2.1.1/
# tar jcf maven-help-plugin-2.1.1.tar.bz2 maven-help-plugin-2.1.1
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}-jpp-depmap.xml
Patch0:         %{name}-pom.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: java-devel >= 0:1.6.0
BuildRequires: plexus-utils
BuildRequires: ant-nodeps
BuildRequires: maven2
BuildRequires: maven-install-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-plugin-testing-harness
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: xstream
BuildRequires: jpackage-utils
Requires: ant-nodeps
Requires: maven2
Requires: jpackage-utils
Requires: java
Requires: xstream
Requires(post): jpackage-utils
Requires(postun): jpackage-utils 

Obsoletes: maven2-plugin-help < 0:%{version}-%{release}
Provides: maven2-plugin-help = 0:%{version}-%{release}

%description
The Maven Help Plugin is used to get relative information about a project
 or the system. It can be used to get a description of a particular plugin, 
including the plugin's mojos with their parameters and component requirements,
the effective POM and effective settings of the current build, 
and the profiles applied to the current project being built.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires: jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q #You may need to update this according to your Source0
%patch0 -b .sav

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository

# no junit-addons, skip test
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE1} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        -Dmaven.test.failure.ignore=true \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.apache.maven.plugins %{name} %{version} JPP %{name}

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

