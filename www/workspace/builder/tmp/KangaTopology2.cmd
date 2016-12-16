set KANGA_HOME=C:\kanga_dev\sw
set NODE_HOME=%KANGA_HOME%\nodejs
set PYTHON_HOME=%KANGA_HOME%\Python27
set NPM_HOME=C:\Users\User\AppData\Roaming\npm;
set IDE_HOME=%KANGA_HOME%\kangaIDE
set IDE_LOG=%KANGA_HOME%\tmp\kangaIDE\logs\ide.log
set APACHE_HOME=%KANGA_HOME%\Apache24
set SQLITE_HOME=%KANGA_HOME%\sqlite3
set path=%PYTHON_HOME%;%NODE_HOME%;%NPM_HOME%\bin;%APACHE_HOME%\bin;%PYTHON_HOME%\SysWOW64;%SQLITE_HOME%;

cd C:\kanga_dev\sw\kangaIDE\workspace\builder\tmp
node C:\kanga_dev\sw\kangaIDE\workspace\builder\tmp\KangaTopology2.js
