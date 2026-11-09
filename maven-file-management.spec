Name:		maven-file-management
Version:	3.2.0
Release:	1
Epoch:		1
Summary:	Maven File Management API
Group:		Development/Java
License:	Apache-2.0
URL:		https://maven.apache.org/shared/file-management/
Source0:	https://github.com/apache/maven-file-management/archive/refs/tags/v%{version}.tar.gz#/maven-file-management-%{version}.tar.gz
# Modello is not packaged. These classes are the 3.2.0 generated sources.
Patch0:		modello-sources.patch
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	mvn(commons-io:commons-io)
BuildRequires:	apache-commons-io >= 1:2.22.0
Requires:	apache-commons-io >= 1:2.22.0
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	plexus-utils >= 3.6.2
Requires:	plexus-utils >= 3.6.2
BuildRequires:	mvn(org.slf4j:slf4j-api)
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

Obsoletes:	maven-shared-file-management < %{EVRD}
Provides:	maven-shared-file-management = %{EVRD}
Obsoletes:	maven-file-management-javadoc < %{EVRD}
Obsoletes:	maven-shared-file-management-javadoc < %{EVRD}

%description
Resolves the files selected by a Maven file set and maps their paths.
3.2.0 deletes through commons-io and handles symlinks with java.nio.
The model classes are the Modello 2.4.0 sources. Tests are not run.

%prep
%autosetup -n maven-file-management-%{version} -p1
rm -rf src/test .github src/site
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
add(root, "groupId", "org.apache.maven.shared")
add(root, "artifactId", "file-management")
add(root, "version", "%{version}")
add(root, "name", "Apache Maven File Management API")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
deps = ET.SubElement(root, tag("dependencies"))
for group, artifact, version in (
    ("commons-io", "commons-io", "2.22.0"),
    ("org.codehaus.plexus", "plexus-utils", "3.6.2"),
    ("org.slf4j", "slf4j-api", "1.7.36"),
):
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY

%files -f .mfiles
%doc LICENSE NOTICE README.md
