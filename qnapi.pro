CONFIG += warn_on \
 thread \
 qt \
 resources \
 release
TEMPLATE = app
SOURCES += src/main.cpp \
 src/forms/frmprogress.cpp \
 src/forms/frmabout.cpp \
 src/forms/frmoptions.cpp \
 src/forms/frmupload.cpp \
 src/forms/frmcorrect.cpp \
 src/forms/frmreport.cpp \
 src/forms/frmscan.cpp \
 src/forms/frmcreateuser.cpp \
 src/forms/frmsummary.cpp \
 src/forms/frmnapiprojektconfig.cpp \
 src/forms/frmlistsubtitles.cpp \
 src/qnapiconfig.cpp \
 src/qnapiapp.cpp \
 src/movieinfo.cpp \
 src/qmultiparthttprequest.cpp \
 src/qcumber/qmanagedrequest.cpp \
 src/qcumber/qmanagedsocket.cpp \
 src/qcumber/qsingleapplication.cpp \
 src/qnapiabstractengine.cpp \
 src/qnapiprojektengine.cpp \
 src/qnapicli.cpp \
 src/qnapiopendialog.cpp \
 src/xmlrpc/client.cpp \
 src/xmlrpc/request.cpp \
 src/xmlrpc/variant.cpp \
 src/xmlrpc/response.cpp \
 src/qnapi.cpp \
 src/qopensubtitlesengine.cpp \
 src/qnapilanguage.cpp \
 src/forms/frmopensubtitlesconfig.cpp
HEADERS += src/forms/frmprogress.h \
 src/forms/frmabout.h \
 src/forms/frmoptions.h \
 src/forms/frmupload.h \
 src/forms/frmcorrect.h \
 src/forms/frmreport.h \
 src/forms/frmscan.h \
 src/forms/frmcreateuser.h \
 src/forms/frmsummary.h \
 src/forms/frmnapiprojektconfig.h \
 src/forms/frmlistsubtitles.h \
 src/version.h \
 src/qnapiconfig.h \
 src/qnapiapp.h \
 src/movieinfo.h \
 src/qmultiparthttprequest.h \
 src/qnapithread.h \
 src/synchttp.h \
 src/qcumber/qmanagedrequest.h \
 src/qcumber/qmanagedsocket.h \
 src/qcumber/qsingleapplication.h \
 src/qcumber/qcumber.h \
 src/qnapiabstractengine.h \
 src/qnapiprojektengine.h \
 src/qnapicli.h \
 src/qnapiopendialog.h \
 src/xmlrpc/qsyncxmlrpcclient.h \
 src/xmlrpc/variant.h \
 src/xmlrpc/client.h \
 src/xmlrpc/request.h \
 src/xmlrpc/response.h \
 src/qcheckedlistwidget.h \
 src/qnapi.h \
 src/qnapisubtitleinfo.h \
 src/qopensubtitlesengine.h \
 src/qnapilanguage.h \
 src/forms/frmopensubtitlesconfig.h
FORMS += ui/frmprogress.ui \
 ui/frmabout.ui \
 ui/frmoptions.ui \
 ui/frmupload.ui \
 ui/frmcorrect.ui \
 ui/frmreport.ui \
 ui/frmscan.ui \
 ui/frmcreateuser.ui \
 ui/frmsummary.ui \
 ui/napiprojekt/frmnapiprojektconfig.ui \
 ui/opensubtitles/frmopensubtitlesconfig.ui \
 ui/frmlistsubtitles.ui
RESOURCES += res/resources.qrc
QT += network gui core xml
#UI_DIR = tmp
#MOC_DIR = tmp
#RCC_DIR = tmp
#OBJECTS_DIR = tmp
INCLUDEPATH += src

 INSTALL_PREFIX =  /usr
 target.path =  $${INSTALL_PREFIX}/bin
 doc.path =  $${INSTALL_PREFIX}/share/doc/$${TARGET}
 doc.files =  doc/ChangeLog \
  doc/changelog.gz \
  doc/README \
  doc/README.pl \
  doc/LICENSE \
  doc/LICENSE.pl \
  doc/COPYRIGHT \
  doc/qnapi-download.desktop \
  doc/qnapi-download.schemas
 man.path =  $${INSTALL_PREFIX}/share/man/man1
 man.files =  doc/$${TARGET}.1.gz
 icons.path =  /usr/share/icons
 icons.files =  res/qnapi.png  res/qnapi-48.png  res/qnapi-128.png  res/qnapi-512.png
 desktop.path =  /usr/share/applications
 desktop.files =  doc/$${TARGET}.desktop
 dolphin_integration.path =  /usr/share/apps/dolphin/servicemenus
 dolphin_integration.files =  doc/$${TARGET}-download.desktop
 d3lphin_integration.path =  /usr/share/apps/d3lphin/servicemenus
 d3lphin_integration.files =  doc/$${TARGET}-download.desktop
 konqueror_integration.path =  /usr/share/apps/konqueror/servicemenus
 konqueror_integration.files =  doc/$${TARGET}-download.desktop
 kde4_integration.path =  /usr/lib/kde4/share/kde4/services/ServiceMenus
 kde4_integration.files =  doc/$${TARGET}-download.desktop
 INSTALLS =  target \
  doc \
  man \
  icons \
  desktop \
  dolphin_integration \
  d3lphin_integration \
  konqueror_integration \
  kde4_integration

 SOURCES +=  src/qcumber/qinterprocesschannel.cpp
 HEADERS +=  src/qcumber/qinterprocesschannel.h

