%{?_javapackages_macros:%_javapackages_macros}
Name:           maven-help-plugin
Version:        2.2
Release:        6.3
Summary:        Plugin to to get relative information about a project or the system
Group:		Development/Java

License:        ASL 2.0
URL:            https://maven.apache.org/plugins/maven-help-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip
Patch0:         maven3-api-fixes.patch
Patch1:         reduce-exception.patch
BuildArch: noarch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: plexus-utils
BuildRequires: ant
BuildRequires: junit-addons
BuildRequires: maven-local
BuildRequires: maven-install-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-plugin-testing-harness
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: xstream
BuildRequires: jpackage-utils
BuildRequires: plexus-containers-component-metadata
BuildRequires: maven-plugin-tools-generators
Requires: ant
Requires: maven
Requires: jpackage-utils
Requires: java
Requires: xstream
Requires: maven-plugin-tools-generators

%description
The Maven Help Plugin is used to get relative information about a project
or the system. It can be used to get a description of a particular plugin,
including the plugin's mojos with their parameters and component requirements,
the effective POM and effective settings of the current build,
and the profiles applied to the current project being built.

%package javadoc

Summary:        Javadoc for %{name}
Requires: jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q
%patch0
%patch1

# Use compatibility API
%pom_remove_dep org.apache.maven:maven-plugin-parameter-documenter
%pom_add_dep org.apache.maven:maven-compat

# Add missing test deps
%pom_add_dep net.sf.cglib:cglib:any:test

# In newer versions of maven-plugin-tools the PluginUtils.toText()
# static method was moved to GeneratorUtils class.
%pom_add_dep org.apache.maven.plugin-tools:maven-plugin-tools-generators
sed -i "s|PluginUtils.toText|org.apache.maven.tools.plugin.generator.GeneratorUtils.toText|" \
    src/main/java/org/apache/maven/plugins/help/DescribeMojo.java

%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Mat Booth <fedora@matbooth.co.uk> - 2.2-1
- Update to latest upstream, fixes rhbz #915220
- Drop upstreamed plexus-containers-component-metadata patch
- No longer need missing package declaration workaround for HelpMojo.java

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-11
- Remove test dependencies from POM

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.1.1-9
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Jan  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-8
- Install license files, resolves: rhbz#879368
- Fix HelpMojo.java package declaration
- Add patch for compatibility with maven-plugin-tools-3.x

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Jaromir Capik <jcapik@redhat.com> 2.1.1-6
- Migration from plexus-maven-plugin to plexus-containers-component-metadata

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 6 2011 Alexander Kurtakov <akurtako@redhat.com> 2.1.1-4
- Fix build in pure maven 3 environment.

* Thu Jun 9 2011 Alexander Kurtakov <akurtako@redhat.com> 2.1.1-3
- Build with maven 3.x.
- Use upstream sources.
- Guidelines fixes.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 02 2010 Yong Yang <yyang@redhat.com> 2.1.1-1
- Initial package.
