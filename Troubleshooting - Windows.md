## Troubleshooting for set-up installation on Windows platform.


Q: I encountered following warnings when trying to install gulp, what should I do?

	return process.dlopen(module, path._makeLong(filename));
                 ^
	Error: %1 is not a valid Win32 application.

A: Try run ```bash npm rebuild node-sass```, note that certain steps may take longer than expected so be patient. Read the error information. Based on previous experiences, you might be missing a Windows 8.1 sdk, or related Visual Studio C++ environment.



Q: I'm trying to download the .sql file into the MySQL Server 5.7\bin\ folder but it syas i need administrator permission, what should I do?

A: Download the .sql file to another folder and copy/cut and paste into the \bin\ folder, this way you'll be asked to given Administrator permission.


Q: I encountered following warnings when trying to install gulp, what should I do?

SKIPPING OPTIONAL DEPENDENCY: fsevents@^1.0.0 (node_modules\chokidar\node_modules\fsevents)
wanted {"os":"darwin","arch":"any"} (current: {"os":"win32","arch":"ia32"})

A: Ignore these warning messages. Fsevents was built for MacOS, this shouldn't have any actual impact on your installation.


Q: I encountered following errors:

  C:\Program Files (x86)\MSBuild\Microsoft.Cpp\v4.0\V140\Platforms\Win32\PlatformToolsets\v140\Toolset.targets(34,5): error MSB8036: The Windows SDK version
8.1 was not found. Install the required version of Windows SDK or change the SDK version in the project property pages or by right-clicking the solution and
selecting "Retarget solution". [C:\Users\Haoyuan\Documents\GitHub\ubyssey-dev\ubyssey-dispatch-theme\ubyssey\static\node_modules\node-sass\build\src\libsass.
vcxproj]

A: Install windows SDK 8.1.


Q:

Unhandled exception in thread started by <function wrapper at 0x00000000040BA6D8>
Traceback (most recent call last):

django.db.utils.OperationalError: (2003, "Can't connect to MySQL server on '127.0.0.1' (10061)")

A:

Check if your mySQL is running, if not, open the MySQL commandline and start the sql server. If that fails, it means that it might be corrupted and you might want to re-install it. If you do decide to re-install the MySQL server, after removing mySQL Server, remove mySQL57 Service before your reinstall it.

You can also try the following command under ubyssey\static\

```bash npm config set msvs_version 2015```


Q: I encountered these warning messages: 
```bash npm WARN deprecated minimatch@2.0.10: Please update to minimatch 3.0.2 or higher to avoid a RegExp DoS issue
npm WARN deprecated minimatch@0.2.14: Please update to minimatch 3.0.2 or higher to avoid a RegExp DoS issue
npm WARN deprecated graceful-fs@1.2.3: graceful-fs v3.0.0 and before will fail on node releases >= v7.0. Please update to graceful-fs@^4.0.0 as soon as possible. Use 'npm ls graceful-fs' to find it in the tree.```

A:

You could ignore these warning messages for now as they should not stop you from running the server. Minimatch developers decided to deprecate versions prior to 3.0.2 but all other packages will be kept up-to-date. Solutions to these problems will hopefully be released soon.
