# Acmeair

## Intruduction

An implementation of the Acme Air sample application for NodeJS

## Preparation

A fully compliant Java 7 (or later) Runtime Environment is required for Apache JMeter to execute

Example:
1. Download JDK7
2. Config environment variable:

```text
   export JAVA_HOME=/opt/jdk1.7
   export JRE_HOME=$JAVA_HOME/jre
   export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
   export PATH=$JAVA_HOME/bin:$PATH
```

## Run shell

### Run setupJmeter.sh

The setupJmeter.sh needs to be executed in three steps:
1. Execute to the "git clone https://github.com/acmeair/acmeair-driver" and "git checkout ..." then suspend

2. Get into the file "acmeair-driver" and add the following contents at the end of the file "gradle.properties":
```text
   systemProp.http.proxyHost=child-prc.intel.com
   systemProp.http.proxyPort=913
   systemProp.http.nonProxyHosts=*.nonproxyrepos.com|localhost
   systemProp.https.proxyHost=child-prc.intel.com
   systemProp.https.proxyPort=913
   systemProp.https.nonProxyHosts=*.nonproxyrepos.com|localhost
```

3. Modify the file "build.gradle" and use the following  "repositories" instead:
```text
   repositories {
      maven {
         url "http://repo1.maven.org/maven2/"
      }
   }
```
4. After that,we can go on executing the remaining shell

### Run run_acmeair.sh

1. Before running run_acmeair.sh,you should install the math tool "bc":
```shell
   sudo apt-get install bc
```
2. Get into the file "acmeair-nodejs" then need to upgrade mongodb to the latest version in npm list
3. Get into the file "loaddb.sh" and set the "--no-proxy" mode at the end of url:
```text
   http://${host}:${port}/rest/api/loader/load?numCustomers=10000 --no-proxy
```
4. Run the run_acmeair.sh
