/*****************************************************************************
** QNapi
** Copyright (C) 2008-2009 Krzemin <pkrzemin@o2.pl>
**
** This program is free software; you can redistribute it and/or modify
** it under the terms of the GNU General Public License as published by
** the Free Software Foundation; either version 2 of the License, or
** (at your option) any later version.
**
** This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
** WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
**
*****************************************************************************/

#ifndef __QNAPICONFIG__H__
#define __QNAPICONFIG__H__

#include <QSettings>
#include <QString>
#include <QStringList>

class QNapiConfig
{
public:
    static QNapiConfig* instance();

    void reload();
    void save();

    bool firstRun();
    QString version();

    QString p7zipPath();
    void setP7zipPath(const QString & path);

    QString tmpPath();
    void setTmpPath(const QString & path);

    QString language();
    void setLanguage(const QString & language);

    bool ppRemoveLines();
    void setPpRemoveLines(bool remove);

    QStringList ppRemoveWords();
    void setPpRemoveWords(const QStringList & words);

    bool ppChangePermissions();
    void setPpChangePermissions(bool change);

    QString ppPermissions();
    void setPpPermissions(const QString & permissions);

    QString previousDialogPath();
    void setPreviousDialogPath(const QString & path);


private:
    QNapiConfig();
    QNapiConfig(const QNapiConfig &);
    ~QNapiConfig();

    QSettings *settings;

    static QNapiConfig* m_instance;

};

QNapiConfig & GlobalConfig();

#endif
