# DO NOT EDIT
# This makefile makes sure all linkable targets are
# up-to-date with anything they link to
default:
	echo "Do not invoke directly"

# Rules to remove targets that are older than anything to which they
# link.  This forces Xcode to relink the targets from scratch.  It
# does not seem to check these dependencies itself.
PostBuild.simple_query.Debug:
/Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_query/build/Debug/simple_query:\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusIdx.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDb.dylib\
	/Library/Frameworks/Python.framework/Versions/3.6/lib/libpython3.6m.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusKernel.dylib
	/bin/rm -f /Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_query/build/Debug/simple_query


PostBuild.simple_query.Release:
/Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_query/build/Release/simple_query:\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusIdx.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDb.dylib\
	/Library/Frameworks/Python.framework/Versions/3.6/lib/libpython3.6m.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusKernel.dylib
	/bin/rm -f /Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_query/build/Release/simple_query


PostBuild.simple_query.MinSizeRel:
/Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_query/build/MinSizeRel/simple_query:\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusIdx.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDb.dylib\
	/Library/Frameworks/Python.framework/Versions/3.6/lib/libpython3.6m.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusKernel.dylib
	/bin/rm -f /Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_query/build/MinSizeRel/simple_query


PostBuild.simple_query.RelWithDebInfo:
/Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_query/build/RelWithDebInfo/simple_query:\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusIdx.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDb.dylib\
	/Library/Frameworks/Python.framework/Versions/3.6/lib/libpython3.6m.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusKernel.dylib
	/bin/rm -f /Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_query/build/RelWithDebInfo/simple_query




# For each target create a dummy ruleso the target does not have to exist
/Library/Frameworks/Python.framework/Versions/3.6/lib/libpython3.6m.dylib:
/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDb.dylib:
/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusIdx.dylib:
/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusKernel.dylib:
