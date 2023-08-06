# DO NOT EDIT
# This makefile makes sure all linkable targets are
# up-to-date with anything they link to
default:
	echo "Do not invoke directly"

# Rules to remove targets that are older than anything to which they
# link.  This forces Xcode to relink the targets from scratch.  It
# does not seem to check these dependencies itself.
PostBuild.external_simple_viewer2d.Debug:
/Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_viewer2d/build/Debug/external_simple_viewer2d.app/Contents/MacOS/external_simple_viewer2d:\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusAppKit.dylib\
	/Library/Frameworks/Python.framework/Versions/3.6/lib/libpython3.6m.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusNodes.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusIdx.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDb.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusGuiNodes.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusGui.dylib\
	/usr/local/opt/qt/lib/QtOpenGL.framework/QtOpenGL\
	/usr/local/opt/qt/lib/QtWidgets.framework/QtWidgets\
	/usr/local/opt/qt/lib/QtGui.framework/QtGui\
	/usr/local/opt/qt/lib/QtCore.framework/QtCore\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDataflow.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusKernel.dylib
	/bin/rm -f /Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_viewer2d/build/Debug/external_simple_viewer2d.app/Contents/MacOS/external_simple_viewer2d


PostBuild.external_simple_viewer2d.Release:
/Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_viewer2d/build/Release/external_simple_viewer2d.app/Contents/MacOS/external_simple_viewer2d:\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusAppKit.dylib\
	/Library/Frameworks/Python.framework/Versions/3.6/lib/libpython3.6m.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusNodes.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusIdx.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDb.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusGuiNodes.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusGui.dylib\
	/usr/local/opt/qt/lib/QtOpenGL.framework/QtOpenGL\
	/usr/local/opt/qt/lib/QtWidgets.framework/QtWidgets\
	/usr/local/opt/qt/lib/QtGui.framework/QtGui\
	/usr/local/opt/qt/lib/QtCore.framework/QtCore\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDataflow.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusKernel.dylib
	/bin/rm -f /Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_viewer2d/build/Release/external_simple_viewer2d.app/Contents/MacOS/external_simple_viewer2d


PostBuild.external_simple_viewer2d.MinSizeRel:
/Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_viewer2d/build/MinSizeRel/external_simple_viewer2d.app/Contents/MacOS/external_simple_viewer2d:\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusAppKit.dylib\
	/Library/Frameworks/Python.framework/Versions/3.6/lib/libpython3.6m.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusNodes.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusIdx.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDb.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusGuiNodes.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusGui.dylib\
	/usr/local/opt/qt/lib/QtOpenGL.framework/QtOpenGL\
	/usr/local/opt/qt/lib/QtWidgets.framework/QtWidgets\
	/usr/local/opt/qt/lib/QtGui.framework/QtGui\
	/usr/local/opt/qt/lib/QtCore.framework/QtCore\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDataflow.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusKernel.dylib
	/bin/rm -f /Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_viewer2d/build/MinSizeRel/external_simple_viewer2d.app/Contents/MacOS/external_simple_viewer2d


PostBuild.external_simple_viewer2d.RelWithDebInfo:
/Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_viewer2d/build/RelWithDebInfo/external_simple_viewer2d.app/Contents/MacOS/external_simple_viewer2d:\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusAppKit.dylib\
	/Library/Frameworks/Python.framework/Versions/3.6/lib/libpython3.6m.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusNodes.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusIdx.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDb.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusGuiNodes.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusGui.dylib\
	/usr/local/opt/qt/lib/QtOpenGL.framework/QtOpenGL\
	/usr/local/opt/qt/lib/QtWidgets.framework/QtWidgets\
	/usr/local/opt/qt/lib/QtGui.framework/QtGui\
	/usr/local/opt/qt/lib/QtCore.framework/QtCore\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDataflow.dylib\
	/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusKernel.dylib
	/bin/rm -f /Users/scrgiorgio/Desktop/OpenVisus/Samples/simple_viewer2d/build/RelWithDebInfo/external_simple_viewer2d.app/Contents/MacOS/external_simple_viewer2d




# For each target create a dummy ruleso the target does not have to exist
/Library/Frameworks/Python.framework/Versions/3.6/lib/libpython3.6m.dylib:
/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusAppKit.dylib:
/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDataflow.dylib:
/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusDb.dylib:
/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusGui.dylib:
/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusGuiNodes.dylib:
/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusIdx.dylib:
/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusKernel.dylib:
/Users/scrgiorgio/Desktop/OpenVisus/build/install/bin/libVisusNodes.dylib:
/usr/local/opt/qt/lib/QtCore.framework/QtCore:
/usr/local/opt/qt/lib/QtGui.framework/QtGui:
/usr/local/opt/qt/lib/QtOpenGL.framework/QtOpenGL:
/usr/local/opt/qt/lib/QtWidgets.framework/QtWidgets:
