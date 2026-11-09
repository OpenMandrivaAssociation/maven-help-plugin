Name:		maven-help-plugin
Version:	3.5.2
Release:	1
Summary:	Describes a Maven build, its plugins, and the effective model
Group:		Development/Java
License:	Apache-2.0
URL:		https://maven.apache.org/plugins/maven-help-plugin/
Source0:	https://github.com/apache/maven-help-plugin/archive/refs/tags/maven-help-plugin-%{version}.tar.gz#/maven-help-plugin-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	maven-components >= 3.10.0
BuildRequires:	java-current-devel
# Generates META-INF/maven/plugin.xml. The separate annotations package
# conflicts with maven-components on the same index file.
BuildRequires:	maven-plugin-tools >= 3.16.0
BuildRequires:	mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:	mvn(org.apache.maven.plugin-tools:maven-plugin-tools-generators)
BuildRequires:	mvn(org.apache.maven.shared:maven-shared-utils)
BuildRequires:	maven-shared-utils >= 3.5.0
Requires:	maven-shared-utils >= 3.5.0
BuildRequires:	mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:	maven-reporting-api >= 1:4.0.0
Requires:	maven-reporting-api >= 1:4.0.0
BuildRequires:	mvn(org.codehaus.plexus:plexus-interactivity-api)
BuildRequires:	plexus-interactivity-api >= 1.6.0
Requires:	plexus-interactivity-api >= 1.6.0
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
# plexus-xml is not packaged. The XML writers this plugin calls are in
# plexus-utils 3.6.2. 3.2.1 is still published and lacks them.
BuildRequires:	plexus-utils >= 3.6.2
Requires:	plexus-utils >= 3.6.2
BuildRequires:	mvn(org.jdom:jdom2)
BuildRequires:	jdom2 >= 2.0.6.1
Requires:	jdom2 >= 2.0.6.1
BuildRequires:	mvn(com.thoughtworks.xstream:xstream)
BuildRequires:	xstream >= 1.4.21
Requires:	xstream >= 1.4.21
BuildRequires:	mvn(org.apache.maven:maven-plugin-api)
BuildRequires:	mvn(org.apache.maven:maven-core)
BuildRequires:	mvn(org.apache.maven:maven-artifact)
BuildRequires:	mvn(org.apache.maven:maven-model)
BuildRequires:	mvn(org.apache.maven:maven-model-builder)
BuildRequires:	mvn(org.apache.maven:maven-settings)
BuildRequires:	mvn(org.apache.maven.resolver:maven-resolver-api)
BuildRequires:	mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:	mvn(javax.inject:javax.inject)
# javax.inject and jakarta-inject both provide this coordinate.
BuildRequires:	javax.inject >= 1-2
Requires:	javax.inject >= 1-2
BuildRequires:	mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

Obsoletes:	maven-help-plugin-javadoc < %{EVRD}

%description
Shows the effective POM and settings, evaluates expressions, and
describes plugins and their goals. 3.5.2 is the current stable
release. help:evaluate reads console input through the Plexus
interactivity API. Tests need JUnit Jupiter, so they are not run.

%prep
%autosetup -n maven-help-plugin-maven-help-plugin-%{version}
rm -rf src/test src/it .github Jenkinsfile
python - <<'PY'
import xml.etree.ElementTree as ET

NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.plugins")
add(root, "artifactId", "maven-help-plugin")
add(root, "version", "%{version}")
add(root, "packaging", "maven-plugin")
add(root, "name", "Apache Maven Help Plugin")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
deps = ET.SubElement(root, tag("dependencies"))
items = (
    ("org.apache.maven.plugin-tools", "maven-plugin-tools-generators", "3.16.0", None),
    ("org.apache.maven.shared", "maven-shared-utils", "3.5.0", None),
    ("org.apache.maven.reporting", "maven-reporting-api", "4.0.0", None),
    ("org.codehaus.plexus", "plexus-interactivity-api", "1.6.0", None),
    ("org.codehaus.plexus", "plexus-utils", "3.6.2", None),
    ("org.jdom", "jdom2", "2.0.6.1", None),
    ("com.thoughtworks.xstream", "xstream", "1.4.21", None),
    ("org.apache.maven", "maven-plugin-api", "3.10.0", "provided"),
    ("org.apache.maven", "maven-core", "3.10.0", "provided"),
    ("org.apache.maven", "maven-artifact", "3.10.0", "provided"),
    ("org.apache.maven", "maven-model", "3.10.0", "provided"),
    ("org.apache.maven", "maven-model-builder", "3.10.0", "provided"),
    ("org.apache.maven", "maven-settings", "3.10.0", "provided"),
    ("org.apache.maven.resolver", "maven-resolver-api", "2.0.24", "provided"),
    ("org.eclipse.sisu", "org.eclipse.sisu.plexus", "0.9.0.M3", "provided"),
    ("javax.inject", "javax.inject", "1", "provided"),
    ("org.apache.maven.plugin-tools", "maven-plugin-annotations", "3.15.2", "provided"),
)
for group, artifact, version, scope in items:
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
    if scope:
        add(dep, "scope", scope)
build = ET.SubElement(root, tag("build"))
plugins = ET.SubElement(build, tag("plugins"))
plugin = ET.SubElement(plugins, tag("plugin"))
add(plugin, "groupId", "org.apache.maven.plugins")
add(plugin, "artifactId", "maven-plugin-plugin")
add(plugin, "version", "3.16.0")
cfg = ET.SubElement(plugin, tag("configuration"))
# DescribeMojo calls HelpMojo.toLines. The generator's default package
# is the artifact id, so the class would not be visible here.
add(cfg, "helpPackageName", "org.apache.maven.plugins.help")
execs = ET.SubElement(plugin, tag("executions"))
execution = ET.SubElement(execs, tag("execution"))
add(execution, "id", "generate-helpmojo")
goals = ET.SubElement(execution, tag("goals"))
add(goals, "goal", "helpmojo")
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY

%files -f .mfiles
%doc LICENSE README.md
